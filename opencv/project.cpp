#include "opencv2/opencv.hpp"
#include <iostream>
#include <ctime>
#include <vector>
#define NOMINMAX 
#include <Windows.h>
#include <mmsystem.h> // 사운드 재생용
#pragma comment(lib, "winmm.lib") // 라이브러리 연결

struct Target {
    cv::Point position;
    int radius;
    bool active;

    Target() {
        this->position = cv::Point();
        this->radius = 20;
        this->active = false;
    }
};

cv::Point getRandomPosition(int width, int height, int radius)
{
    // 화면 경계를 벗어나지 않도록 범위 설정
    int x = rand() % (width - 2 * radius) + radius;
    int y = rand() % (height - 2 * radius) + radius;
    return cv::Point(x, y);
}

void runProject() CV_NOEXCEPT
{
    srand((unsigned int)time(0));
    cv::Mat targetImg = cv::imread("me.jpg");
    if (targetImg.empty()) {
        std::cerr << "이미지 파일을 찾을 수 없습니다!" << std::endl;
        return;
    }

    cv::VideoCapture cap(0);
    if (!cap.isOpened()) return;

    cv::namedWindow("GAME", cv::WINDOW_AUTOSIZE);

    int width = cvRound(cap.get(cv::CAP_PROP_FRAME_WIDTH));
    int height = cvRound(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
    cv::Mat prev_gray;

    // --- [이미지 전처리 및 마스크 제작] ---
    cv::resize(targetImg, targetImg, cv::Size(120, 120));
    cv::Mat gray, mask;
    cv::cvtColor(targetImg, gray, cv::COLOR_BGR2GRAY);
    cv::threshold(gray, mask, 250, 255, cv::THRESH_BINARY_INV);

    std::vector<std::vector<cv::Point>> contours;
    cv::findContours(mask, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
    cv::Mat final_mask = cv::Mat::zeros(mask.size(), CV_8UC1);
    if (!contours.empty()) {
        double maxArea = 0; int maxIdx = 0;
        for (int i = 0; i < contours.size(); i++) {
            if (cv::contourArea(contours[i]) > maxArea) {
                maxArea = cv::contourArea(contours[i]);
                maxIdx = i;
            }
        }
        cv::drawContours(final_mask, contours, maxIdx, cv::Scalar(255), -1);
        cv::Mat k = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3));
        cv::erode(final_mask, final_mask, k);
    }

    // --- [게임 변수 설정] ---
    Target target;
    int score = 0;
    int baseSize = 40;
    int currentSize = 40;
    int effectTimer = 0;
    int totalRotation = 0;
    int spawnDelay = 0;
    int specialScore = 0;
    int hitEffectTimer = 0;
    int hitCount = 0;
    target.radius = currentSize / 2;
    target.position = getRandomPosition(width, height, 60);
    cv::VideoWriter videoWriter;
    int fps = 30; // 게임 내 타이머 기준과 동일하게 설정
    int fourcc = cv::VideoWriter::fourcc('M', 'J', 'P', 'G');
    videoWriter.open("game_record.avi", fourcc, fps, cv::Size(width, height), true);

    while (true)
    {
        cv::Mat frame, gray_frame, diff, thresh;
        cap >> frame;
        if (frame.empty()) break;
        cv::flip(frame, frame, 1);
        cv::cvtColor(frame, gray_frame, cv::COLOR_BGR2GRAY);
        cv::GaussianBlur(gray_frame, gray_frame, cv::Size(15, 15), 0);
        if (prev_gray.empty()) { gray_frame.copyTo(prev_gray); continue; }

        if (prev_gray.size() != gray_frame.size()) cv::resize(prev_gray, prev_gray, gray_frame.size());
        cv::absdiff(prev_gray, gray_frame, diff);
        cv::threshold(diff, thresh, 25.0, 255.0, cv::THRESH_BINARY);
        if (spawnDelay > 0) spawnDelay--;

        cv::Rect targetRect(target.position.x - target.radius,
            target.position.y - target.radius,
            currentSize, currentSize);

        if (targetRect.x >= 0 && targetRect.y >= 0 &&
            targetRect.x + targetRect.width <= frame.cols &&
            targetRect.y + targetRect.height <= frame.rows)
        {
            if (spawnDelay == 0) {
                if (cv::countNonZero(thresh(targetRect)) > (targetRect.width * targetRect.height) * 0.03) {
                    if (effectTimer > 0) {
                        specialScore++;
                        hitCount++;
                        currentSize += 2;
                        hitEffectTimer = 10;
                        PlaySound(TEXT("hit4.wav"), NULL, SND_FILENAME | SND_ASYNC | SND_NOSTOP);
                        spawnDelay = 5;
                    }
                    else {
                        score++;
                        hitCount = 0;
                        PlaySound(TEXT("hit.wav"), NULL, SND_FILENAME | SND_ASYNC);  //파일 이름을 사용한다, 소리가 재생되는 동안 프로그램이 멈추지 않고 게임이 계속 진행
                        totalRotation = (totalRotation + 90) % 360;
                        target.position = getRandomPosition(width, height, 60);
                        spawnDelay = 20;

                        if (score > 0 && score % 10 == 0) {
                            PlaySound(TEXT("Fevertimestart.WAV"), NULL, SND_FILENAME | SND_ASYNC);
                            currentSize = 120;
                            effectTimer = 150;
                        }
                    }
                }
            }
        }

        if (effectTimer > 0) {
            effectTimer--;
            if (effectTimer == 0) currentSize = baseSize;
        }
        target.radius = currentSize / 2;

        cv::Mat tempImg, tempMsk;
        cv::resize(targetImg, tempImg, cv::Size(currentSize, currentSize), 0, 0, cv::INTER_AREA);
        cv::resize(final_mask, tempMsk, cv::Size(currentSize, currentSize), 0, 0, cv::INTER_AREA);
        cv::threshold(tempMsk, tempMsk, 180, 255, cv::THRESH_BINARY);

        if (effectTimer > 0) {
            cv::Mat hsv, skinMask;
            cv::cvtColor(tempImg, hsv, cv::COLOR_BGR2HSV);
            cv::inRange(hsv, cv::Scalar(0, 40, 80), cv::Scalar(17, 150, 255), skinMask);
            cv::bitwise_and(skinMask, tempMsk, skinMask);

            std::vector<cv::Mat> channels;
            cv::split(tempImg, channels);

            int redIntensity = std::min(hitCount * 8, 80);
            int greenReduce = std::min(hitCount * 5, 50);
            cv::add(channels[2], redIntensity, channels[2], skinMask);
            cv::subtract(channels[1], greenReduce, channels[1], skinMask);
            cv::merge(channels, tempImg);
        }

        if (hitEffectTimer > 0) {
            float flip_dir = (hitCount % 2 == 0) ? 1.0f : -1.0f;
            float shear_factor = 0.5f * sin(hitEffectTimer * 0.5f);
            float x_offset = (flip_dir == -1.0f) ? (float)(currentSize - 1) : 0;

            cv::Mat M = (cv::Mat_<float>(2, 3) <<
                flip_dir, shear_factor, x_offset - (shear_factor * currentSize / 2.0f),
                0, 1, 0);

            cv::warpAffine(tempImg, tempImg, M, tempImg.size(), cv::INTER_CUBIC, cv::BORDER_REPLICATE);

            cv::warpAffine(tempMsk, tempMsk, M, tempMsk.size(), cv::INTER_NEAREST, cv::BORDER_CONSTANT, cv::Scalar(0));
      
            hitEffectTimer--;
        }

        else if (effectTimer == 0 && totalRotation != 0) {
            cv::Point2f center(tempImg.cols / 2.0f, tempImg.rows / 2.0f);
            cv::Mat R = cv::getRotationMatrix2D(center, (double)totalRotation, 1.0);
            cv::warpAffine(tempImg, tempImg, R, tempImg.size(), cv::INTER_LINEAR, cv::BORDER_REPLICATE);
            cv::warpAffine(tempMsk, tempMsk, R, tempMsk.size(), cv::INTER_NEAREST, cv::BORDER_CONSTANT, cv::Scalar(0));
        }

        cv::threshold(tempMsk, tempMsk, 200, 255, cv::THRESH_BINARY);

        if (effectTimer > 0) {
            cv::Mat k = cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(3, 3));
            cv::erode(tempMsk, tempMsk, k);
            cv::GaussianBlur(tempMsk, tempMsk, cv::Size(9, 9), 0);
            cv::threshold(tempMsk, tempMsk, 130, 255, cv::THRESH_BINARY);
        }

        int drawX = std::max(0, target.position.x - target.radius);
        int drawY = std::max(0, target.position.y - target.radius);
        cv::Rect finalDrawRect(drawX, drawY, currentSize, currentSize);
        if (finalDrawRect.x + finalDrawRect.width <= frame.cols &&
            finalDrawRect.y + finalDrawRect.height <= frame.rows)
        {
            tempImg.copyTo(frame(finalDrawRect), tempMsk);
        }

        if (effectTimer > 0) {
            double seconds = (double)effectTimer / 30.0;
            char buf[20];
            sprintf_s(buf, sizeof(buf), "%05.2f", seconds);
            std::string timerText = std::string(buf);
            std::string titleText = "FEVER";

            // 1. 크기 및 폰트 설정 (작게 조절)
            int myFont = cv::FONT_HERSHEY_PLAIN;
            double myScale = 1.2; // 1.5에서 1.2로 축소
            int myThick = 2;      // 2에서 1로 축소하여 더 얇고 깔끔하게

            // 2. 박스 크기 계산 (글자 크기에 맞춰 더 작게 설정)
            int boxW = 100; // 박스 가로폭 축소
            int boxH = 60;  // 박스 세로높이 축소
            cv::Point boxTopLeft((width / 2) - (boxW / 2), 5);
            cv::Point boxBottomRight((width / 2) + (boxW / 2), 5 + boxH);

            // 3. 검정색 박스 그리기
            cv::rectangle(frame, boxTopLeft, boxBottomRight, cv::Scalar(0, 0, 0), -1);

            // 4. 글자 가운데 정렬 계산 및 출력
            // [FEVER 글자 정렬]
            int base = 0;
            cv::Size titleSize = cv::getTextSize(titleText, myFont, myScale, myThick, &base);
            cv::putText(frame, titleText, cv::Point((width - titleSize.width) / 2, 28),
                myFont, myScale, cv::Scalar(0, 255, 255), myThick);

            // [타이머 숫자 정렬]
            cv::Size timerSize = cv::getTextSize(timerText, myFont, myScale, myThick, &base);
            cv::putText(frame, timerText, cv::Point((width - timerSize.width) / 2, 55),
                myFont, myScale, cv::Scalar(0, 255, 255), myThick);

            // 5. 화면 테두리 빨간색 (피버 강조)
            cv::rectangle(frame, cv::Point(0, 0), cv::Point(width, height), cv::Scalar(0, 0, 255), 10);
        }

        // 2. 좌측 스코어 (Score)
        cv::putText(frame, "Score : " + std::to_string(score), cv::Point(20, 30),
            cv::FONT_HERSHEY_PLAIN, 2, cv::Scalar(0, 255, 255), 2);

        // 3. 우측 피버 스코어 (FEVER)
        std::string specStr = "FEVER: " + std::to_string(specialScore);
        cv::putText(frame, specStr, cv::Point(width - 230, 30),
            cv::FONT_HERSHEY_PLAIN, 2, cv::Scalar(0, 255, 255), 2);

        if (videoWriter.isOpened()) {
            videoWriter.write(frame);
        }

        cv::imshow("GAME", frame);
        gray_frame.copyTo(prev_gray);
        if (cv::waitKey(10) == 27) break;
    }
    if (videoWriter.isOpened()) {
        videoWriter.release();
    }
    cap.release();
    cv::destroyAllWindows();
}