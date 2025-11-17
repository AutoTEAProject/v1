#!/opt/anaconda3/envs/myenv/bin/python
from Parse import parseTEA, parseHEX, parseCOMP, parseCAPCOSTParam, parseUtility, parseLawMaterial
from Utility import calEquipmentCost, printout, inputRTX
from Calc import calCAPEX, calUtility, calOPEX, calProfitAnalysis

inputData = []
inputfile = "./input/input.xlsx"
inputrep = "./input/input.rep"
lawMaterialData = {}
cost = {} # 2차원 딕셔너리로 "이름" : {딕셔너리} 이렇게 저장하고 각 유닛 종류별 인자와 계산 결과를 출력한다.
CAPEX = {}
OPEX = {}
utility =  {}
profitAnalysis = {}
# 이거 가능한 많이 파일로 빼자~
try: 
	parseTEA(inputfile, inputData)
	parseHEX(inputfile, inputData)
	parseCOMP(inputfile, inputData)
	parseCAPCOSTParam(inputrep, inputData)

	parseLawMaterial(inputrep, lawMaterialData) #KMOL/HR 단위로 추출  {'H2': -1841.32, 'N2': -613.773, 'NH3': 1227.55}
	parseUtility(inputrep, utility)
	calEquipmentCost(inputData, cost, utility)


	# 이제 여기서 Capacity 값 각 모듈별로 파싱해서 저장해둬야함.
	inputRTX(cost)

	calCAPEX(cost, CAPEX)
	calUtility(utility)
	calOPEX(CAPEX, lawMaterialData, OPEX, utility)
	calProfitAnalysis(CAPEX, OPEX, profitAnalysis, lawMaterialData)
	#이제 예쁘게 출력만 하면 완성이다~
	printout(inputData, cost, utility, CAPEX, OPEX, profitAnalysis)

except Exception as e:
	print("Error occurred:", e)