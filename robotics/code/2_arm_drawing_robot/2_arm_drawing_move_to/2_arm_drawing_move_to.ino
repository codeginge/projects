#include <Servo.h>
#include <math.h>
int sm_pin1 = A0, sm_pin2 = A1, sm_min = 544, sm_max = 2400, move_time = 100, draw = 1;
float theta_1 = 0.0, theta_2 = 0.0, l1 = 3.0, l2 = 3.0, x = 4.0, y = 0.0;
Servo servo_1, servo_2;

void setup() {
  servo_1.attach(sm_pin1, sm_min, sm_max);
  servo_2.attach(sm_pin2, sm_min, sm_max);
  Serial.begin(9600); 
}

void loop() {
  px = x, py = y;
  if (Serial.available() > 0) {
    x = Serial.parseFloat();
    y = Serial.parseFloat();
    if (x == 0 && y == 0) {x = 4, y = 0; }
  }
  if (draw == 1) {
    // ADD - make move speed constant
    theta_2 = acos((x*x + y*y - l1*l1 - l2*l2) / (2.0*l1*l2));
    theta_1 = (atan2(y,x) + atan2((l2*sin(theta_2)), (l1+l2*cos(theta_2))));
    moveArm(theta_1, theta_2);
    servo_2.write(theta_2 * 
    delay(move_time);
  } else {
    servo_1.write(theta_1 * RAD_TO_DEG);
    servo_2.write(theta_2 * RAD_TO_DEG);
  }
}

void move_arm(float theta_1, float theta_2) {
  servo_1.write(theta_1 * RAD_TO_DEG);
  servo_2.write(theta_2 * RAD_TO_DEG);
}
