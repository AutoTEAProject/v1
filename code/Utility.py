import math
from copy import deepcopy
from enums import Index
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font
from data import HeaterParam, HeatExchangerParam, CompressorParam, ReactParam

def checkType(name):
	length = len(name)
	NGLen = 2
	HTXLen = 3
	HEXLen = 3
	SEPLen = 3
	MIXLen = 3
	PFRLen = 3
	COMPLen = 4
	COOLLen = 4
	SPFRLen = 4
	DISTLen = 4
	REACTLen = 5
	FLASHLen = 5
	VALVELen = 5
	SPLITLen = 5
	
	for i in range(0, length):
		if (length - i >= NGLen and name[i:i + NGLen] == "NG"):
			return "HTX"
		if (length - i >= HTXLen and name[i:i + HTXLen] == "HTX"):
			return "HTX"
		elif (length - i >= SEPLen and name[i:i + SEPLen] == "SEP"):
			return "SEP"
		elif (length - i >= HEXLen and name[i:i + HEXLen] == "HEX"):
			return "HEX"
		elif (length - i >= MIXLen and name[i:i + MIXLen] == "MIX"):
			return "MIX"
		elif (length - i >= PFRLen and name[i:i + PFRLen] == "PFR"):
			return "REACT"
		elif (length - i >= COMPLen and name[i:i + COMPLen] == "COMP"):
			return "COMP"
		elif (length - i >= COOLLen and name[i:i + COOLLen] == "COOL"):
			return "COOL" 
		elif (length - i >= SPFRLen and name[i:i + SPFRLen] == "SPFR"):
			return "REACT"
		elif (length - i >= DISTLen and name[i:i + DISTLen] == "DIST"):
			return "DIST"
		elif (length - i >= REACTLen and name[i:i + REACTLen] == "REACT"):
			return "REACT"
		elif (length - i >= FLASHLen and name[i:i + FLASHLen] == "FLASH"):
			return "FLASH"
		elif (length - i >= VALVELen and name[i:i + VALVELen] == "VALVE"):
			return "MIX"
		elif (length - i >= SPLITLen and name[i:i + SPLITLen] == "SPLIT"):
			return "MIX"
	# print(name)

