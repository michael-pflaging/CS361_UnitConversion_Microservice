from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import requests
import json

app = FastAPI(title="Unit Conversion")
# fastapi run main.py

# Define conversion rates for each weight unit
weight_conversion_rates = {
    'kg': {'lbs': 2.20462, 'g': 1000, 'oz': 35.274, 'mg': 1_000_000, 'tonne': 0.001, 'st': 0.157473},
    'lbs': {'kg': 0.453592, 'g': 453.592, 'oz': 16, 'mg': 453_592, 'tonne': 0.000453592, 'st': 0.0714286},
    'g': {'kg': 0.001, 'lbs': 0.00220462, 'oz': 0.035274, 'mg': 1000, 'tonne': 1e-6, 'st': 0.000157473},
    'oz': {'kg': 0.0283495, 'lbs': 0.0625, 'g': 28.3495, 'mg': 28_349.5, 'tonne': 2.835e-5, 'st': 0.00446429},
    'mg': {'kg': 1e-6, 'lbs': 2.2046e-6, 'g': 0.001, 'oz': 3.5274e-5, 'tonne': 1e-9, 'st': 1.5747e-7},
    'tonne': {'kg': 1000, 'lbs': 2204.62, 'g': 1_000_000, 'oz': 35_274, 'mg': 1_000_000_000, 'st': 157.473},
    'st': {'kg': 6.35029, 'lbs': 14, 'g': 6350.29, 'oz': 224, 'mg': 6_350_290, 'tonne': 0.00635029}
}


# Define conversion rates for each length unit
length_conversion_rates = {
    'cm': {'in': 0.393701, 'm': 0.01, 'mm': 10, 'yd': 0.0109361, 'ft': 0.0328084, 'mi': 6.2137e-6, 'km': 0.00001, 'µm': 10_000, 'nm': 10_000_000},
    'in': {'cm': 2.54, 'm': 0.0254, 'mm': 25.4, 'yd': 0.0277778, 'ft': 0.0833333, 'mi': 1.5783e-5, 'km': 0.0000254, 'µm': 25_400, 'nm': 25_400_000},
    'm': {'cm': 100, 'in': 39.3701, 'mm': 1000, 'yd': 1.09361, 'ft': 3.28084, 'mi': 0.000621371, 'km': 0.001, 'µm': 1_000_000, 'nm': 1_000_000_000},
    'mm': {'cm': 0.1, 'in': 0.0393701, 'm': 0.001, 'yd': 0.00109361, 'ft': 0.00328084, 'mi': 6.2137e-7, 'km': 1e-6, 'µm': 1000, 'nm': 1_000_000},
    'yd': {'cm': 91.44, 'in': 36, 'm': 0.9144, 'mm': 914.4, 'ft': 3, 'mi': 0.000568182, 'km': 0.0009144, 'µm': 914_400, 'nm': 914_400_000},
    'ft': {'cm': 30.48, 'in': 12, 'm': 0.3048, 'mm': 304.8, 'yd': 0.333333, 'mi': 0.000189394, 'km': 0.0003048, 'µm': 304_800, 'nm': 304_800_000},
    'mi': {'cm': 160_934, 'in': 63_360, 'm': 1609.34, 'mm': 1_609_344, 'yd': 1760, 'ft': 5280, 'km': 1.60934, 'µm': 1.609e+9, 'nm': 1.609e+12},
    'km': {'cm': 100_000, 'in': 39_370.1, 'm': 1000, 'mm': 1_000_000, 'yd': 1093.61, 'ft': 3280.84, 'mi': 0.621371, 'µm': 1_000_000_000, 'nm': 1e+12},
    'µm': {'cm': 0.0001, 'in': 3.937e-5, 'm': 1e-6, 'mm': 0.001, 'yd': 1.0936e-6, 'ft': 3.2808e-6, 'mi': 6.2137e-10, 'km': 1e-9, 'nm': 1000},
    'nm': {'cm': 1e-7, 'in': 3.937e-8, 'm': 1e-9, 'mm': 1e-6, 'yd': 1.0936e-9, 'ft': 3.2808e-9, 'mi': 6.2137e-13, 'km': 1e-12, 'µm': 0.001}
}


class CurrencyConversionRequest(BaseModel):
    source_unit: str
    target_unit: str
    amount: float

class WeightConversionRequest(BaseModel):
    source_unit: str
    target_unit: str
    amount: float

class LengthConversionRequest(BaseModel):
    source_unit: str
    target_unit: str
    amount: float

@app.post("/currency", status_code=status.HTTP_200_OK)
async def unit_conversion(request: CurrencyConversionRequest) -> float:
    try:
        url = "https://api.exchangerate-api.com/v4/latest/" + request.source_unit
        response = requests.get(url)
        json_data = json.loads(response.text)
        rate_array = json_data["rates"]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source currency not found")
    try:
        rate = rate_array[request.target_unit]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target currency not found")
    output = float(request.amount) * rate
    return float(output)

@app.post('/weight', status_code=status.HTTP_200_OK)
async def weight_conversion(request: WeightConversionRequest) -> float:
    if request.source_unit not in weight_conversion_rates:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source unit not found")
    elif request.target_unit not in weight_conversion_rates[request.source_unit]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target unit not found")
    converted_value = request.amount * weight_conversion_rates[request.source_unit][request.target_unit]
    return float(converted_value)

@app.post('/length', status_code=status.HTTP_200_OK)
async def length_conversion(request: LengthConversionRequest) -> float:
    if request.source_unit not in length_conversion_rates:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source unit not found")
    elif request.target_unit not in length_conversion_rates[request.source_unit]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target unit not found")
    converted_value = request.amount * length_conversion_rates[request.source_unit][request.target_unit]
    return float(converted_value)