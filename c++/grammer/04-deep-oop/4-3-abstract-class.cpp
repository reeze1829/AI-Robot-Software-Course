/*****************************************************************
 * 주제: 4-3. abstract-class (인터페이스 설계)
 * 작성일: 2026. 03. 11.
 * * [핵심 요약]
 * 1. 인터페이스 설계: 부모는 '버튼(함수 이름)'만 만들고, 실제 '동작'은 자식이 구현하게 강제함.
 * 2. 통합 제어: 부모 포인터 배열을 쓰면 서로 다른 가전제품도 하나의 리모컨으로 조작 가능함.
 * 3. 설계 표준: 구체적인 구현보다 추상적인 규격에 의존하여 코드의 확장성을 높임.
 *****************************************************************/

#include <iostream>
#include <string>

using namespace std;
// [비유: 리모컨 설계도]
// 이건 실제 리모컨이 아니라 "리모컨이라면 켜기/끄기 버튼은 있어야 한다"는 약속!!
// 버튼만 있고 전선은 연결 안 된 '껍데기'라서, 이걸로 직접 물건(객체)을 만들 순 없음
class IRemoteControl {
public:
    // [순수 가상 함수 = 0]
    // 부모는 어떻게 켜는지 모르니, 상속받는 자식이 무조건(강제로) 직접 구현해라라는 뜻임.
    virtual void turnOn() = 0;                 // 전원 켜기 규격
    virtual void turnOff() = 0;                // 전원 끄기 규격
    
    virtual ~IRemoteControl() {}               // 상속 관계이므로 가상 소멸자는 필수 안전장치
};

// [비유: 실제 TV 제작]
// 리모컨 설계도(부모)를 가져와서 실제로 화면을 띄우는 전선을 연결한 진짜 기기입니다.
class Television : public IRemoteControl {
public:
    // 부모가 강제한 turnOn을 TV 방식에 맞게 구현합니다.
    void turnOn() override { 
        cout << "TV: 전원이 켜지고 화면이 출력됩니다." << endl; 
    }
    void turnOff() override { 
        cout << "TV: 화면이 꺼지고 절전 모드로 들어갑니다." << endl; 
    }
};

// [비유: 실제 에어컨 제작]
// 똑같은 리모컨 설계도를 썼지만, 에어컨은 찬바람을 내뿜는 방식으로 기능을 구현함
class AirConditioner : public IRemoteControl {
public:
    // 부모가 강제한 turnOn을 에어컨 방식에 맞게 구현함!
    void turnOn() override { 
        cout << "에어컨: 실외기가 돌아가며 찬바람이 나옵니다." << endl; 
    }
    void turnOff() override { 
        cout << "에어컨: 작동을 멈추고 송풍 모드 후 종료됩니다." << endl; 
    }
};

int main() {
    // [비유: 통합 리모컨 관리]
    // 사용자는 이게 TV인지 에어컨인지 일일이 구분할 필요가 없음
    // '리모컨(부모 포인터)'만 있으면 어떤 기기든 똑같은 버튼으로 제어할 수 있음
    
    IRemoteControl* devices[2];        // 부모 타입의 포인터 배열 (통합 바구니)
    
    devices[0] = new Television();     // TV를 리모컨 바구니에 담기
    devices[1] = new AirConditioner(); // 에어컨을 리모컨 바구니에 담기

    cout << "가전제품 통합 제어 시작 " << endl;
    
    for (int i = 0; i < 2; i++) {
        // [다형성 실행] 
        // i가 0이면 TV의 turnOn, i가 1이면 에어컨의 turnOn이 자동으로 호출됨!
        devices[i]->turnOn(); 
    }

    cout << "\n모든 기기 종료" << endl;
    for (int i = 0; i < 2; i++) {
      delete devices[i]; 
    }

    return 0;
}
/*
 * 1. 인터페이스 명명 규칙: C++에서는 인터페이스 역할을 하는 클래스 이름 앞에 
 * 'I'(Interface)를 붙이는 관례가 있음 (예: IRemoteControl)
 * 2. 추상 클래스의 제약: 순수 가상 함수가 하나라도 있으면 'new IRemoteControl()'처럼 
 * 직접 객체를 생성할 수 없음 (설계도일 뿐이라서)
 * 3. 확장성: 나중에 '세탁기' 클래스가 추가되어도 main 함수의 제어 로직은 
 * 수정할 필요가 없음. 이것이 객체지향 설계의 강력함!!!
 */
