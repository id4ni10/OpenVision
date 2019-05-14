// OpenVisionCpp.cpp : define o ponto de entrada para o aplicativo do console.
//

#include "stdafx.h"
#include "opencv2/opencv.hpp"

using namespace cv;

int main()
{
	VideoCapture cap(0);

	if (!cap.isOpened())
		return -1;

	Mat edges;

	for (;;)
	{
		Mat frame;
		cap >> frame;
		if (frame.empty()) break; // end of video stream

		cvtColor(frame, edges, COLOR_BGR2GRAY);

		GaussianBlur(edges, edges, Size(7, 7), 1.5, 1.5);

		Canny(edges, edges, 0, 30, 3);

		imshow("this is you, smile! :)", edges);

		if (waitKey(10) == 27) break; // stop capturing by pressing ESC 
	}

    return 0;
}

