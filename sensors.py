import json
import time
import board
import busio
import adafruit_scd4x
from adafruit_pm25.i2c import PM25_I2C
from ideaboard import IdeaBoard

# Initialize IdeaBoard and required interfaces
ib = IdeaBoard()
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
pm25 = PM25_I2C(i2c, None)  # Reset pin is set to None
scd4x = adafruit_scd4x.SCD4X(i2c)

# Start periodic measurements
scd4x.start_periodic_measurement()

# Define the analog input pin
entrada = ib.AnalogIn(board.IO36)

class Sensors:
    def __init__(self, pm25_env, pm10_env, co2_value, temperature_value, humidity_value, mics_5524):
        self.pm25_env = pm25_env
        self.pm10_env = pm10_env
        self.co2_value = co2_value
        self.temperature_value = temperature_value
        self.humidity_value = humidity_value
        self.mics_5524 = mics_5524

    def read_sensors(self):
        try:
            # Read sensor data and update class attributes
            aqdata = pm25.read()
            self.pm25_env = aqdata["pm25 env"]
            self.pm10_env = aqdata["pm100 env"]
            self.co2_value = scd4x.CO2
            self.temperature_value = scd4x.temperature
            self.humidity_value = scd4x.relative_humidity
            self.mics_5524 = entrada.value
        except RuntimeError:
            print("Error")

    def get_sensor_data(self):
        if self.co2_value is not None and self.temperature_value is not None and self.humidity_value is not None:
            sensor_data = {
                "VOC": self.mics_5524,
                "PM2.5": self.pm25_env,
                "PM10": self.pm10_env,
                "CO2": self.co2_value,
                "Temperatura": round(self.temperature_value, 1),
                "Humedad": round(self.humidity_value, 1)
            }
            return sensor_data
        return {}
    
    
    def print_sensor_data(self):
        if self.co2_value is not None and self.temperature_value is not None and self.humidity_value is not None:
            print(f"VOC: {self.mics_5524} ")
            print(f"PM2.5: {self.pm25_env} µg/m³")
            print(f"PM10: {self.pm10_env} µg/m³")
            print(f"CO2: {self.co2_value} ppm")
            print(f"Temperatura: {self.temperature_value:.1f} °C")
            print(f"Humedad: {self.humidity_value:.1f} %")
            print()
            
    def generate_sensor_data_json(self):
        json_data = {
            "device_id": 1,
            "sensor_data": []
        }
        
        if self.co2_value is not None and self.temperature_value is not None and self.humidity_value is not None:
            sensor_data_dict = {
                "sensor_name": "VOC",
                "value": self.mics_5524,
                "unit": ""
            }
            json_data["sensor_data"].append(sensor_data_dict)
            
            sensor_data_dict = {
                "sensor_name": "PM2.5",
                "value": self.pm25_env,
                "unit": "µg/m³"
            }
            json_data["sensor_data"].append(sensor_data_dict)
            
            sensor_data_dict = {
                "sensor_name": "PM10",
                "value": self.pm10_env,
                "unit": "µg/m³"
            }
            json_data["sensor_data"].append(sensor_data_dict)
            
            sensor_data_dict = {
                "sensor_name": "CO2",
                "value": self.co2_value,
                "unit": "ppm"
            }
            json_data["sensor_data"].append(sensor_data_dict)
            
            sensor_data_dict = {
                "sensor_name": "Temperatura",
                "value": self.temperature_value,
                "unit": "°C"
            }
            json_data["sensor_data"].append(sensor_data_dict)
            
            sensor_data_dict = {
                "sensor_name": "Humedad",
                "value": self.humidity_value,
                "unit": "%"
            }
            json_data["sensor_data"].append(sensor_data_dict)
        
        return json_data
