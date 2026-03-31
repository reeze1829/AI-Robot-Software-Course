/*
 * 주제: 7-1. 구조체 기초 (struct Basic)
 * 날짜: 2026-03-31
 * 핵심: 연관된 서로 다른 타입의 데이터를 하나로 묶는 바구니 만들기
 */

#include <stdio.h>
#include <string.h>

struct Student {             // 구조체 설계 (붕어빵 틀 만들기)
    char name[20];
    int age;
    double score;
};

int main() {
    struct Student s1 = {"홍길동", 20, 95.5};   // 구조체 변수 선언 및 초기화 (실제 붕어빵 굽기), C에서는 변수 선언 시 struct 키워드를 반드시 붙여야 함
    // s1은 메모리에 약 32바이트(20 + 4 + 8) 크기의 연속된 덩어리로 잡힘!
    printf("--- 학생 정보 출력 ---\n");         // 점(.) 연산자로 멤버에 접근하기 
    printf("이름: %s\n", s1.name);
    printf("나이: %d\n", s1.age);
    printf("성적: %.1f\n", s1.score);

    s1.age = 21;                            // 값 수정하기
    strcpy(s1.name, "이순신");              // 문자열은 대입 대신 strcpy 사용!, s1.name = "이순신"; (X) - 배열 이름은 상수라 직접 대입 불가, strcpy 필수!

    printf("\n--- 정보 수정 후 ---\n");
    printf("이름: %s, 나이: %d\n", s1.name, s1.age);

    return 0;
}

// [나중을 위한 핵심 노트]
// 1. 배열은 같은 타입만 묶지만, 구조체는 다른 타입도 하나로 묶을 수 있음
// 2. struct Student는 새로운 자료형 이름이고, s1이 실제 변수임
// 3. 멤버를 부를 때는 변수명.멤버명 (마침표 연산자)을 사용함!
// 4. 구조체 전체를 다른 구조체에 대입하는 것(s2 = s1)은 가능함! (배열과 달리 메모리 덩어리를 통째로 복사해줌)
