import smbus2
import bme280
from datetime import datetime

# Check if I2C sensor address is '0x76' or '0x77' with bash command 'i2cdetect -y 1' from Raspberry Pi machine
I2C_SENSOR_ADDRESS = 0x77  

# Initialize I2C bus
bus = smbus2.SMBus(1)

# Load calibration parameters
try:
    calibration_params = bme280.load_calibration_params(bus, I2C_SENSOR_ADDRESS)
except Exception as e:
    print(f"Error: Unable to load calibration parameters for BME280. {e}")
    calibration_params = None

# Function to read CPU temperature
def get_cpu_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
            cpu_temp_milli = int(file.read().strip())
            cpu_temp = cpu_temp_milli / 1000.0  # Convert to Celsius
            return cpu_temp
    except FileNotFoundError:
        print("Error: Unable to read CPU temperature.")
        return None

# Function to read sensor data
def get_sensor_data():
    if calibration_params is None:
        print("Error: BME280 sensor calibration parameters not loaded. Is the sensor connected?")
        return None

    try:
        # Read sensor data
        sensor_data = bme280.sample(bus, I2C_SENSOR_ADDRESS, calibration_params)
        return {
            "timestamp": sensor_data.timestamp,
            "temperature": sensor_data.temperature,
            "humidity": sensor_data.humidity,
            "pressure": sensor_data.pressure
        }
    except Exception as e:
        print(f"Error: Unable to read data from BME280 sensor. {e}")
        return None

# Function to print all data
def print_all_data():
    # Read CPU temperature
    cpu_temperature = get_cpu_temperature()

    # Read sensor data
    sensor_data = get_sensor_data()

    # Print CPU temperature
    if cpu_temperature is not None:
        print(f"CPU Temperature: {cpu_temperature:.2f}°C")

    # Print sensor data
    if sensor_data:
        print(f"Timestamp: {sensor_data['timestamp']}")
        print(f"Temperature (BME280): {sensor_data['temperature']:.2f}°C")
        print(f"Humidity: {sensor_data['humidity']:.2f}%")
        print(f"Pressure: {sensor_data['pressure']:.2f} hPa")
    else:
        print("No sensor data available.")

    print("-" * 40)  # Separator for readability

# Example usage
if __name__ == "__main__":
    while True:
        print_all_data()
        input("Press Enter to refresh the data...\n")  # Pause for manual refresh
