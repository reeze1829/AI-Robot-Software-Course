#include <opencv2/opencv.hpp>
#include <iostream>

using namespace std;
using namespace cv;

// --- 6일차: 특징 추출 및 검출 실습 함수 정의 ---

// [show41] 소벨 필터(Sobel Filter) - 에지 검출의 기초
void show41() {
    Mat src = imread("lenna.png", IMREAD_GRAYSCALE);
    if (src.empty()) return;

    Mat dx, dy;
    // x방향, y방향 미분
    Sobel(src, dx, CV_32F, 1, 0);
    Sobel(src, dy, CV_32F, 0, 1);

    Mat mag;
    magnitude(dx, dy, mag); // 그래디언트 크기 계산
    mag.convertTo(mag, CV_8U);

    Mat edge = mag > 150; // 임계값(Threshold) 처리

    imshow("Original", src);
    imshow("Sobel Edge", edge);
    waitKey();
}

// [show42] 캐니 에지 검출기 (Canny Edge Detector) - 가장 성능 좋은 에지 검출
void show42() {
    Mat src = imread("lenna.png", IMREAD_GRAYSCALE);
    if (src.empty()) return;

    Mat dst;
    // 하단 임계값 50, 상단 임계값 150 (보통 1:2 또는 1:3 비율)
    Canny(src, dst, 50, 150);

    imshow("Original", src);
    imshow("Canny Edge", dst);
    waitKey();
}

// [show43] 허프 변환 직선 검출 (Hough Lines)
void show43() {
    Mat src = imread("building.jpg", IMREAD_GRAYSCALE);
    if (src.empty()) return;

    Mat edge;
    Canny(src, edge, 50, 150);

    vector<Vec4i> lines;
    // 확률적 허프 변환 직선 검출 (선분 찾기)
    HoughLinesP(edge, lines, 1, CV_PI / 180, 160, 50, 5);

    Mat dst;
    cvtColor(src, dst, COLOR_GRAY2BGR);

    for (Vec4i l : lines) {
        line(dst, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0, 0, 255), 2, LINE_AA);
    }

    imshow("Edge", edge);
    imshow("Hough Lines", dst);
    waitKey();
}

// [show44] 허프 변환 원 검출 (Hough Circles)
void show44() {
    Mat src = imread("coins.jpg", IMREAD_GRAYSCALE);
    if (src.empty()) return;

    // 원 검출 전 노이즈 제거 (가우시안 블러 필수)
    Mat blurred;
    GaussianBlur(src, blurred, Size(), 1.0);

    vector<Vec3f> circles;
    // 허프 그래디언트 방식 사용
    HoughCircles(blurred, circles, HOUGH_GRADIENT, 1, 50, 150, 30, 10, 50);

    Mat dst;
    cvtColor(src, dst, COLOR_GRAY2BGR);

    for (Vec3f c : circles) {
        Point center(cvRound(c[0]), cvRound(c[1]));
        int radius = cvRound(c[2]);
        circle(dst, center, radius, Scalar(0, 0, 255), 2, LINE_AA);
    }

    imshow("Hough Circles", dst);
    waitKey();
}

// --- 메인 함수: 메뉴 선택기 ---
int main() {
    int choice;
    while (true) {
        cout << "\n****************************************" << endl;
        cout << "  [Day 06] 특징 추출 및 검출 실습" << endl;
        cout << "  41.소벨에지  42.캐니에지  43.허프직선  44.허프원" << endl;
        cout << "  0.종료" << endl;
        cout << "****************************************" << endl;
        cout << "실습 번호 입력: ";

        if (!(cin >> choice)) break;
        if (choice == 0) break;

        switch (choice) {
            case 41: show41(); break;
            case 42: show42(); break;
            case 43: show43(); break;
            case 44: show44(); break;
            default: cout << "목록의 번호를 선택하세요." << endl;
        }
        destroyAllWindows();
    }
    return 0;
}
