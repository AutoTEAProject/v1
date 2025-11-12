# v1
Aspen plus TEA 자동화 프로젝트입니다.

## 빌드
```
git clone
```

## 사용 메뉴얼
- 현재 raw material에 대한 데이터가 상당히 부족합니다. 데이터에 없는 물질이 들어오면 에러가 발생하는데 해당 물질에 대한 데이터를 parse/Calc.py파일의 lawMaterialCostData, lawMaterialWeightData 딕셔너리에 추가하면 됩니다.
- 또한 현재 프로그램을 처음 실행하면 파이썬 가상환경 경로 출력 메세지때문에 입력값이 멋대로 들어가는 버그가 있어서 처음 실행은 Ctrl + C로 중단시키고 두 번째 실행부터는 정상 동작하니 사용하시면 됩니다.
- 현재 해당 물질이 반응물 또는 생성물이 맞는지 입력받습니다. y 또는 n으로 답변
- 그리고 reactor의 equipment cost는 내부에서 계산하지 않고 가격만 USD단위로 입력받고 있습니다.

## 개선 예정
- raw Material data를 입력이 쉽게 파일로 따로 저장해서 읽어오도록 변경할 예정입니다.
- reactor의 Equipment Cost를 파일로 따로 저장해서 읽어오도록 변경할 예정입니다.
- Parameters & Assumption를 파일로 따로 저장해서 읽어오도록 변경할 예정입니다.
- Equipment Cost 계산 파라미터를 쉽게 변경할 수 있도록 파일로 저장해서 읽어오도록 변경할 예정입니다.
- Aspen에서 계산되어있는 Equipment cost가 있는 경우 해당 값을 우선으로 사용하도록 변경할 예정입니다.
