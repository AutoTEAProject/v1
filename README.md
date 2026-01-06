# v1
Aspen plus TEA 자동화 프로젝트입니다.

## 기간
2025.09.03 ~ 현재.

## 빌드
```
git clone https://github.com/AutoTEAProject/v1.git
```

- 코드 변경 적용
```
git pull
```

- 초기 환경설정
```
pip install pandas
pip install openpyxl
```


## 사용 메뉴얼

[auto TEA 메뉴얼 노션 페이지](https://knowing-bagel-55f.notion.site/Auto-TEA-2aee8e10756f80348619e23ccc2213b9?source=copy_link)
- 해당 메뉴얼 페이지를 참고하여 사용해주세요.
- 현재 터미널에 입력해야하는 값은 reactor 가격입니다. -> 엑셀에서 입력하도록 수정 예정
- 또한 현재 프로그램을 처음 실행하면 파이썬 가상환경 경로 출력 메세지때문에 입력값이 멋대로 들어가는 버그가 있어서 처음 실행은 Ctrl + C로 중단시키고 두 번째 실행부터는 정상 동작하니 사용하시면 됩니다.
- 그리고 reactor의 equipment cost는 내부에서 계산하지 않고 가격만 USD단위로 입력받고 있습니다.
- 입력파일은 aspen에서 뽑아낸 xlsx, rep파일 두 개이고, 이 두 파일을 input.xlsx, input.rep로 이름을 변경한 뒤 input 디렉토리에 넣은 뒤 실행시키면 루트에 output.xlsx파일이 생성됩니다.

## 개선 예정

- reactor의 Equipment Cost를 엑셀로 따로 저장해서 읽어오도록 변경할 예정입니다.
- Parameters & Assumption를 엑셀로 따로 저장해서 읽어오도록 변경할 예정입니다.
- Equipment Cost 계산 파라미터를 쉽게 변경할 수 있도록 엑셀로 저장해서 읽어오도록 변경할 예정입니다.

## git branch 배우는 사이트
https://learngitbranching.js.org/?locale=ko
