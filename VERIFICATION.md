# 검증 결과

검증일: 2026-10-28 (Asia/Seoul)

환경: Windows, Python 3.14.7, 설치된 pico2d 및 transitions 사용.

## 자동 검증

`python -m unittest -v test_boy` — **11개 테스트 통과**.

- IDLE 위치 유지와 시간 기반 애니메이션
- 일반 RUN 이동 및 키 해제 후 IDLE
- 양방향 동시 입력과 한쪽 해제
- a 키 진입, a 키 해제 후 자동 이동, 일반 속도의 2배
- 현재 바라보는 방향으로 자동 이동
- 확대 크기, 발 높이 유지, 취소 후 일반 크기 복원
- 좌우 벽 반사 및 확대 상태 진입 시 경계 보정
- 벽 반사 및 a 재입력으로 타이머가 연장되지 않음, 정확히 5초에 IDLE
- 양쪽 방향키 취소, 일반 RUN 속도 복원, 해제 후 IDLE
- RUN에서 a 입력 무시
- 긴 프레임에서도 화면 내부 위치 유지

시간은 모의 monotonic 시계로 제어하고, 이미지 객체는 대체 객체를 사용했습니다.
크기 검증은 실제 draw 함수에 전달되는 인수를 확인합니다.

`python -m compileall -q boy.py grass.py main.py test_boy.py` — **통과**.

## 실제 SDL 이미지·렌더링 확인

SDL dummy 비디오 드라이버와 명시적으로 생성한 software renderer로
800×600 캔버스를 열고, 실제 소년 이미지 2개와 잔디 이미지를 로딩했습니다.
잔디와 IDLE, AutoRun, RUN의 draw 호출 및 화면 갱신·종료가 **통과**했습니다.

기본 dummy 드라이버에서는 pico2d의 accelerated renderer 생성 후 이미지 로딩이
실패했습니다. 검증용으로 software renderer를 명시하면 정상 동작했습니다.
게임 소스의 렌더러 설정은 변경하지 않았습니다.

## 남은 수동 확인

실제 데스크톱 창에서 키보드 조작과 애니메이션의 시각적 품질은 수동 확인이 필요합니다.
GitHub 업로드 및 e-Class 제출은 수행하지 않았습니다.
