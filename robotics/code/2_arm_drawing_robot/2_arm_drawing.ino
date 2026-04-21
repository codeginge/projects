#include <Servo.h>
struct AnglePair {
  int theta_1; // angle of first linkage
  int theta_2; // angle of second linkage
};

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

bool pen_down; // boolean for pen up or down

void setup() {
  // Setup servos
  servo_1.attach(sm_pin_1, sm_min, sm_max);
  servo_2.attach(sm_pin_2, sm_min, sm_max);
  servo_3.attach(sm_pin_3, sm_min, sm_max);

  // Set servo to start position
  servo_1.write(0);
  servo_2.write(0);

  // Wait until start command
  Serial.begin(9600);
  while(!Serial) { ; }
  Serial.println("Send anything over serial to start the program...");
  while (Serial.available() == 0) {} // loop until something in serial buffer
  Serial.println("Program started");
}

void loop() {
  for (int i = servo_min; i < servo_max; i+=step){
    servo_1.write(i);
    delay(servo_wait_period);
    for (int j = servo_min; j < servo_max; j+=step){
      servo_2.write(j);
      delay(servo_wait_period); 
    }
  }
}


AnglePair reverse_kinematics(float x, float y, float l1, float l2) {
  // input your desired coordinates and linkage lengths and the 
  // function will return the angles for the linkages 
  AnglePair resultant_angles;
  resultant_angles.theta_2 = acos((x*x+y*y-l1*l1-l2*l2)/(-2*l1*l2))*180/PI;
  resultant_angles.theta_1 = (atan(y/x)+atan((l2*sin(resultant_angles.theta_1))/(l1+l2*cos(resultant_angles.theta_1))))*180/PI;
  return(resultant_angles);
}

