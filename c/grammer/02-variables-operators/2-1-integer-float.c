/*
 * 주제: 2-1. 데이터 타입의 크기와 한계 (정수와 실수)
 * 날짜: 2026-02-18
 * 내용: 
 * 1. 정수 오버플로우: int(4byte)의 범위를 넘어서는 계산 시 long long(8byte) 사용법 학습
 * 2. 부동소수점 오차: 실수가 근사값으로 저장됨에 따라 발생하는 오차 확인
 * 3. 정밀도 비교: float(4byte)보다 double(8byte)이 더 정밀하게 데이터를 처리하는 이유 분석
 * 4. 자료형 선택 기준: 정확한 정수 계산(long long) vs 정밀한 실수 계산(double)
 */

//1.
#include <stdio.h>
#include <limits.h> 

int main() {
    // 저축 계산기 (정수 범위 테스트)
    int balance = 2100000000; // 현재 잔고 21억
    int interest = 100000000;  // 이자 1억 추가
    
    printf("현재 잔고: %d\n", balance);
    printf("이자 지급 후 잔고: %d\n", balance + interest);   // 결과가 마이너스로 나오는데 이게 오버플로우임!
    long long big_balance = 2200000000LL;                   // longlong, double(8byte)  >> int, float(4byte) >> char(1byte) 순으로 크기가 나뉨
    printf("이자 후 잔고(long long): %lld\n", big_balance); // double(실수)이랑 longlong(정수)의 크기는 같지만 22억 같은 정수는 소수점 오차가 없는 long long이 가장 정확함! - 정확한 정수계산시에 필요
    return 0;                                              // 실수는 항상 오차의 위험이 있음!!!
}

//2.
#include <stdio.h>

int main() {
    float sum = 0.0f;
    double d_sum = 0.0;
  
    for (int i = 0; i < 100; i++) {
        sum += 0.1f;
        d_sum += 0.1;
    }

    printf("0.1을 100번 더한(float) 결과: %f\n", sum); // 10.000002 오차발생
    printf("double 결과: %f\n", d_sum);                // 10.000000 오차가 훨씬 적음!   float보다 double이 소수점을 더 정밀하게 표현해서 오차가 적음!!
    printf("우리가 기대한 값: 10.000000\n");           // 오차 때문에 10.000000이 나오지않고 10.000002가 나옴, 0.1을 정확히 표현못해서 근사값으로 정하기때문에
    return 0;
}




