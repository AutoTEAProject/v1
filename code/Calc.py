from Utility import checkType
from data import lawMaterialCostData, lawMaterialWeightData, utilityCostData, calcOPEXdata, profitAnalysisData
from enums import Index

def calCAPEX(inputData, cost, CAPEX):
	#CAPEX 출력 순서 지정을 위한 전방선언
	CAPEX["CAPEX"] = ""
	CAPEX[" "] = ""
	CAPEX["CLASSIFICATION"] = "[USD/yr]"
	CAPEX[" "] = ""
	CAPEX["Direct cost"] = ""
	CAPEX["ISBL (Inside battery limit, 전체공사구역 중 주 공정시설)"] = ""
	CAPEX["Equipment cost"] = 0
	CAPEX["Installation of equipment "] = 0
	CAPEX["Instrument and control"] = 0
	CAPEX["Piping"] = 0
	CAPEX["Electrical"] = 0
	CAPEX["  "] = ""
 
	CAPEX["OSBL(Outside bettery limit,주공정시설 외 부대시설)"] = ""
	CAPEX["Building and building services"] = 0
	CAPEX["Yard improvements"] = 0
	CAPEX["Services facilities"] = 0
	CAPEX["Land"] = 0
	CAPEX[" "] = ""

	CAPEX["Total direct cost"] = 0
	CAPEX["   "] = ""

	CAPEX["Indirect cost"] = ""
	CAPEX["Engineering"] = 0
	CAPEX["Construction expenses"] = 0
	CAPEX["Contractor's fee"] = 0
	CAPEX["Contingency"] = 0
	CAPEX["    "] = ""
 
	CAPEX["Total indirect cost"] = 0
	CAPEX["     "] = ""
 
	CAPEX["Fixed capital investment (FCI)"] = 0
	CAPEX["Start up cost (SUC)"] = 0
	CAPEX["      "] = ""
 
	CAPEX["Total capital investment (Capex)"] = 0
	CAPEX["Annualized capital cost (r=5%, t=30 year)"] = 0
	# print(cost)
	for key in cost:
		# print(key + " " + inputData[key]["Type"])
		if ("ATEA" in cost[key]):
			CAPEX["Equipment cost"] += int(cost[key]["ATEA"]["EQUIPMENT COST"])
			continue;
		if (inputData[key]["Type"] == "REACT"):
			CAPEX["Equipment cost"] += int(cost[key]["input"]["EQUIPMENT COST"])
		elif(inputData[key]["Type"] == "HEX"):
			CAPEX["Equipment cost"] += int(cost[key]["U-tube"]["EQUIPMENT COST"])
		elif(inputData[key]["Type"] == "HTX"):
			CAPEX["Equipment cost"] += int(cost[key]["Hot water heater"]["EQUIPMENT COST"])
		elif(inputData[key]["Type"] == "COMP"):
			CAPEX["Equipment cost"] += int(cost[key]["Centrifugal, axial and reciprocating"]["EQUIPMENT COST"])
		elif(inputData[key]["Type"] == "FLASH"):
			CAPEX["Equipment cost"] += int(cost[key]["ATEA"]["EQUIPMENT COST"])
	CAPEX["Fixed capital investment (FCI)"] = CAPEX["Equipment cost"] * 100 / 40
	CAPEX["Start up cost (SUC)"] = CAPEX["Fixed capital investment (FCI)"] * 0.1

	CAPEX["Installation of equipment "] = CAPEX["Fixed capital investment (FCI)"] * 0.08
	CAPEX["Instrument and control"] = CAPEX["Fixed capital investment (FCI)"] * 0.05
	CAPEX["Piping"] = CAPEX["Fixed capital investment (FCI)"] * 0.03
	CAPEX["Electrical"] = CAPEX["Fixed capital investment (FCI)"] * 0.05
	
	CAPEX["Building and building services"] = CAPEX["Fixed capital investment (FCI)"] * 0.07
	CAPEX["Yard improvements"] = CAPEX["Fixed capital investment (FCI)"] * 0.02
	CAPEX["Services facilities"] = CAPEX["Fixed capital investment (FCI)"] * 0.08
	CAPEX["Land"] = CAPEX["Fixed capital investment (FCI)"] * 0.02
 
	CAPEX["Total direct cost"] = CAPEX["Equipment cost"] + CAPEX["Installation of equipment "] + CAPEX["Instrument and control"] + CAPEX["Piping"] + CAPEX["Electrical"] + CAPEX["Building and building services"] + CAPEX["Yard improvements"] + CAPEX["Services facilities"] + CAPEX["Land"]
 
	CAPEX["Engineering"] = CAPEX["Fixed capital investment (FCI)"] * 0.05
	CAPEX["Construction expenses"] = CAPEX["Fixed capital investment (FCI)"] * 0.05
	CAPEX["Contractor's fee"] = CAPEX["Fixed capital investment (FCI)"] * 0.05
	CAPEX["Contingency"] = CAPEX["Fixed capital investment (FCI)"] * 0.05

	CAPEX["Total indirect cost"] = CAPEX["Engineering"] + CAPEX["Construction expenses"] + CAPEX["Contractor's fee"] + CAPEX["Contingency"]
	CAPEX["Start up cost (SUC)"] = CAPEX["Fixed capital investment (FCI)"] * 0.1
	
	CAPEX["Total capital investment (Capex)"] = CAPEX["Start up cost (SUC)"] + CAPEX["Fixed capital investment (FCI)"]
	CAPEX["Annualized capital cost (r=5%, t=30 year)"] = CAPEX["Total capital investment (Capex)"] / ((1 - (1 / ((1.05)**30)))/0.05)

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
	OPEX["OPEX (Total product costm TPC)"] = ""
	OPEX[" "] = ""
	OPEX["CLASSIFICATION"] = "[USD/yr]"
	OPEX[" "] = ""
	OPEX["Fixed charge(FC)"] = 0
	OPEX["Local taxes, Insurance"] = 0
	OPEX[" "] = ""
 
	OPEX["Direct production cost (DPC)"] = 0
	OPEX["Raw materials"] = 0
	OPEX["Utility"] = 0
	OPEX["Matinenenance (M)"] = 0
	OPEX["Operating labor (OL)"] = 0
	OPEX["Supervision and support labor (S)"] = 0
	OPEX["Operating supplies"] = 0
	OPEX["Laboratory charges"] = 0
	OPEX["  "] = ""
 
	OPEX["Plant overhead cost(OVHD)"] = 0
	OPEX["   "] = ""
 
	OPEX["General expenses"] = 0
	OPEX["Admistrative cost"] = 0
	OPEX["Distribution and marketing"] = 0
	OPEX["R&D cost"] = 0
 
	OPEX["    "] = ""
	OPEX["OPEX"] = 0

	OPEX["Fixed charge(FC)"] = CAPEX["Fixed capital investment (FCI)"] * 0.01
	OPEX["Local taxes, Insurance"] = CAPEX["Fixed capital investment (FCI)"] * 0.01

	OPEX["Raw materials"] = 0 # 이거 raw material key에 따른 알맞은 값 넣어야함.
	for key in lawMaterialData:
		if lawMaterialData[key] < 0:
			OPEX["Raw materials"] += lawMaterialData[key] * lawMaterialCostData[key] * calcOPEXdata["plantOperationHours"] * -1 * lawMaterialWeightData[key] * lawMaterialWeightData[key]  # kg 단위로 바꿔주기 위해 1000으로 나눔
		# elif key == "CATALYST":
			# 	OPEX["Raw materials"] += lawMaterialData[key] * plantOperationHours * -1 * calcOPEXdata["catalystPrice"] / 1000  # ton 단위로 바꿔주기 위해 1000으로 나눔
	#OPEX["Raw materials"] = lawMaterialData["H2"] * plantOperationHours *  -1 * hydrogenPrice * hydrogenWeight + lawMaterialData["N2"] * plantOperationHours * -1 * nitrogenPrice * nitrogenWeight
	OPEX["Utility"] = 0
	for key in utility:
		if "ELECTRICITY UTILITY ANNUAL COST [USD/year]" in utility[key] and utility[key]["ELECTRICITY UTILITY ANNUAL COST [USD/year]"] > 0:
			OPEX["Utility"] += utility[key]["ELECTRICITY UTILITY ANNUAL COST [USD/year]"]
		if "COOLING UTILITY ANNUAL COST [USD/year]" in utility[key] and utility[key]["COOLING UTILITY ANNUAL COST [USD/year]"] > 0:
			OPEX["Utility"] += utility[key]["COOLING UTILITY ANNUAL COST [USD/year]"]
		if "HOT UTILITY ANNUAL COST [USD/year]" in utility[key] and utility[key]["HOT UTILITY ANNUAL COST [USD/year]"] > 0:
			OPEX["Utility"] += utility[key]["HOT UTILITY ANNUAL COST [USD/year]"]

	OPEX["Matinenenance (M)"] = CAPEX["Fixed capital investment (FCI)"] * 0.01
	OPEX["Operating supplies"] = OPEX["Matinenenance (M)"] * 0.1



	OPEX["OPEX"] = 1.35135135135 * (CAPEX["Fixed capital investment (FCI)"] * 0.026 + (OPEX["Utility"] + OPEX["Raw materials"]))
	OPEX["Operating labor (OL)"] = OPEX["OPEX"] * 0.1
	OPEX["Supervision and support labor (S)"] = OPEX["Operating labor (OL)"] * 0.3
	OPEX["Laboratory charges"] = OPEX["Operating labor (OL)"] * 0.1
	OPEX["Plant overhead cost(OVHD)"] = 0.5 * (OPEX["Matinenenance (M)"] + OPEX["Operating labor (OL)"] + OPEX["Supervision and support labor (S)"])
	OPEX["Direct production cost (DPC)"] = OPEX["Raw materials"] + OPEX["Utility"] + OPEX["Matinenenance (M)"] + OPEX["Operating labor (OL)"] + OPEX["Supervision and support labor (S)"] + OPEX["Operating supplies"] + OPEX["Laboratory charges"]

	OPEX["Admistrative cost"] = OPEX["Operating labor (OL)"] * 0.15
	OPEX["Distribution and marketing"] = OPEX["OPEX"] * 0.02
	OPEX["R&D cost"] = OPEX["OPEX"] * 0.02
	OPEX["General expenses"] = OPEX["Admistrative cost"] + OPEX["Distribution and marketing"] + OPEX["R&D cost"]

def calProfitAnalysis(CAPEX, OPEX, profitAnalysis, lawMaterialData):
	product = ""
	for key in lawMaterialData:
		if lawMaterialData[key] > 0:
			product = key
			break

	profitAnalysis[" "] = product
	profitAnalysis["OPEX"] = OPEX["OPEX"]
	profitAnalysis["Depreciation [USD/yr]"] = CAPEX["Fixed capital investment (FCI)"] / profitAnalysisData["depreciationLifetime"]
	profitAnalysis["annual amount of product [ton/yr]"] = 0
	for key in lawMaterialData:
		if lawMaterialData[key] > 0:
			profitAnalysis["annual amount of product [ton/yr]"] = lawMaterialData[key] * calcOPEXdata["plantOperationHours"] * lawMaterialWeightData[key] / 1000  # ton/yr
			break
	if (profitAnalysis["annual amount of product [ton/yr]"] == 0):
		profitAnalysis["Manufacturing cost [USD/ton]"] = 0
	else:
		profitAnalysis["Manufacturing cost [USD/ton]"] = (profitAnalysis["OPEX"] + profitAnalysis["Depreciation [USD/yr]"]) / profitAnalysis["annual amount of product [ton/yr]"]