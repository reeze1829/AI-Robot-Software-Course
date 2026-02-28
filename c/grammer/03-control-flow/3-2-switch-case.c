/*
 * 주제: 3-2. 다중 선택문 (switch-case) & 제어 흐름 심화
 * 날짜: 2026-02-28
 * 학습 내용:
 * 1. 고정값 분기: 변수가 정수/문자일 때 특정 값과 일치하는지 빠르게 판단 (Jump Table 원리)
 * 2. 흐름 제어(break): 각 case 실행 후 switch문을 탈출하여 의도치 않은 실행 방지
 * 3. Fall-through 기법: break를 의도적으로 생략하여 여러 case(학점, 계절 등)를 하나의 로직으로 그룹화
 * 4. 제어문 중첩: switch 내부에 if문을 사용하여 특정 상황(예: 나눗셈 0)의 예외 처리 구현
 * 5. 타입 제한: 실수(float, double)는 사용 불가능하며, 오직 정수 계열과 문자형만 가능함을 이해
 */
#include <stdio.h>

int main() {
    int choice = 2;
    printf("--- 가상 자판기 ---\n");
    printf("1. 콜라 / 2. 사이다 / 3. 환타 / 4. 물\n");

    switch (choice) {            // 값에 의한 점프: choice가 2면 바로 case 2로 점프해서 속도가 빠름
        case 1:                  // 범위를 지정할 수 없어 정확한 값만 가능하고, 실수(float) 불가능! 정수나 문자형만 가능함!!
            printf("콜라를 선택하셨습니다. (1,000원)\n");
            break;               // 여기서 멈추고 switch문을 나감. break가 없으면 다음 case까지 줄줄이 실행되는 Fall-through 발생
        case 2:
            printf("사이다를 선택하셨습니다. (1,000원)\n");
            break;
        case 3:
            printf("환타를 선택하셨습니다. (1,000원)\n");
            break;
        case 4:
            printf("물을 선택하셨습니다. (500원)\n");
            break;
        default:
            printf("잘못된 번호입니다. 1~4번 중에서 골라주세요.\n");
            break;
    }

    char grade = 'B';   
    printf("\n--- 학점 판정 (%c) ---\n", grade);    // 학점 판정 & 의도적 Fall-through (여러 case 묶기)
    switch (grade) {                                // 그룹화: A, B, C를 세로로 나열하면 "하나라도 해당하면 합격"이라는 논리가 됨
        case 'A':
        case 'B':
        case 'C':
            printf("합격(Pass)입니다!\n");           // A, B, C 모두 여기서 처리됨
            break;
        default:
            printf("재수강 대상입니다.\n");
            break;
    }

    int month = 10;
    printf("\n--- 계절 판별기 (%d월) ---\n", month);  // 계절 판별기 (의도적 break 생략의 실전 활용)
    switch (month) {                                  // 가독성: if문으로 짰을 때보다 훨씬 직관적이고 코드가 짧아짐
        case 12: case 1: case 2:
            printf("겨울입니다 \n"); break;
        case 3: case 4: case 5:
            printf("봄입니다 \n"); break;
        case 6: case 7: case 8:
            printf("여름입니다 \n"); break;
        case 9: case 10: case 11:
            printf("가을입니다 \n"); break;
        default:
            printf("유효한 월을 입력하세요.\n"); break;
    }

    char op = '*';                  
    int n1 = 10, n2 = 5;        
    printf("\n---  미니 계산기 (%d %c %d) ---\n", n1, op, n2);
    switch (op) {                                            // 문자 기반 대소문자 통합 & 미니 계산기, 문자 활용: 연산 기호 '+', '-', '*', '/'도 결국 내부적으론 정수(아스키코드)라 switch 가능!
        case '+': printf("결과: %d\n", n1 + n2); break;
        case '-': printf("결과: %d\n", n1 - n2); break;
        case '*': printf("결과: %d\n", n1 * n2); break;
        case '/': 
            if (n2 != 0) printf("결과: %d\n", n1 / n2);      // 제어문 중첩: switch 안에 if를 넣어 특정 case에서만 발생하는 예외(0 나누기)를 처리함
            else printf("0으로 나눌 수 없습니다!\n");
            break;
        default: printf("지원하지 않는 연산자입니다.\n"); break;
    }

    return 0;
}
