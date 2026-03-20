/*
 * 주제: 5-4. string.h 주요 함수와 안전한 입력(fgets)
 * 날짜: 2026-03-18
 * 내용: 
 * 1. strlen: 문자열의 실제 길이 측정
 * 2. fgets: 공백 포함 문자열 안전하게 입력받기
 * 3. strcmp: 두 문자열 비교하기
 */

#define _CRT_SECURE_NO_WARNINGS 
#include <stdio.h>
#include <string.h>                                 // 문자열 처리 함수(strlen, strcmp 등)를 쓰기 위한 헤더

int main() {
    // fgets로 공백 포함 입력받기
    char intro[50];                                 // 50바이트 크기의 넉넉한 배열 선언
    printf("자기소개를 입력하세요(공백 가능): ");
    
    // fgets(배열명, 크기, 입력장치); 
    // stdin은 키보드 입력을 뜻함. 띄어쓰기를 포함해서 한 줄을 통째로 읽어옴!,  fgets은 사용자가 누른 엔터(\n)까지 문자열로 저장함 - 그래서 출력할때 줄바꿈이 한번 더 일어날 수 있
    fgets(intro, sizeof(intro), stdin);  
    if (strlen(intro) > 0) {
        intro[strlen(intro) - 1] = '\0'; 
    }
    // strlen으로 실제 길이 확인 
    // sizeof(intro)는 50이지만, strlen(intro)는 실제 입력된 글자 수만 계산함
    printf("\n입력한 문장: %s", intro);
    printf("실제 문자열 길이: %d\n", (int)strlen(intro)); 

    // strcmp로 문자열 비교하기
    char secret[] = "apple";                        // 비교 대상 정답
    char input[20];                                 // 사용자 입력용
    
    printf("\n비밀번호를 입력하세요: ");
    scanf("%s", input);                             // strcmp 확인을 위해 짧은 단어 입력

    // strcmp는 두 문자열이 같으면 0을 반환함 (주의: 1이 아님!)  - 두 문자열의 차이를 계산해서 차이가 0이다 = 똑같다는 논리
    // strcmp는 단순히 같냐, 틀리냐만 알려주는 함수가 아니라, 누가 더 앞에 있냐(사전순)를 알려주는 함수
    if (strcmp(input, secret) == 0) {                  //if(input == secret) 이라고 안쓰는 이유는 이렇게 써버리면 글자 내용을 비교하는 게 아니라 두 배열의 메모리 주소가 같냐?라고 물어보는거(서로다른 그릇이니 결과는 거짓)
        printf("성공! 비밀번호가 일치합니다.\n");
    } else {
        printf("실패! 비밀번호가 다릅니다.\n");
    }

    return 0;
}
