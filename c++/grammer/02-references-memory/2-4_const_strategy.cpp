/*****************************************************************
 * 주제: 2-4. const를 활용한 데이터 보호 전략 (Const Correctness)
 * 작성일: 2026. 02. 25.
 * 설명: 
 * - const의 위치(* 기준 왼쪽/오른쪽)에 따른 데이터 및 주소값 보호 학습
 * - const T&를 활용하여 성능(복사 방지)과 안전(수정 방지)을 동시에 챙기는 법 이해
 * - const는 단순 문법을 넘어 개발자 간의 '수정 불가 약속'임을 인지
 *****************************************************************/

#include <iostream>

void printInfo(const int &ref) {                   // const 참조자 매개변수 = const T& ref (상수 참조자) - T 타입의 원본을 참조하되, 읽기 전용으로만 씀  
    std::cout << "값: " << ref << std::endl;       // ref = 100; // 에러! 읽기 전용 (데이터 보호) ,  복사 비용은 아끼면서 원본 보호. (실무 최다 사용!)
}
// void func(Image img): 이미지 전체를 똑같이 복사해서 가져옴 (메모리 낭비, 속도 느림)
// void func(Image &img): 원본을 그대로 쓰기 때문에 빠르지만, 함수 안에서 실수로 이미지를 지워버릴 수도 있음! (위험함)
// void func(const Image &img): 원본을 그대로 써서 빠르면서, const 덕분에 절대 수정할 수 없음! (퍼펙트)
int main() {
    int num = 10;
    int target = 20;

    // 포인터와 const의 위치 
    // (A) 가리키는 대상이 const (데이터 상수화)  
    const int* ptr1 = &num;   // *의 왼쪽에 const. 즉, int 타입의 *ptr(데이터)이 상수! (데이터 보호) 
    // *ptr1 = 30;       // 에러! ptr1을 통해서 값을 바꿀 수 없음 (내용물 변경 불가능)
    ptr1 = &target;      // 가능! 다른 곳을 가리키는 건 허용

    // (B) 포인터 자체가 const (가리키는 방향 고정)
    int* const ptr2 = &num;   // *의 오른쪽에 const. 즉, int 타입을 가리키는 ptr(주소값)이 상수! (주소 고정)
    *ptr2 = 30;          // 가능! 값은 바꿀 수 있음
    // ptr2 = &target;   // 에러! 다른 곳을 가리킬 수 없음 (방향변경 불가능)

    // (C) 둘 다 const (완전 봉쇄)
    const int* const ptr3 = &num;
    // *ptr3 = 40;          // 에러!
    // ptr3 = &target;      // 에러!
    
    printInfo(num);

    return 0;
}
 // const T* ptr   -   const int ptr일 수도 있고, const double ptr일 수도 있다는 뜻
 // const T*: 가리키는 값을 보호하고 싶을 때.
 // T* const: 포인터의 가리키는 방향을 고정하고 싶을 때
 // const T&: 성능과 안전을 동시에 챙기는 실무 표준 패턴
 // const를 사용하는 가장 큰 이유는 작성자뿐만 아니라 사용자에게 '이 변수는 여기서 절대 변하지 않으니 안심하고 써도 된다'는 강력한 신뢰를 주기 위함
