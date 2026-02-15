/*****************************************************************
 * 주제: 1-3. 디폴트 매개변수 (Default Parameters)
 * 작성일: 2026. 02. 15.
 * 설명: 
 * - 인자 생략 시 자동으로 채워지는 '기본값' 설정법 실습
 * - "값 전달은 왼쪽부터, 설정은 오른쪽부터" 규칙 이해
 * - 오버로딩과 혼용 시 발생하는 '모호성(Ambiguity)' 주의
 *****************************************************************/

//1.
#include <iostream>

void hello(std::string name = "손님") {                 // name의 기본값 "손님"
    std::cout << "안녕, " << name << "!" << std::endl;
}

int main() {
    hello("철수"); // 직접 입력: "안녕, 철수!"
    hello();       // 생략하면 기본값 "손님" 이 나옴!
    return 0;
}

//2.
#include <iostream>
#include <string>

void setWindow(std::string title, int width = 800, int height = 600) {                                // 디폴트 값은 무조건 오른쪽 부터 채워야함!
    std::cout << "제목: " << title << " / 크기: " << width << "x" << height << std::endl;             // 올바른 예: (int a, int b = 10, int c = 20)
                                                                                                      // 잘못된 예: (int a = 10, int b, int c) -> 컴파일 에러!
}

int main() {
   
    setWindow("게임", 1920, 1080);       // 다 입력할 때
    setWindow("웹", 1024);               // height만 생략 (오른쪽 끝부터 생략 가능)
    setWindow("메모장");                 // width, height 둘 다 생략

    return 0;
}

/* 오버로딩과 함께 사용할 때의 모호함
 * 1. void func(int a) { ... }
 * 2/ void func(int a, int b = 5) { ... }
 * func(10);                             // 1.a=10 2, a=10 b=5 으로 둘다 가능하기에 어떤 함수를 호출할지 컴파일러가 결정을 못해서 에러가 발생함!
 * func();                               // 1번 2번 둘다 인자 부족으로 에러 - 인자 한개는 줘야함
 * void func(int a = 10, int b) { ... }
 * func(20);                             // a에 20을 넣는것도 불가능하고, 첫번째 인자인 a를 건너뛰고 b에 20을 넣는것도 규칙상 불가능!!
 */
//  값 전달(호출)은 왼쪽부터!  기본값 설정(정의)은 오른쪽부터!
//  오른쪽부터 (값이 안들어와도 되는)기본값을 채운다는 건 왼쪽부터 채워져 내려오는 실제 값과 부딪히지 않게 하기 위한 약속임!!!