# cost = {} # 2차원 딕셔너리로 "이름" : {딕셔너리} 이렇게 저장하고 각 유닛 종류별 인자와 계산 결과를 출력한다.
def calEquipmentCost(inputData, cost, utility): #react도 추가해야함.
	for i in range(0, len(inputData), 1):
		temp = {}
		type = checkType(inputData[i][Index.NameIdx])

 		# 여기서 이제 cost의 값들을 하나씩 이름, 인자 순으로 저장해야함.
		'''
		1. EQUIPMENT COST
		- HEX, HTX : ((10^(K1+K2+K3))*(Capacity / 10)^(0.6)) * (CEPCI(June 2024) / CEPCI(Sept 2001))
		- COMP : (10^(K1 + K2 * log(Capacity) + K3 * ((log(Capacity))^2))) * (CEPCI(June 2024) / CEPCI(Sept 2001))
		2. C_BM 
		- HEX, HTX : EQUIPMENT COST * (B1 + B2*FM)
		'''
		if (type == "HTX"):
			if ("HOT UTILITY[kW]" in utility[inputData[i][Index.NameIdx]]):
				utilityKey = "HOT UTILITY[kW]"
			elif ("ELECTRICITY UTILITY[kW]" in utility[inputData[i][Index.NameIdx]]):
				utilityKey = "ELECTRICITY UTILITY[kW]"
			else:
				utilityKey = "COOLING UTILITY[kg/hr]"
			if(utility[inputData[i][Index.NameIdx]][utilityKey] < 0):
				# error 이거 어떻게 처리해야하는거지?
				# 이거 cooler라서 양수 전환해서 계산해야함
				continue
			temp["Diphenyl heater"] = deepcopy(HeaterParam["Diphenyl heater"])
			temp["Diphenyl heater"]["EQUIPMENT COST"] = ((10**(temp["Diphenyl heater"]["K1"]+temp["Diphenyl heater"]["K2"]+temp["Diphenyl heater"]["K3"]))*(utility[inputData[i][Index.NameIdx]][utilityKey] / 10)**(0.6)) * (798.8 / 397)
			
			temp["Molten salt heater"] = deepcopy(HeaterParam["Molten salt heater"])
			temp["Molten salt heater"]["EQUIPMENT COST"] = ((10**(temp["Molten salt heater"]["K1"]+temp["Molten salt heater"]["K2"]+temp["Molten salt heater"]["K3"]))*(utility[inputData[i][Index.NameIdx]][utilityKey] / 10)**(0.6)) * (798.8 / 397)
			
			temp["Hot water heater"] = deepcopy(HeaterParam["Hot water heater"])
			temp["Hot water heater"]["EQUIPMENT COST"] = ((10**(temp["Hot water heater"]["K1"]+temp["Hot water heater"]["K2"]+temp["Hot water heater"]["K3"]))*(utility[inputData[i][Index.NameIdx]][utilityKey] / 10)**(0.6)) * (798.8 / 397)
			
			temp["Steam boiler"] = deepcopy(HeaterParam["Steam boiler"])
			temp["Steam boiler"]["EQUIPMENT COST"] = ((10**(temp["Steam boiler"]["K1"]+temp["Steam boiler"]["K2"]+temp["Steam boiler"]["K3"]))*(utility[inputData[i][Index.NameIdx]][utilityKey] / 10)**(0.6)) * (798.8 / 397)
		elif (type == "HEX"):
			temp["Fixed tube"] = deepcopy(HeatExchangerParam["Fixed tube"])
			temp["Fixed tube"]["EQUIPMENT COST"] = ((10**(temp["Fixed tube"]["K1"]+temp["Fixed tube"]["K2"]+temp["Fixed tube"]["K3"]))*(inputData[i][Index.HeatTransferAreaIdx] / 10)**(0.6)) * (798.8 / 397)
			
			temp["Floating head"] = deepcopy(HeatExchangerParam["Floating head"])
			temp["Floating head"]["EQUIPMENT COST"] = ((10**(temp["Floating head"]["K1"]+temp["Floating head"]["K2"]+temp["Floating head"]["K3"]))*(inputData[i][Index.HeatTransferAreaIdx] / 10)**(0.6)) * (798.8 / 397)
			
			temp["U-tube"] = deepcopy(HeatExchangerParam["U-tube"])
			temp["U-tube"]["EQUIPMENT COST"] = ((10**(temp["U-tube"]["K1"]+temp["U-tube"]["K2"]+temp["U-tube"]["K3"]))*(inputData[i][Index.HeatTransferAreaIdx] / 10)**(0.6)) * (798.8 / 397)
			
			temp["Bayonet"] = deepcopy(HeatExchangerParam["Bayonet"])
			temp["Bayonet"]["EQUIPMENT COST"] = ((10**(temp["Bayonet"]["K1"]+temp["Bayonet"]["K2"]+temp["Bayonet"]["K3"]))*(inputData[i][Index.HeatTransferAreaIdx] / 10)**(0.6)) * (798.8 / 397)
		elif (type == "COMP"):
			temp["Centrifugal, axial and reciprocating"] = deepcopy(CompressorParam["Centrifugal, axial and reciprocating"])
			if (inputData[i][Index.DriverPowerIdx] == 0):
				continue
				#error
				# 나중에 여기에 에러 처리 코드 넣기
			temp["Centrifugal, axial and reciprocating"]["EQUIPMENT COST"] = (10**(temp["Centrifugal, axial and reciprocating"]["K1"] + temp["Centrifugal, axial and reciprocating"]["K2"] * (math.log(inputData[i][Index.DriverPowerIdx], 10)) + (temp["Centrifugal, axial and reciprocating"]["K3"] * ((math.log(inputData[i][Index.DriverPowerIdx], 10))**2)))) * (798.8 / 397)
			temp["Rotary"] = deepcopy(CompressorParam["Rotary"])
			temp["Rotary"]["EQUIPMENT COST"] = (10**(temp["Rotary"]["K1"] + temp["Rotary"]["K2"] * (math.log(inputData[i][Index.DriverPowerIdx], 10)) + (temp["Rotary"]["K3"] * ((math.log(inputData[i][Index.DriverPowerIdx], 10))**2)))) * (798.8 / 397)
		elif (type == "REACT"):
			temp["input"] = deepcopy(ReactParam["Nan"])
			temp["input"]["EQUIPMENT COST"] = 0
		# 여기는 이미 가격 계산 되어있으면 계산 안 하는 부분
		if (inputData[i][Index.EquipmentCostIdx] != 0): 
			temp["ATEA"] = {}
			temp["ATEA"]["EQUIPMENT COST"] = inputData[i][Index.EquipmentCostIdx]
		cost[inputData[i][Index.NameIdx]] = deepcopy(temp)
	 
