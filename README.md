# DRILL_11 — AutoRun

pico2d 소년 캐릭터의 IDLE, RUN, AutoRun 상태 전환 과제입니다.

## 실행

```powershell
python -m pip install -r requirements.txt
python main.py
```

Python과 SDL을 사용할 수 있는 데스크톱 환경이 필요합니다. 기본 화면은 800×600입니다.

## 조작과 동작

| 입력 | 동작 |
| --- | --- |
| ← / → | 일반 달리기: 초당 200px, 표시 크기 100×100 |
| 방향키 해제 | 이동 입력이 없으면 IDLE |
| IDLE에서 a | 현재 바라보는 방향으로 AutoRun |
| AutoRun 중 ← / → | 즉시 취소하고 누른 방향으로 일반 RUN |
| Esc / 창 닫기 | 종료 |

AutoRun은 별도 클래스로 구현했습니다. 키를 놓아도 초당 400px로 이동하며,
150×150 크기로 표시합니다. 확대해도 발의 높이를 유지합니다.
캐릭터 전체가 화면 안에 있도록 좌우 경계에서 반사 이동하고,
진입 후 5초가 되면 현재 위치에서 IDLE로 돌아옵니다.
벽 반사와 a 재입력은 제한 시간을 연장하지 않습니다.
종료 후 일반 크기와 속도를 사용합니다. SLEEP 상태는 사용하지 않습니다.

## 검증

```powershell
python -m unittest -v test_boy
python -m compileall -q boy.py grass.py main.py test_boy.py
```

실제 수행 결과와 검증 범위는 [VERIFICATION.md](VERIFICATION.md)에 기록했습니다.
요구사항은 [PRD.md](PRD.md)를 참고하세요.
