#!/opt/anaconda3/envs/myenv/bin/python
from Parse import parseTEA, parseHEX, parseCOMP, parseCAPCOSTParam, parseUtility, parseLawMaterial, parseEQUIP, parseLawMaterialExcelData
from Utility import calEquipmentCost, printout, inputRTX
from Calc import calCAPEX, calUtility, calOPEX, calProfitAnalysis
from ExcelParse import parseUtilityParam, parseEquipmentParam
inputData = {}
inputfile = "./input/input.xlsx"
inputrep = "./input/input.rep"
lawMaterialData = {}
cost = {} # 2차원 딕셔너리로 "이름" : {딕셔너리} 이렇게 저장하고 각 유닛 종류별 인자와 계산 결과를 출력한다.
CAPEX = {}
OPEX = {}
utility =  {}
profitAnalysis = {}

try:
	parseUtilityParam()
	parseEquipmentParam() 
	parseLawMaterialExcelData()
	parseTEA(inputfile, inputData)
	parseEQUIP(inputrep, inputData)
	parseHEX(inputfile, inputData)
	parseCOMP(inputfile, inputData)
	parseCAPCOSTParam(inputrep, inputData)

except Exception as e:
	print("Error parsexlxs:", e)
try: 
	parseLawMaterial(inputrep, lawMaterialData) #KMOL/HR 단위로 추출  {'H2': -1841.32, 'N2': -613.773, 'NH3': 1227.55}
	parseUtility(inputData, inputrep, utility)
	calEquipmentCost(inputData, cost, utility)

except Exception as e:
	print("Error parserep:", e)

try:
	inputRTX(inputData, cost) # 여기서 reactor 엑셀에 입력하고 읽어오기
	calCAPEX(inputData, cost, CAPEX)
	calUtility(utility)
	calOPEX(CAPEX, lawMaterialData, OPEX, utility)
	calProfitAnalysis(CAPEX, OPEX, profitAnalysis, lawMaterialData)
	printout(inputData, cost, utility, CAPEX, OPEX, profitAnalysis)

except Exception as e:
	print("Error calc:", e)