/*****************************************************************
 * 주제: 1-1. iostream-namespace 이해 및 활용
 * 작성일: 2026. 02. 11.
 * 설명: 
 * - std::cin, std::cout을 활용한 기본 입출력
 * - namespace std의 장단점 및 std::를 직접 사용하여 이름 충돌을 방지하는 코딩 습관 실습
 * - 여러 개의 변수를 연속으로 입력받는 방법(cin >> a >> b)
 *****************************************************************/
// 1.
#include <iostream>  // 입출력을 위한 표준 스트림 라이브러리(input/output stream)
using namespace std; // std라는 이름공간을 생략, 편리하지만 이름충돌 가능성이 있을 수 있음
                     // std를 직접붙이는 이유는 이름 충돌을 방지하고 코드의 출처를 명확히 하여 유지보수를 쉽게하기 위해!  

int main(){
     int number;

     cout << "숫자를 입력하세요: ";  // << 데이터 출력 연산자
     cin >> number; // >> 데이터를 변수에 저장(입력) 

     cout << "입력하신 숫자는" << number << "입니다." << endl;
     return 0;
}


//2. 사용자 정보 입력 및 평균게산
#include <iostream>
#include <string> //문자열

int main(){
    std::string studentName;
    int korean, english, math;

    std::cout << "---- 성적 입력 프로그램 ----" << std::endl;

    std::cout << "학생 이름: ";
    std::cin >> studentName;

    std::cout << "국어, 영어, 수학 점수 입력 : (예: 80 90 100): ";
    std::cin >> korean >> english >> math;

    int total = korean + english + math;
    double average = total / 3.0;            //소수점 계산을 위해 3.0으로 나눔

    std::cout << "\n--- 결과 리포트 ---" << std::endl;
    std::cout << "이름: " << studentName << std::endl;
    std::cout << "총점: " << total << "점" << std::endl;
    std::cout << "평균: " << average << "점" << std::endl;

    return 0;
    }
    
  



     
