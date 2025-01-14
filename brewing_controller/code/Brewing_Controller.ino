#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// Initialize LCD with I2C address (default is usually 0x27 or 0x3F)
LiquidCrystal_I2C lcd(0x27, 20, 4);

// Variables
char breweryName[] = "Roberts Brewery";
float currentTemp = 25.0;
float desiredTemp = 50.0;
int power = 75;
bool heaterOn = false; // Initial state of the heater
bool pumpOn = false;    // Initial state of the pump
float pidP = 2.0;
float pidI = 0.5;
float pidD = 0.1;

// Pin Definitions
const int pumpSwitchPin = 8;  // D3
const int heaterSwitchPin = 4; // D4
const int heaterRelayPin = 5;  // D5 for SSR

// Analog Input Pins for PID and control
const int pidDPin = A0;  // D for PID
const int pidIPin = A1;  // I for PID
const int pidPPin = A2;  // P for PID
const int powerPin = A3; // Power control
const int tempPin = A6;  // Desired temperature control

// Pin for DS18B20 temperature probe
const int oneWireBus = 2; // D2
OneWire oneWire(oneWireBus);
DallasTemperature sensors(&oneWire);

void setup() {
  // Initialize LCD
  lcd.init();
  lcd.backlight();

  // Configure pins for switches and SSR
  pinMode(pumpSwitchPin, INPUT_PULLUP);  // Use internal pull-up resistor
  pinMode(heaterSwitchPin, INPUT_PULLUP); // Use internal pull-up resistor
  pinMode(heaterRelayPin, OUTPUT);       // Output to SSR
  analogWrite(heaterRelayPin, 0);        // Ensure heater is off initially

  // Start DS18B20 sensor
  sensors.begin();
  Serial.begin(9600);
  while (!Serial) {
    ;  // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  // Read switch states (LOW when pressed due to INPUT_PULLUP)
  pumpOn = digitalRead(pumpSwitchPin) == HIGH;  // Pump is ON if switch is pressed
  heaterOn = digitalRead(heaterSwitchPin) == HIGH;  // Heater is ON if switch is pressed

  // Read and map PID values from analog inputs (0-1023) to the range 0 to 2
  pidD = map(analogRead(pidDPin), 0, 1023, 200, 0) / 100.0;  // Range 0 to 2
  pidI = map(analogRead(pidIPin), 0, 1023, 200, 0) / 100.0;  // Range 0 to 2
  pidP = map(analogRead(pidPPin), 0, 1023, 200, 0) / 100.0;  // Range 0 to 2

  // Read and map power from A3 (range 0 to 100)
  power = map(analogRead(powerPin), 0, 1023, 100, 0);

  // Read and map desired temperature from A4 (range 80 to 212)
  desiredTemp = map(analogRead(tempPin), 0, 1023, 212, 80);
  

  // Request temperature from DS18B20 sensor
  sensors.requestTemperatures();
  currentTemp = sensors.getTempFByIndex(0); // Read temperature in Fahrenheit from the first sensor
  Serial.println(currentTemp);
  // Control the SSR using PWM only if heater is ON
  if (heaterOn) {
    int pwmValue = map(power, 0, 100, 0, 255);  // Map 0-100 power to 0-255 PWM range
    analogWrite(heaterRelayPin, pwmValue);
  } else {
    analogWrite(heaterRelayPin, 0);  // Turn off SSR if heater is OFF
  }

// Line 0: Display name of brewery (20 characters)
lcd.setCursor(0, 0);
lcd.print("Roberts Brewery   ");  // Already 20 characters

// Line 1: Display Current and Desired Temp (Integer only) (20 characters)
lcd.setCursor(0, 1);
String line1 = "Cur:" + String((int)currentTemp) + "F Des:" + String((int)desiredTemp) + "F  ";
while (line1.length() < 20) {
  line1 += " ";  // Pad with spaces until the length is 20
}
lcd.print(line1);

// Line 2: Display Power, Heater, and Pump Status (20 characters)
lcd.setCursor(0, 2);
String line2 = "Pow:" + String(power) + "% H:" + (heaterOn ? "ON" : "OFF") + " P:" + (pumpOn ? "ON" : "OFF");
while (line2.length() < 20) {
  line2 += " ";  // Pad with spaces until the length is 20
}
lcd.print(line2);

// Line 3: Display PID Variables (20 characters)
lcd.setCursor(0, 3);
String line3 = "P:" + String(pidP, 1) + " I:" + String(pidI, 1) + " D:" + String(pidD, 1);
while (line3.length() < 20) {
  line3 += " ";  // Pad with spaces until the length is 20
}
lcd.print(line3);


  // Add a delay for stability
  delay(100);
}
