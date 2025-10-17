#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>
#include <opencv2/features2d.hpp>

int main() {
    // This URL must be an active video stream on your network
    std::string url = "http://192.168.1.73:8080/video";

    // Create a VideoCapture object
    cv::VideoCapture cap(url);

    // Check if the video stream was opened successfully
    if (!cap.isOpened()) {
        std::cerr << "Error: Could not open video stream at " << url << std::endl;
        return -1;
    }

    // Create an A-KAZE detector object using a smart pointer
    cv::Ptr<cv::AKAZE> detector = cv::AKAZE::create();

    std::cout << "Successfully opened video stream. Press 'ESC' to exit." << std::endl;

    for (;;) {
        cv::Mat frame;
        // Read a new frame from the video stream
        cap >> frame; 

        // If the frame is empty, break the loop
        if (frame.empty()) {
            std::cerr << "Error: Frame is empty or stream ended." << std::endl;
            break;
        }

        // Convert the frame to grayscale
        cv::Mat gray;
        cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);

        // Detect keypoints
        std::vector<cv::KeyPoint> keypoints;
        detector->detect(gray, keypoints);

        // Draw the keypoints on the original color frame
        cv::Mat frame_with_keypoints;
        cv::drawKeypoints(frame, keypoints, frame_with_keypoints, cv::Scalar(0, 255, 0), cv::DrawMatchesFlags::DEFAULT);

        // Display the output
        cv::imshow("C++ Features", frame_with_keypoints);

        // Wait for 1ms. If the 'ESC' key (ASCII 27) is pressed, break the loop
        if (cv::waitKey(1) == 27) {
            break;
        }
    }

    // The VideoCapture and Mat objects are automatically released when they go out of scope.
    // We can explicitly destroy the windows.
    cv::destroyAllWindows();
    
    return 0;
}