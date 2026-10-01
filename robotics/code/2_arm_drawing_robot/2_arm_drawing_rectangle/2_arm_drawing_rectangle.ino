#include <Servo.h>
#include <math.h>
int sm_pin1 = A0, sm_pin2 = A1, sm_min = 544, sm_max = 2400, move_time = 200; 
float theta_1 = 0.0, theta_2 = 0.0, l1 = 2.0, l2 = 2.0, x = 4.0, y = 0.0;
Servo servo_1, servo_2;

void setup() {
  servo_1.attach(sm_pin1, sm_min, sm_max);
  servo_2.attach(sm_pin2, sm_min, sm_max);
}

void loop() {
  for (float x_pos = 2.0; x_pos > -2.0; x_pos -= 0.1) {
    for (float y_pos = 2.0; y_pos > -2.0; y_pos -= 0.1) {
      x = x_pos, y = y_pos;
      theta_2 = acos((x*x + y*y - l1*l1 - l2*l2) / (2.0*l1*l2));
      theta_1 = (atan2(y,x) + atan2((l2*sin(theta_2)), (l1+l2*cos(theta_2))));
      servo_1.write(theta_1 * RAD_TO_DEG);
      servo_2.write(theta_2 * RAD_TO_DEG);
      delay(move_time);
    }
  }
}