# 이제 여기서 Capacity 값은 각 모듈별로 파싱해서 저장해둬야함.
def safe_df(df):
    # 인덱스가 RangeIndex(0,1,2,...)가 아니거나, 인덱스 이름이 있다면 컬럼으로 복구
    if not isinstance(df.index, pd.RangeIndex) or df.index.name is not None:
        return df.reset_index()
    return df

def write_block(ws, df, title):
    ws.append([title])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True, color="004085")
    for r in dataframe_to_rows(df, index=True, header=True):
        ws.append(r)
    ws.append([])

def autofit(ws):
    for col in ws.columns:
        max_len = max((len(str(cell.value)) if cell.value else 0) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 60)

def printout(inputData, cost, utility, CAPEX, OPEX, profitAnalysis):
    parse_out = pd.DataFrame(inputData)
    parse_out.columns = ["Name","EquipmentCost","InstalledCost","EquipmentWeight",
                         "InstalledWeight","UtilityCost","HeatTransferArea","DriverPower"]
    wb = Workbook()

    # 시트 1: parse
    ws1 = wb.active
    ws1.title = "parse"
    for r in dataframe_to_rows(parse_out, index=False, header=True): ws1.append(r)

    # 시트 2: UTILITY
    ws2 = wb.create_sheet("UTILITY")
    for r in dataframe_to_rows(pd.DataFrame(utility), header=True): ws2.append(r)

    # 시트 3: CAPCOST (블럭 스타일)
    ws3 = wb.create_sheet("Equipment Cost")
    for k,v in cost.items():
        df = pd.DataFrame(v).T   # 행열 전치 추가!
        write_block(ws3, df, k)
    autofit(ws3)

    # 시트 4: CAPEX  —— 스칼라 dict이면 리스트로 감싸서 1-row DF
    ws4 = wb.create_sheet("CAPEX")
    capex_df = pd.DataFrame([CAPEX]).T if isinstance(CAPEX, dict) else pd.DataFrame(CAPEX).T
    for r in dataframe_to_rows(capex_df, header=False):
        ws4.append(r)
    autofit(ws4)

    # 시트 5: OPEX
    ws5 = wb.create_sheet("OPEX")
    opex_df = pd.DataFrame([OPEX]).T  if isinstance(OPEX, dict) else pd.DataFrame(OPEX).T 
    for r in dataframe_to_rows(opex_df, header=False):
        ws5.append(r)
    autofit(ws5)
    
    ws6 = wb.create_sheet("Profitability Analysis")
    opex_df = pd.DataFrame([profitAnalysis]).T  if isinstance(profitAnalysis, dict) else pd.DataFrame(profitAnalysis).T 
    for r in dataframe_to_rows(opex_df, header=False):
        ws6.append(r)
    autofit(ws6)
    
    # 마지막에 한 번만 저장
    wb.save("output.xlsx")

def inputRTX(inputData):
	for key in inputData:
		if (checkType(key) == "REACT"):
			print("Enter the equipment cost for reactor [USD]", key, ": ", end='')
			inputData[key]["input"]["EQUIPMENT COST"] = input()
			
