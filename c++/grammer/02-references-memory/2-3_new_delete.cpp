/*****************************************************************
 * 주제: 2-3. C++ 동적 할당 (new & delete)
 * 작성일: 2026. 02. 23.
 * 설명: 
 * - C의 malloc/free를 대체하는 new/delete 연산자 학습
 * - Heap 메모리의 특성 및 메모리 해제의 중요성 이해
 * - 배열 할당 시 delete[]를 사용해야 하는 내부 메커니즘 파악
 *****************************************************************/
#include <iostream>

int main() {
    // 단일 데이터 동적 할당
    // int* ptr = (int*)malloc(sizeof(int)); // C 방식 (복잡함) // 
    int* ptr = new int;    // C++ 방식: new int라고 하면 알아서 int*타입을 반환! , (int*)같은 강제 형변환이 필요없음!
    *ptr = 100;

    std::cout << "값: " << *ptr << " | 주소: " << ptr << std::endl;

    int* ptr2 = new int(200);        // 할당과 동시에 초기화 - 할당과 동시에 값을 넣어
    std::cout << "초기화된 값: " << *ptr2 << std::endl;

    int len;                         // 배열 동적 할당
    std::cout << "할당할 배열의 길이는? ";
    std::cin >> len;

    int* arr = new int[len]; // 입력받은 크기만큼 배열 생성

    for (int i = 0; i < len; i++) {
        arr[i] = i + 1;
    }
    // 동적 할당을 할때 우리가 건드리는 메모리공간은 힙(heap)
    // 스택(stack) - 일반 변수들이 사는 곳. 함수 끝나면 자동으로 나감
    // 힙(heap) - new로 만든 데이터가 사는 곳. 우리가 delete 하기 전까지 절대로 나가지 않음
    // delete를 까먹으면 프로그램이 종료될 때까지 메모리를 계속 점유하는 메모리누수가 발생include <iostream>

int main() {
    // 단일 데이터 동적 할당
    // int* ptr = (int*)malloc(sizeof(int)); // C 방식 (복잡함) // 
    int* ptr = new int;    // C++ 방식: new int라고 하면 알아서 int*타입을 반환! , (int*)같은 강제 형변환이 필요없음!
    *ptr = 100;

    std::cout << "값: " << *ptr << " | 주소: " << ptr << std::endl;

    int* ptr2 = new int(200);        // 할당과 동시에 초기화 - 할당과 동시에 값을 넣어
    std::cout << "초기화된 값: " << *ptr2 << std::endl;

    int len;                         // 배열 동적 할당
    std::cout << "할당할 배열의 길이는? ";
    std::cin >> len;

    int* arr = new int[len]; // 입력받은 크기만큼 배열 생성

    for (int i = 0; i < len; i++) {
        arr[i] = i + 1;
    }
    // 동적 할당을 할때 우리가 건드리는 메모리공간은 힙(heap)
    // 스택(stack) - 일반 변수들이 사는 곳. 함수 끝나면 자동으로 나감
    // 힙(heap) - new로 만든 데이터가 사는 곳. 우리가 delete 하기 전까지 절대로 나가지 않음
    // delete를 까먹으면 프로그램이 종료될 때까지 메모리를 계속 점유하는 메모리누수가 발생
    // 메모리 해제
    delete ptr;        // 단일 할당 해제
    delete ptr2;
    delete[] arr;      // 배열 할당 해제는 반드시 []를 붙여야 함!
    // 배열이 delete[]를 써야하는 이유는 컴퓨터는 배열 할당 시 메모리 앞부분에 배열의 길이를 따로 기록해 두는데
    // delete[]를 써야만 이 정보를 확인하여 배열 전체의 메모리와 각 요소의 소멸자를 정확히 처리할 수 있기 때문임!!
    // - delete: 포인터가 가리키는 단 하나의 대상만 해제하려고 시도함!
    // - delete[]: 기록된 배열 길이를 참조하여 범위 전체를 해제하고, 객체일 경우 모든 요소의 소멸자를 호출
    // 그냥 delete를 쓰게 되면 배열의 첫 번째 요소만 해제되거나, 메모리 해제 정보가 일치하지 않아 런타임 에러가 발생할 수 있음!!!!
    //
    //new로 할당햇으면 반드시 delete 해제
    //new[]로 할당했으면 반드시 delete[] 해제
    //delete 후에도 포인터 변수에는 주소값이 남아있으므로, 안전을 위해 ptr = nullptr; 습관
    return 0;
}
