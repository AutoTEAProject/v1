#!/opt/anaconda3/envs/myenv/bin/python
import pandas as pd
from data import utilityCostData, calcOPEXdata, profitAnalysisData, HeaterParam, HeatExchangerParam, CompressorParam

def parseUtilityParam():
	filename = "./input/Material/MaterialData.xlsx"
	df = pd.read_excel(io = filename, sheet_name='Utility Parameter', header=1, engine='openpyxl')
 
	for i in range(0, 3):
		key = df.iat[i, 1]
		value = df.iat[i, 2]
		utilityCostData[key] = value

	for i in range(6, 8):
		key = df.iat[i, 1]
		value = df.iat[i, 2]
		calcOPEXdata[key] = value
 
	key = df.iat[11, 1]
	value = df.iat[11, 2]
	profitAnalysisData[key] = value

def parseEquipmentParam():
	filename = "./input/Material/MaterialData.xlsx"
	df = pd.read_excel(io = filename, sheet_name='Equipment Cost Parameter', header=1, engine='openpyxl')
 
	for i in range(0, 4):
		key = df.iat[i, 1]
		k1 = df.iat[i, 2]
		k2 = df.iat[i, 3]
		k3 = df.iat[i, 4]
		HeaterParam[key] = {"K1" : k1, "K2" : k2, "K3" : k3}

	for i in range(7, 11):
		key = df.iat[i, 1]
		k1 = df.iat[i, 2]
		k2 = df.iat[i, 3]
		k3 = df.iat[i, 4]
		HeatExchangerParam[key] = {"K1" : k1, "K2" : k2, "K3" : k3}
 
	for i in range(14, 16):
		key = df.iat[i, 1]
		k1 = df.iat[i, 2]
		k2 = df.iat[i, 3]
		k3 = df.iat[i, 4]
		CompressorParam[key] = {"K1" : k1, "K2" : k2, "K3" : k3}

