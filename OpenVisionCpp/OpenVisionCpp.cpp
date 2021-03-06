// OpenVisionCpp.cpp : define o ponto de entrada para o aplicativo do console.
//

#include "stdafx.h"
#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc.hpp> 
#include <opencv2/features2d.hpp>
#include <vector>

using namespace cv;
using namespace std;

SimpleBlobDetector::Params searchSquarePage();

SimpleBlobDetector::Params searchSquareForm();

void findSquareOne(const Mat &gray, const Mat &drawing);

void fastFeatureDetector(const Mat &gray, const Mat &drawing);

void simpleBlobDetector(const Mat &gray, Mat &drawing, int sequence);

void omrScan(const Mat &gray, Mat &img);

void findContours(const Mat &gray, Mat &drawing);

SimpleBlobDetector::Params searchSquarePage() {
	SimpleBlobDetector::Params params;

	params.minThreshold = 90;
	params.maxThreshold = 160;

	params.filterByArea = true;
	params.minArea = 390;
	params.maxArea = 510;

	params.filterByColor = false;

	params.filterByCircularity = false;

	return params;
}

SimpleBlobDetector::Params searchSquareForm() {
	SimpleBlobDetector::Params params;

	params.minThreshold = 85;
	params.maxThreshold = 165;

	params.filterByArea = true;
	params.minArea = 390;
	params.maxArea = 510;

	params.filterByColor = false;

	params.filterByCircularity = false;

	return params;
}

SimpleBlobDetector::Params resolve(int search) {
	switch (search) {
	case 1:
		return searchSquarePage();
	default:
		return searchSquareForm();
	}
}

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

