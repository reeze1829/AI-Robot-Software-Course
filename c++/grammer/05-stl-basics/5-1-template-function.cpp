/*****************************************************************
 * 주제: 5-1. template-function (함수 템플릿 심화)
 * 작성일: 2026. 03. 15.
 * [5-1. 핵심 요약]
 * 1. 함수 템플릿: 데이터 타입(int, double 등)만 다르고 로직이 같은 함수들을 하나로 통합함
 * 2. 다중 템플릿: 서로 다른 타입(T, U)을 동시에 사용하여 유연성을 높임
 * 3. 템플릿 특수화: 특정 타입에 대해서만 다른 동작이 필요할 때 별도로 정의 가능함
 *****************************************************************/

#include <iostream>
#include <string>

using namespace std;

template <typename T>                       // 두 변수의 값을 바꾸는 Swap 함수,  컴파일 시점에 결정될 임의의 자료형(Type Parameter)을 선언함
void Swap(T& a, T& b) {    
    T temp = a;                             // T는 호출 시 전달된 인자의 자료형으로 치환됨
    a = b;
    b = temp;
}

template <typename T, typename U>                // 서로 다른 두 개의 자료형(T, U)을 매개변수화하여 함수 내부에서 사용함
void PrintPair(T a, U b) {                       // T와 U가 서로 달라도(예: int와 double) 출력할 수 있게 함
    cout << "데이터 1: " << a << " | 데이터 2: " << b << endl; // 전달된 인자의 타입이 표준 출력(ostream) 연산자를 지원해야 함
}


template <typename T>                        // 배열에서 가장 큰 값을 찾는 함수 (반복문 활용) 
T GetMax(T arr[], int size) {                // T arr[]: 임의의 타입 T로 이루어진 배열의 주소값을 전달받음
    T maxVal = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > maxVal) maxVal = arr[i];    // T 타입에 대해 비교 연산자(>)가 정의되어 있어야 작동함
    }
    return maxVal;                               // 함수 반환 타입 또한 T로 정의됨
}

int main() {                                            
    int num1 = 10, num2 = 20;                     // Swap 테스트(컴파일러의 타입 추론)
    Swap(num1, num2);                             // 컴파일러가 Swap<int> 함수를 생성함
    cout << "[Swap] num1: " << num1 << ", num2: " << num2 << endl;

    double d1 = 1.1, d2 = 9.9;
    Swap(d1, d2);                                // 컴파일러가 Swap<double> 함수를 생성함
    cout << "[Swap] d1: " << d1 << ", d2: " << d2 << endl;

    cout << "------------------------------------" << endl;

   // 다중 파라미터 실행
    PrintPair(100, 3.14);    // int와 double     // PrintPair<int, double>(100, 3.14)로 인스턴스화됨
    PrintPair("Age", 25);    // string과 int     // PrintPair<const char*, int>("Age", 25)로 인스턴스화됨

    cout << "------------------------------------" << endl;

    // 배열 최대값 테스트
    int iArr[] = {1, 5, 3, 9, 2};
    double dArr[] = {1.2, 5.5, 3.3};

    cout << "정수 배열 최대값: " << GetMax(iArr, 5) << endl;   // 정수형 배열 전달 시 T는 int로 결정됨
    cout << "실수 배열 최대값: " << GetMax(dArr, 3) << endl;   // 실수형 배열 전달 시 T는 double로 결정됨

    return 0;
}

/*
 * 1. 명시적 호출: Add<int>(10, 20) 처럼 타입을 직접 지정할 수도 있습니다.
 * 2. 템플릿과 오버로딩: 템플릿 함수와 일반 함수가 이름이 같으면, 일반 함수가 우선순위를 가집니다.
 * 3. 코드 비대화: 템플릿을 너무 많이 쓰면 컴파일러가 각 타입별로 함수를 다 만들어내기 때문에 
 * 실행 파일의 크기가 커질 수 있습니다. (이를 'Code Bloat' 현상이라 함)
 */

/*
 * [복습]
 * 1. 호출 방식: 타입을 직접 안 적어도 컴파일러가 눈치껏 알아서 처리함 (가끔 명시 필요)
 * 2. 동작 방식: 템플릿은 호출될 때마다 해당 타입에 맞는 함수를 자동으로 복사해서 만듦
 * 3. 예외 상황: 모든 타입에 공통으로 적용하기 힘든 특별한 경우(예: 문자열)는 따로 정의 가능함
 * - 이유: 문자열(char*)을 넣으면 '글자'가 아니라 '메모리 주소값'을 비교하는 함정이 발생하기 때문
 * - 해결: 템플릿 특수화를 사용하거나, 주소 비교를 하지 않는 std::string을 사용하면 해결됨
 */
