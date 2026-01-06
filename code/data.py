# This file includes all the data required for TEA calculation.
import pandas as pd

lawMaterialCostData = {}

lawMaterialWeightData = {}

outputFlowData = {}

utilityCostData = {
    'electricityCostPerKWH' : 0.1088, # $USD/kWh -> ELECTRICITY UTILITY 계산할 때 사용
	'NGprice' : 0.0075, # USD/kWh -> Hot utility 계산할 때 사용
	'CoolingWaterPrice' : 0.0000458 #USD/kg -> Cooling utility 계산할 때 사용
}

calcOPEXdata = {
	'coolingWaterPrice' : 0.00053, #USD/kg
	'catalystPrice' : 1, #USD/ton
	'plantOperationHours' : 8400 #hours/year
}

profitAnalysisData = {
	'depreciationLifetime' : 20, #years
}




# 여기부터는 각종 설비 비용 산정을 위한 상수들입니다.
HeaterParam = {
	"Diphenyl heater" : {"K1": 2.2628, "K2": 0.8581, "K3": 0.0003} ,
	"Molten salt heater" : {"K1": 1.1979, "K2": 1.4782, "K3": -0.0958} ,
	"Hot water heater" : {"K1": 2.0829, "K2": 0.9074, "K3": -0.0243} ,
	"Steam boiler" : {"K1": 6.9617, "K2": -1.48, "K3": 0.3161} 
}

HeatExchangerParam = {
	"Fixed tube" : {"K1": 4.3247, "K2": -0.303, "K3": 0.1634},
	"Floating head" : {"K1": 4.8306, "K2": -0.8509, "K3": 0.3187},
	"U-tube" : {"K1": 4.1884, "K2": -0.2503, "K3": 0.1974},
	"Bayonet" : {"K1": 4.2768, "K2": -0.0495, "K3": 0.1431}
}

CompressorParam = {
	"Centrifugal, axial and reciprocating" : {"K1": 2.2891, "K2": 1.3604, "K3": -0.1027},
	"Rotary" : {"K1": 5.0355, "K2": -1.8002, "K3": 0.8253}
}
ReactParam = {
	"Nan" : {"K1": 0, "K2": 0, "K3": 0}
}

