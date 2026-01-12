# v1
Aspen plus TEA 자동화 프로젝트입니다.

## 기간
2025.09.03 ~ 2026.01.10

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
- 입력파일은 aspen에서 뽑아낸 xlsx, rep파일 두 개이고, 이 두 파일을 input.xlsx, input.rep로 이름을 변경한 뒤 input 디렉토리에 넣은 뒤 실행시키면 루트에 output.xlsx파일이 생성됩니다.

## 개선 예정
- 에러가 발생할 수 있는 부분에 대해 시큐어 코딩을 진행할 예정입니다.
- 현재 한 파일에 함수가 너무 많아 파일 분리를 진행할 예정입니다.
- 객체지향으로 변경할 수 있는 부분은 리펙토링을 진행하여 변경하고 디자인 패턴 적용을 고려할 예정입니다.

## git branch 배우는 사이트
https://learngitbranching.js.org/?locale=ko
