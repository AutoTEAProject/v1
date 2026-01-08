from Utility import checkType
from data import lawMaterialCostData, lawMaterialWeightData, utilityCostData, calcOPEXdata, profitAnalysisData, outputFlowData
from enums import Index

def calCAPEX(inputData, cost, CAPEX):
	#CAPEX 출력 순서 지정을 위한 전방선언
	CAPEX["CAPEX"] = ["  ", "  "]
	CAPEX[" "] = ["  ", "  "]
	CAPEX["CLASSIFICATION"] = ["% of FCI", "[USD/yr]"]
	CAPEX[" "] = ["  ", "  "]
	CAPEX["Direct cost"] = ["  ", "  "]
	CAPEX["ISBL (Inside battery limit, 전체공사구역 중 주 공정시설)"] = ["  ", "  "]
	CAPEX["Equipment cost"] = ["20-40", 0]
	CAPEX["Installation of equipment "] = ["7.3-26"]
	CAPEX["Instrument and control"] = ["2.5-7.0"]
	CAPEX["Piping"] = ["3.0-15"]
	CAPEX["Electrical"] = ["2.5-9.0"]
	CAPEX["  "] = ["  ", "  "]
 
	CAPEX["OSBL(Outside bettery limit,주공정시설 외 부대시설)"] = ["  ", "  "]
	CAPEX["Building and building services"] = ["6.0-20"]
	CAPEX["Yard improvements"] = ["1.5-5.0"]
	CAPEX["Services facilities"] = ["8.0-35"]
	CAPEX["Land"] = ["1.0-2.0"]
	CAPEX[" "] = ["  ", "  "]

	CAPEX["Total direct cost"] = ["  "]
	CAPEX["   "] = ["  ", "  "]

	CAPEX["Indirect cost"] = ["  ", "  "]
	CAPEX["Engineering"] = ["4.0-21"]
	CAPEX["Construction expenses"] = ["4.8-22"]
	CAPEX["Contractor's fee"] = ["1.5-5.0"]
	CAPEX["Contingency"] = ["5.0-20"]
	CAPEX["    "] = ["  ", "  "]
 
	CAPEX["Total indirect cost"] = ["  "]
	CAPEX["     "] = ["  ", "  "]
 
	CAPEX["Fixed capital investment (FCI)"] = ["100"]
	CAPEX["Start up cost (SUC)"] = ["10"]
	CAPEX["      "] = ["  ", "  "]
 
	CAPEX["Total capital investment (Capex)"] = ["TCI"]
	CAPEX["Annualized capital cost (r=5%, t=30 year)"] = ["EAC", 0]

	for key in cost:
		if ("ATEA" in cost[key]):
			CAPEX["Equipment cost"][1] += int(cost[key]["ATEA"]["EQUIPMENT COST"])
			# print("error")
			continue;
		if (inputData[key]["Type"] == "REACT"):
			CAPEX["Equipment cost"][1] += int(cost[key]["input"]["EQUIPMENT COST"])
		elif(inputData[key]["Type"] == "HEX"):
			CAPEX["Equipment cost"][1] += int(cost[key]["U-tube"]["EQUIPMENT COST"])
		elif(inputData[key]["Type"] == "HTX"):
			CAPEX["Equipment cost"][1] += int(cost[key]["Hot water heater"]["EQUIPMENT COST"])
		elif(inputData[key]["Type"] == "COMP"):
			CAPEX["Equipment cost"][1] += int(cost[key]["Centrifugal, axial and reciprocating"]["EQUIPMENT COST"])
		elif(inputData[key]["Type"] == "FLASH"):
			CAPEX["Equipment cost"][1] += int(cost[key]["ATEA"]["EQUIPMENT COST"])
	CAPEX["Fixed capital investment (FCI)"].append(CAPEX["Equipment cost"][1] * 100 / 40)
	CAPEX["Start up cost (SUC)"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.1)

	CAPEX["Installation of equipment "].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.08)
	CAPEX["Instrument and control"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.05)
	CAPEX["Piping"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.03)
	CAPEX["Electrical"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.05)
	
	CAPEX["Building and building services"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.07)
	CAPEX["Yard improvements"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.02)
	CAPEX["Services facilities"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.08)
	CAPEX["Land"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.02)
 
	CAPEX["Total direct cost"].append(CAPEX["Equipment cost"][1] + CAPEX["Installation of equipment "][1] + CAPEX["Instrument and control"][1] + CAPEX["Piping"][1] + CAPEX["Electrical"][1] + CAPEX["Building and building services"][1] + CAPEX["Yard improvements"][1] + CAPEX["Services facilities"][1] + CAPEX["Land"][1])
 
	CAPEX["Engineering"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.05)
	CAPEX["Construction expenses"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.05)
	CAPEX["Contractor's fee"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.05)
	CAPEX["Contingency"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.05)

	CAPEX["Total indirect cost"].append(CAPEX["Engineering"][1] + CAPEX["Construction expenses"][1] + CAPEX["Contractor's fee"][1] + CAPEX["Contingency"][1])
	
	CAPEX["Total capital investment (Capex)"].append(CAPEX["Start up cost (SUC)"][1] + CAPEX["Fixed capital investment (FCI)"][1])
	CAPEX["Annualized capital cost (r=5%, t=30 year)"][1] = (CAPEX["Total capital investment (Capex)"][1] / ((1 - (1 / ((1.05)**30)))/0.05))

