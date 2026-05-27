#!/opt/anaconda3/envs/myenv/bin/python
from Parse import parseTEA, parseHEX, parseCOMP, parseCAPCOSTParam, parseUtility, parseLawMaterial, parseEQUIP, parseLawMaterialExcelData, parseFlowData, parseMPSG, parseMPS , parseReactor
from Utility import calEquipmentCost, printout, inputRTX
from Calc import calCAPEX, calUtility, calOPEX, calProfitAnalysis
from ExcelParse import parseUtilityParam, parseEquipmentParam, parsereactorParam
from data import calcOPEXdata, reactorParam

inputData = {}
inputfile = "./input/input.xlsx"
inputrep = "./input/input.rep"
lawMaterialData = {}
cost = {} # 2차원 딕셔너리로 "이름" : {딕셔너리} 이렇게 저장하고 각 유닛 종류별 인자와 계산 결과를 출력한다.
CAPEX = {}
OPEX = {}
utility =  {}
profitAnalysis = {}
flowData = {}
exceptUtility = []
exceptEquipmentcost = []
exceptCapacity = {}
try:
	parseUtilityParam()
	parseEquipmentParam() 
	parsereactorParam()
	parseLawMaterialExcelData(flowData, exceptEquipmentcost, exceptUtility, exceptCapacity, )
except Exception as e:
	print("Error parsexlxs:", e)
try: 
	parseTEA(inputfile, inputData)
	parseEQUIP(inputrep, inputData)
	parseHEX(inputfile, inputData)
	parseCOMP(inputfile, inputData)
	parseCAPCOSTParam(inputrep, inputData)
	parseUtility(inputData, inputrep, utility, exceptCapacity)
	parseMPSG(inputData, inputrep, utility)
	parseMPS(inputData, inputrep, utility)
	parseReactor(inputData, inputrep, utility)

except Exception as e:
	print("Error parserep:", e)

try:
	calEquipmentCost(inputData, cost, utility, exceptCapacity)
	# inputRTX(inputData, cost) # 여기서 reactor 엑셀에 입력하고 읽어오기
	calCAPEX(inputData, cost, CAPEX, exceptEquipmentcost)
	calUtility(utility, exceptUtility)
	calOPEX(CAPEX, flowData, OPEX, utility)
	calProfitAnalysis(CAPEX, OPEX, profitAnalysis, flowData)
	printout(inputData, cost, utility, CAPEX, OPEX, profitAnalysis)

except Exception as e:
	print("Error calc:", e)