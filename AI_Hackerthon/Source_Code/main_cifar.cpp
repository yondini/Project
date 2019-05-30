//** Image classification

#include <vector>
#include <memory>
#include <string>

#include <opencv2/opencv.hpp>
#include <inference_engine.hpp>

using namespace std;
using namespace InferenceEngine;

const char *labels[13] = {"airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "sheep", "truck", "rock", "scissors", "paper"};

int main(int argc, char *argv[]) {

	// ---------------------Load A Plugin for Inference Engine-----------------------------------------

	InferenceEngine::PluginDispatcher dispatcher({""});
	InferencePlugin plugin(dispatcher.getSuitablePlugin(TargetDevice::eCPU));

	// --------------------Load IR Generated by ModelOptimizer (.xml and .bin files)------------------------

	CNNNetReader network_reader;

	network_reader.ReadNetwork("/home/intel/my_model/cifar.xml");
	network_reader.ReadWeights("/home/intel/my_model/cifar.bin");
	network_reader.getNetwork().setBatchSize(1);

	CNNNetwork network = network_reader.getNetwork();

	// -----------------------------Prepare input blobs-----------------------------------------------------

	auto input_info = network.getInputsInfo().begin()->second;
	auto input_name = network.getInputsInfo().begin()->first;

	input_info->setPrecision(Precision::U8);

	// ---------------------------Prepare output blobs------------------------------------------------------

	auto output_info = network.getOutputsInfo().begin()->second;
	auto output_name = network.getOutputsInfo().begin()->first;

	output_info->setPrecision(Precision::FP32);

	// -------------------------Loading model to the plugin and then infer----------------------------------

	auto executable_network = plugin.LoadNetwork(network, {});
	auto infer_request = executable_network.CreateInferRequest();

	auto input = infer_request.GetBlob(input_name);
	auto input_data = input->buffer().as<PrecisionTrait<Precision::U8>::value_type*>();

	/* Copying data from image to the input blob */
	cv::Mat ori_image, infer_image;
	ori_image = cv::imread("/home/intel/sample/input.jpg");
	cv::resize(ori_image, infer_image, cv::Size(input_info->getDims()[0], input_info->getDims()[1]));

	//cv::namedWindow("title", cv::WINDOW_NORMAL);
	//cv::resizeWindow("title", 600,600);
	//cv::imshow("title", infer_image);
	//cv::waitKey(0);

	size_t channels_number = input->dims()[2];
	size_t image_size = input->dims()[1] * input->dims()[0];

	for (size_t pid = 0; pid < image_size; ++pid) {
	    for (size_t ch = 0; ch < channels_number; ++ch) {
		input_data[ch * image_size + pid] = infer_image.at<cv::Vec3b>(pid)[ch];
	    }
	}

	/* Running the request synchronously */
	infer_request.Infer();

	// ---------------------------Postprocess output blobs--------------------------------------------------

	auto output = infer_request.GetBlob(output_name);

	auto output_data = output->buffer().as<PrecisionTrait<Precision::FP32>::value_type*>();

	vector<unsigned> results;
	/*  This is to sort output probabilities and put it to results vector */
	TopResults(13, *output, results);

	cout << endl << "Top 13 results:" << endl << endl;
	for (size_t id = 0; id < 13; ++id) {
	    cout.precision(7);
	    auto result = output_data[results[id]];
	    cout << left << fixed << result << " label #" << results[id] << ", " << labels[results[id]] << endl;
	}

	return EXIT_SUCCESS;
}