def calUtility(utility):
	for key in utility:
		if "COOLING UTILITY[kg/hr]" in utility[key]:
			usage = utility[key]["COOLING UTILITY[kg/hr]"]
			if (usage < 0):
				usage = -1 * usage
			annualUsage = usage * calcOPEXdata["plantOperationHours"] #kg/year
			utility[key]["COOLING UTILITY ANNUAL USAGE [kg/year]"] = int(annualUsage)
			utilityCost = usage * utilityCostData["CoolingWaterPrice"] #USD/hr
			utility[key]["COOLING UTILITY UTILITY COST [USD/hr]"] = int(utilityCost)
			annualCost = utilityCost * calcOPEXdata["plantOperationHours"] #USD/year
			utility[key]["COOLING UTILITY ANNUAL COST [USD/year]"] = int(annualCost)

		if "HOT UTILITY[kW]" in utility[key]:
			duty = utility[key]["HOT UTILITY[kW]"]
			if (duty < 0):
				duty = -1 * duty
			annualDuty = duty * calcOPEXdata["plantOperationHours"] #kWh/year
			utility[key]["HOT UTILITY ANNUAL DUTY [kWh/year]"] = int(annualDuty)
			annualCost = annualDuty * utilityCostData["NGprice"]  #USD/year
			utility[key]["HOT UTILITY ANNUAL COST [USD/year]"] = int(annualCost)

		if "ELECTRICITY UTILITY[kW]" in utility[key]:
			usage = utility[key]["ELECTRICITY UTILITY[kW]"]
			annualUsage = usage * calcOPEXdata["plantOperationHours"] #kWh/year
			utility[key]["ELECTRICITY UTILITY ANNUAL USAGE [kWh/year]"] = int(annualUsage)
			annualCost = annualUsage * utilityCostData["electricityCostPerKWH"] #USD/year
			utility[key]["ELECTRICITY UTILITY ANNUAL COST [USD/year]"] = int(annualCost)


