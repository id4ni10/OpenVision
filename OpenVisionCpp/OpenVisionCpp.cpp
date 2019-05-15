// OpenVisionCpp.cpp : define o ponto de entrada para o aplicativo do console.
//

#include "stdafx.h"
#include "opencv.hpp"

using namespace cv;

int main()
{
	const std::string rtsp = "rtsp://71014217:123@192.168.0.3:8554/profile0";

	VideoCapture vcap(rtsp);

	//open the video stream and make sure it's opened
	if (!vcap.open(rtsp)) {
		std::cout << "Error opening video stream or file" << std::endl;

		if (!vcap.isOpened())
			return -1;
	}

	Mat edges;

	for (;;)
	{
		Mat frame;
		vcap >> frame;
		if (frame.empty()) break; // end of video stream

		cvtColor(frame, edges, COLOR_BGR2GRAY);

		GaussianBlur(edges, edges, Size(7, 7), 1.5, 1.5);

		Canny(edges, edges, 0, 30, 3);

		imshow("this is you, smile! :)", edges);

		if (waitKey(10) == 27) break; // stop capturing by pressing ESC 
	}

    return 0;
}

