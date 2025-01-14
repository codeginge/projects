# Potentiometers: 1 = Distance, 2 = Deflection, 3 = Number of marbles, 4 = Counter weight

import serial
import matplotlib.pyplot as plt  # Optional: for plotting live data

# Establish serial connection
arduino_port = '/dev/cu.usbmodem1201'  # Change this to your Arduino's port (e.g., COM3 for Windows)
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)



# Optional: for plotting live data
plt.ion()  # Enable interactive mode for live plotting
fig, ax = plt.subplots()
x_data, y_data = [], []

while True:
    if ser.in_waiting > 0:
        # Read data from serial
        data = ser.readline().decode('utf-8').rstrip()
        
        if data and ',' in data:  # Check if data is not empty and contains comma-separated values
            values = data.split(',')
            
            # Convert non-empty strings to integers
            values = [int(val) for val in values if val.strip()]
            
            if len(values) == 5:  # Check if there are 5 values
                print(values)  # Print received data

                # Calculate sum of potentiometer values
                total_value = sum(values)
                print("Total:", total_value)  # Print the total sum
                
                # Optional: for plotting live data
                x_data.append(len(x_data))
                y_data.append(total_value)
                ax.clear()
                ax.plot(x_data, y_data)
                ax.set_xlabel('Time')
                ax.set_ylabel('Sum of Potentiometer Values')
                plt.pause(0.05)  # Adjust as needed for plotting speed