def calOPEX(CAPEX, lawMaterialData, OPEX, utility):

	#OPEX 출력 순서 지정을 위한 전방선언
	OPEX["OPEX (Total product costm TPC)"] = [" " ," "]
	OPEX[" "] = [" " ," "]
	OPEX["CLASSIFICATION"] = ["(REF Range)", "[USD/yr]"]
	OPEX[" "] = [" " ," "]
	OPEX["Fixed charge(FC)"] = [" "]
	OPEX["Local taxes, Insurance"] = ["1~4% of FCI"]
	OPEX[" "] = [" " ," "]
 
	OPEX["Direct production cost (DPC)"] = [" "]
	OPEX["Raw materials"] = [" "]
	OPEX["Utility"] = [" "]
	OPEX["Matinenenance (M)"] = ["1~10% of FCI"]
	OPEX["Operating labor (OL)"] = ["10~20% of OPEX"]
	OPEX["Supervision and support labor (S)"] = ["30 or 15(peter)% of OL"]
	OPEX["Operating supplies"] = ["10~20% of M"]
	OPEX["Laboratory charges"] = ["10~20% of OL"]
	OPEX["  "] = [" " ," "]
 
	OPEX["Plant overhead cost(OVHD)"] = ["50~70% of M+OL+S"]
	OPEX["   "] = [" " ," "]
 
	OPEX["General expenses"] = [" "]
	OPEX["Admistrative cost"] = ["15~20% of OL"]
	OPEX["Distribution and marketing"] = ["2~20% of OPEX"]
	OPEX["R&D cost"] = ["2~5% of OPEX"]
 
	OPEX["    "] = [" " ," "]
	OPEX["OPEX"] = [" "]

	OPEX["Fixed charge(FC)"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.01)
	OPEX["Local taxes, Insurance"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.01)

	OPEX["Raw materials"] = [" ", 0] # 이거 raw material key에 따른 알맞은 값 넣어야함.
	for key in lawMaterialData:
		if lawMaterialData[key] < 0:
			OPEX["Raw materials"][1] += lawMaterialData[key] * lawMaterialCostData[key] * calcOPEXdata["plantOperationHours"] * -1 * lawMaterialWeightData[key]  # kg 단위로 바꿔주기 위해 1000으로 나눔
	OPEX["Utility"] = [" ", 0]
	for key in utility:
		if "ELECTRICITY UTILITY ANNUAL COST [USD/year]" in utility[key] and utility[key]["ELECTRICITY UTILITY ANNUAL COST [USD/year]"] > 0:
			OPEX["Utility"][1] += utility[key]["ELECTRICITY UTILITY ANNUAL COST [USD/year]"]
		if "COOLING UTILITY ANNUAL COST [USD/year]" in utility[key] and utility[key]["COOLING UTILITY ANNUAL COST [USD/year]"] > 0:
			OPEX["Utility"][1] += utility[key]["COOLING UTILITY ANNUAL COST [USD/year]"]
		if "HOT UTILITY ANNUAL COST [USD/year]" in utility[key] and utility[key]["HOT UTILITY ANNUAL COST [USD/year]"] > 0:
			OPEX["Utility"][1] += utility[key]["HOT UTILITY ANNUAL COST [USD/year]"]

	OPEX["Matinenenance (M)"].append(CAPEX["Fixed capital investment (FCI)"][1] * 0.01)
	OPEX["Operating supplies"].append(OPEX["Matinenenance (M)"][1] * 0.1)



	OPEX["OPEX"].append(1.35135135135 * (CAPEX["Fixed capital investment (FCI)"][1] * 0.026 + (OPEX["Utility"][1] + OPEX["Raw materials"][1])))
	OPEX["Operating labor (OL)"].append(OPEX["OPEX"][1] * 0.1)
	OPEX["Supervision and support labor (S)"].append(OPEX["Operating labor (OL)"][1] * 0.3)
	OPEX["Laboratory charges"].append(OPEX["Operating labor (OL)"][1] * 0.1)
	OPEX["Plant overhead cost(OVHD)"].append(0.5 * (OPEX["Matinenenance (M)"][1] + OPEX["Operating labor (OL)"][1] + OPEX["Supervision and support labor (S)"][1]))
	OPEX["Direct production cost (DPC)"].append(OPEX["Raw materials"][1] + OPEX["Utility"][1] + OPEX["Matinenenance (M)"][1] + OPEX["Operating labor (OL)"][1] + OPEX["Supervision and support labor (S)"][1] + OPEX["Operating supplies"][1] + OPEX["Laboratory charges"][1])

	OPEX["Admistrative cost"].append(OPEX["Operating labor (OL)"][1] * 0.15)
	OPEX["Distribution and marketing"].append(OPEX["OPEX"][1] * 0.02)
	OPEX["R&D cost"].append(OPEX["OPEX"][1] * 0.02)
	OPEX["General expenses"].append(OPEX["Admistrative cost"][1] + OPEX["Distribution and marketing"][1] + OPEX["R&D cost"][1])

def calProfitAnalysis(CAPEX, OPEX, profitAnalysis, lawMaterialData):
	product = ""
	for key in lawMaterialData:
		if lawMaterialData[key] > 0:
			product = key
			break

	profitAnalysis[" "] = product
	profitAnalysis["OPEX"] = OPEX["OPEX"][1]
	profitAnalysis["Depreciation [USD/yr]"] = CAPEX["Fixed capital investment (FCI)"][1] / profitAnalysisData["depreciationLifetime"]
	for output_stream in outputFlowData:
		material = outputFlowData[output_stream]
		profitAnalysis[output_stream + " annual amount of product [ton/yr]"] = 0
		for key in material:
			profitAnalysis[output_stream + " annual amount of product [ton/yr]"] += lawMaterialData[key] * calcOPEXdata["plantOperationHours"] * lawMaterialWeightData[key] / 1000  # ton/yr
		profitAnalysis[output_stream + " manufacturing cost [USD/ton]"] = 0
		profitAnalysis[output_stream + " manufacturing cost [USD/ton]"] = (profitAnalysis["OPEX"] + profitAnalysis["Depreciation [USD/yr]"]) / profitAnalysis[output_stream + " annual amount of product [ton/yr]"]
