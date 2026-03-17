/*****************************************************************
 * 주제: 5-2. vector-container (동적 배열 std::vector)
 * 작성일: 2026. 03. 17.
 * [5-2. 핵심 요약]
 * 1. std::vector: 크기가 자동으로 조절되는 동적 배열 (가장 범용적인 컨테이너).
 * 2. 편리함: 메모리 관리(new/delete)를 직접 하지 않아도 되어 안전함.
 * 3. 효율성: 연속된 메모리 공간을 사용하여 데이터 접근 속도가 매우 빠름.
 *****************************************************************/

#include <iostream>
#include <vector>   // vector를 쓰기 위해 필수 포함
#include <string>

using namespace std;

int main() {
    // 선언 
    // 템플릿 클래스이므로 <int>처럼 저장할 데이터 타입을 명시해야 함.
    vector<int> vec;                        // 비어있는 정수형 벡터 생성

    // push_back: 데이터 추가 (뒤에서부터 차곡차곡)
    // 맨 뒤에 데이터를 추가함. 공간이 부족하면 내부적으로 메모리를 재할당함
    vec.push_back(10);
    vec.push_back(20);
    vec.push_back(30);

    // 데이터 접근 (일반 배열처럼 [] 사용 가능)
    // 일반 배열과 동일하게 [ ] 연산자로 특정 위치의 데이터에 즉시 접근 가능 (시간 복잡도: O(1))
    cout << "첫 번째 요소: " << vec[0] << endl;
    
    // size(): 요소 개수 확인
    // 현재 벡터에 실제로 저장된 데이터의 개수를 반환함
    cout << "벡터의 현재 크기: " << vec.size() << endl;

    // 반복문을 이용한 출력
    cout << "전체 요소 출력: ";
    for (int i = 0; i < vec.size(); i++) {
        cout << vec[i] << " ";
    }
    cout << endl;

    // pop_back: 데이터 삭제
    // 맨 뒤의 요소를 제거함. 메모리 공간은 유지하되 저장된 값만 날림
    vec.pop_back(); 
    
    // 범위 기반 for문, 컨테이너의 시작부터 끝까지 안전하게 순회함
    cout << "삭제 후 요소: ";
    for (int n : vec) {
        cout << n << " ";
    }
    cout << endl;

    // empty() & clear() 데이터 전부 비우기
    // clear()는 모든 요소를 제거하여 size를 0으로 만듦.
    vec.clear();
    if (vec.empty()) {      // 데이터가 하나도 없으면 true 반환
        cout << "벡터가 비어있습니다." << endl;
    }

    return 0;
}

/*
 * [기술적 원리 메모]
 * 1. 동적 할당: 내부적으로는 new/delete를 통해 크기를 늘리거나 줄임
 * 2. 연속 메모리: 일반 배열처럼 메모리가 붙어 있어 인덱스([]) 접근이 O(1)로 매우 빠름
 * 3. 가용량(Capacity): 데이터가 꽉 차면 메모리 공간을 약 1.5~2배로 자동 확장
 *  Size vs Capacity:
 * - Size: 실제로 들어있는 데이터 개수
 * - Capacity: 재할당 없이 담을 수 있는 최대 공간 (Size가 이걸 넘어서면 메모리를 새로 할당함)
 *  RAII(Resource Acquisition Is Initialization):
 *  - vector 객체가 소멸될 때(함수가 끝날 때 등) 내부에서 할당했던 메모리도 자동으로 delete됨
 *  복사 비용:
 * - 함수 인자로 넘길 때 'vector<int> v'처럼 받으면 전체 데이터가 복사되므로, 보통 const vector<int>& v처럼 참조형을 써서 메모리를 아낌
 */