void findSquareOne(const Mat &gray, const Mat &drawing) {
	Mat mask;
	threshold(gray, mask, 0, 255, THRESH_BINARY_INV | THRESH_OTSU);

	vector<vector<Point>> contours;
	vector<Vec4i> hierarchy;
	findContours(mask, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

	int biggestContourIdx = -1;
	float biggestContourArea = 0;
	for (int i = 0; i < contours.size(); i++) {
		Scalar color = Scalar(255, 0, 0, 255);
		drawContours(drawing, contours, i, color, 1, 8, hierarchy, 0, Point());

		double ctArea = contourArea(contours[i]);
		if (ctArea > biggestContourArea) {
			biggestContourArea = ctArea;
			biggestContourIdx = i;
		}
	}

	// compute the rotated bounding rect of the biggest contour! (this is the part that does what you want/need)
	RotatedRect boundingBox = minAreaRect(contours[biggestContourIdx]);
	// one thing to remark: this will compute the OUTER boundary box, so maybe you have to erode/dilate if you want something between the ragged lines

	// draw the rotated rect
	Point2f corners[4];
	boundingBox.points(corners);
	line(drawing, corners[0], corners[1], Scalar(255, 255, 255));
	line(drawing, corners[1], corners[2], Scalar(255, 255, 255));
	line(drawing, corners[2], corners[3], Scalar(255, 255, 255));
	line(drawing, corners[3], corners[0], Scalar(255, 255, 255));
}

void fastFeatureDetector(const Mat &gray, const Mat &drawing) {
	vector<KeyPoint> v;
	Ptr<FeatureDetector> detector = FastFeatureDetector::create();
	detector->detect(gray, v);
	for (unsigned int i = 0; i < v.size(); i++) {
		const KeyPoint &kp = v[i];
		circle(drawing, Point(kp.pt.x, kp.pt.y), 10, Scalar(255, 0, 0, 255));
	}
}

void simpleBlobDetector(const Mat &gray, Mat &drawing, int sequence) {
	vector<KeyPoint> keypoints;
	Ptr<SimpleBlobDetector> detector = SimpleBlobDetector::create(resolve(sequence));
	detector->detect(gray, keypoints);

	Scalar red(255, 0, 0, 255);
	Scalar green(0, 255, 0);
	Scalar color = keypoints.size() == 4 ? green : red;

	KeyPoint min, max;

	for (unsigned int i = 0; i < keypoints.size(); i++) {
		const KeyPoint &kp = keypoints[i];
		circle(drawing, Point(kp.pt.x, kp.pt.y), 10, color, -1);

		if (i == 0) {
			min = kp;
			max = kp;
		}

		if (kp.pt.x <= min.pt.x & kp.pt.y <= min.pt.y)
			min = kp;

		if (kp.pt.x >= max.pt.x & kp.pt.y >= max.pt.y)
			max = kp;
	}

	Rect rect(min.pt.x, min.pt.y, max.pt.x - min.pt.x, max.pt.y - min.pt.y);
	rectangle(drawing, rect, green);

	putText(drawing, "*", Point(min.pt.x, min.pt.y), FONT_HERSHEY_PLAIN, 2, Scalar(0, 255, 0), 2);

	putText(drawing, "+", Point(max.pt.x, max.pt.y), FONT_HERSHEY_PLAIN, 2, Scalar(0, 0, 255), 2);

	//return (long) &keypoints;
	//drawKeypoints(drawing, keypoints, im_with_keypoints, Scalar(0, 0, 255), DrawMatchesFlags::DRAW_RICH_KEYPOINTS);
}

void omrScan(const Mat &gray, Mat &img) {
	Size dims(10, 5); // this variable should be changed according input
	Mat thresh;
	threshold(gray, thresh, 0, 255, THRESH_BINARY_INV + THRESH_OTSU);

	Mat quad(img.size(), CV_8UC1); // should be improved
	Mat results(img.size(), CV_8UC3);

	vector<Point2f> quad_pts;
	quad_pts.push_back(Point2f(0, 0));
	quad_pts.push_back(Point2f(quad.cols, 0));
	quad_pts.push_back(Point2f(quad.cols, quad.rows));
	quad_pts.push_back(Point2f(0, quad.rows));

	vector<Point2f> corners;
	vector<vector<Point>> contours;

	findContours(thresh.clone(), contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

	for (size_t i = 0; i < contours.size(); i++) {
		RotatedRect minRect = minAreaRect(Mat(contours[i]));

		Point2f rect_points[4];
		minRect.points(rect_points);

		if (Rect(minRect.boundingRect()).width > img.cols / 2)
			for (int j = 0; j < 4; j++) {
				Point2f pt = quad_pts[j];
				Point2f nearest_pt = rect_points[0];
				double dist = norm(pt - nearest_pt);
				for (int k = 1; k < 4; k++) {
					if (norm(pt - rect_points[k]) < dist) {
						dist = norm(pt - rect_points[k]);
						nearest_pt = rect_points[k];
					}
				}
				corners.push_back(nearest_pt);
			}
	}

	erode(thresh, thresh, Mat(), Point(-1, -1), 10);
	dilate(thresh, thresh, Mat(), Point(-1, -1), 5);

	Mat transmtx = getPerspectiveTransform(corners, quad_pts);
	warpPerspective(img, results, transmtx, img.size());
	warpPerspective(thresh, quad, transmtx, img.size());

	resize(quad, quad, dims);

	for (int i = 0; i < quad.cols; i++) {
		String answer = "";

		answer += quad.at<uchar>(1, i) == 0 ? "" : "A";
		answer += quad.at<uchar>(2, i) == 0 ? "" : "B";
		answer += quad.at<uchar>(3, i) == 0 ? "" : "C";
		answer += quad.at<uchar>(4, i) == 0 ? "" : "D";
		answer += quad.at<uchar>(5, i) == 0 ? "" : "E";

		if (answer.length() > 1) answer = "X"; // Double mark
		int y = 0;
		if (answer == "A") y = results.rows / dims.height;
		if (answer == "B") y = results.rows / dims.height * 2;
		if (answer == "C") y = results.rows / dims.height * 3;
		if (answer == "D") y = results.rows / dims.height * 4;
		if (answer == "E") y = results.rows / dims.height * 5;
		if (answer == "") answer = "[-]";

		putText(img, answer, Point(50 * i + 15, 30 + y),
			FONT_HERSHEY_PLAIN, 2, Scalar(0, 0, 255), 2);
	}
}

RNG rng(12345);

void findContours(const Mat &gray, Mat &drawing) {
	Mat canny_output;
	vector<vector<Point>> contours;
	vector<Vec4i> hierarchy;
	int thresh = 100;

	Canny(gray, canny_output, thresh, thresh * 2, 3);
	findContours(canny_output, contours, hierarchy, RETR_TREE, CHAIN_APPROX_NONE,
		Point(0, 0));


	/*for (int x = 0; x < contours.size(); x++) {
		vector<Point> contour = contours[x];
		contour.area();
	}*/

	for (int i = 0; i < contours.size(); i++) {
		Scalar color = Scalar(rng.uniform(0, 255), rng.uniform(0, 255), rng.uniform(0, 255));
		drawContours(drawing, contours, i, color, 2, 8, hierarchy, 0, Point());
	}
}