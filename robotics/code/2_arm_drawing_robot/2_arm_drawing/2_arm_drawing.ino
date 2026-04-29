#include <Servo.h>
#include <math.h>

struct AnglePair {
  float theta_1; // angle of first linkage
  float theta_2; // angle of second linkage
};

int program_type = 1; // 0 = draw problem space, 1 = go to coordinates from serial
int sm_pin_1 = A0; // servo motor pin
int sm_pin_2 = A1; // servo motor pin
int sm_pin_3 = A2; // servo motor pin
int sm_min = 544; // pwm relateing to 0 degrees
int sm_max = 2400; // pwm relating to 180 degrees
Servo servo_1; // define servo object
Servo servo_2; // define servo object
Servo servo_3; // define servo object
float linkage_1 = 3; // first linkage
float linkage_2 = 3; // second linkage
int servo_wait_period = 50;
int servo_min = 0;
int servo_max = 150;
int step = 1;

AnglePair current_angles;
AnglePair desired_angles;

bool pen_down; // boolean for pen up or down

void setup() {
  // Setup servos
  servo_1.attach(sm_pin_1, sm_min, sm_max);
  servo_2.attach(sm_pin_2, sm_min, sm_max);
  servo_3.attach(sm_pin_3, sm_min, sm_max);

  // Set servo to start position
  servo_1.write(0); // straight with x-axis
  servo_2.write(0); // straight with x-axis
  servo_3.write(0); // pen up position

  // Wait until start command
  Serial.begin(9600);
  while(!Serial) { ; }
  Serial.println("Send anything over serial to start the program...");
  while (Serial.available() == 0) {} // loop until something in serial buffer
  Serial.println("Program started");
}

void loop() {
  if (program_type == 1) {
    if (Serial.available() > 0){
      // read serial for x, y coordinates and pen-down variable "x_float, y_float, pen_down" line by line
      float x_value = Serial.parseFloat();
      float y_value = Serial.parseFloat();
      float pen_down = Serial.parseInt();
      if (x_value == 0 && y_value == 0) {continue;}
      // set position to coordinate
      desired_angles = inverse_kinematics(x_value, y_value, linkage_1, linkage_2);
      int desired_theta_1 = floor(desired_angles.theta_1 * 180 / PI);
      int desired_theta_2 = floor(desired_angles.theta_2 * 180 / PI);
      // add angle increment until close enough
      int angle_increment = 1;
      while (current_angles.theta_1 != desired_theta_1 || current_angles.theta_2 != desired_theta_2) {
        if (current_angles.theta_1 < desired_theta_1) {current_angles.theta_1 += angle_increment;}
        if (current_angles.theta_1 > desired_theta_1) {current_angles.theta_1 -= angle_increment;}
        if (current_angles.theta_2 < desired_theta_2) {current_angles.theta_2 += angle_increment;}
        if (current_angles.theta_2 > desired_theta_2) {current_angles.theta_2 -= angle_increment;}
        servo_1.write(current_angles.theta_1);
        servo_2.write(current_angles.theta_2);
        servo_3.write(90*pen_down);
        delay(servo_wait_period);
        Serial.print("Current: "); Serial.print(current_angles.theta_1);
        Serial.print(","); Serial.println(current_angles.theta_2);
        Serial.print("Desired: "); Serial.print(desired_theta_1);
        Serial.print(","); Serial.println(desired_theta_2);
      }
      Serial.print("Moved to: "); Serial.print(x_value); 
      Serial.print(","); Serial.println(y_value);
    }
  }
  if (program_type == 0) {
    for (int i = servo_min; i < servo_max; i+=step){
      servo_1.write(i);
      delay(servo_wait_period);
      for (int j = servo_min; j < servo_max; j+=step){
        servo_2.write(j);
        delay(servo_wait_period); 
      }
    }
  }
}

AnglePair inverse_kinematics(float x, float y, float l1, float l2) {
  // input your desired coordinates and linkage lengths and the 
  // function will return the angles for the linkages 
  AnglePair resultant_angles;
  float cos_t2 = ((x*x + y*y - l1*l1 - l2*l2) / (2*l1*l2)); 
  resultant_angles.theta_2 = acos(cos_t2);
  resultant_angles.theta_1 = (atan2(y,x) + atan2((l2*sin(resultant_angles.theta_2)), (l1+l2*cos(resultant_angles.theta_2))));
  return(resultant_angles);
}

