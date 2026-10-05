#include <Servo.h>
#include <math.h>
int sm_pin1 = A0, sm_pin2 = A1, sm_min = 544, sm_max = 2400, move_time = 50, draw = 1;
float t1 = 0.0, t2 = 0.0, l1 = 3.0, l2 = 3.0, x = 4.0, y = 0.0, xo = x, yo = y, ct1 = t1, ct2 = t2, st = 0.02, t1st, t2st, tdist;
Servo servo_1, servo_2;

void setup() {
  servo_1.attach(sm_pin1, sm_min, sm_max);
  servo_2.attach(sm_pin2, sm_min, sm_max);
  Serial.begin(9600); 
}

void loop() {
  if (draw == 1) {
    for (float x_pos = 4.0; x_pos > 0.5; x_pos -= 0.1) {
      for (float y_pos = 4.0; y_pos > 0.5; y_pos -= 0.1) {
        x = x_pos, y = ypos;
        t2 = acos((x*x + y*y - l1*l1 - l2*l2) / (2.0*l1*l2));
        t1 = (atan2(y,x) + atan2((l2*sin(t2)), (l1+l2*cos(t2))));
        moveArm(t1, t2, st, move_time);
  } else {
    moveArm(t1, t2, st, move_time);
  }
}

void moveArm(float t1, float t2, float step, int wait_ms) {
  tdist = sqrt((t1 - ct1)*(t1 - ct1) + (t2 - ct2)*(t2 - ct2));
  t1st = step*((t1 - ct1)/tdist), t2st = step*((t2 - ct2)/tdist); 
  while (ct1 != t1 || ct2 != t2) {
    if (abs(ct1 - t1) <= step) {
      ct1 = t1;
    } else {
      ct1 += t1st;
    }
    if (abs(ct2 - t2) <= step) {
      ct2 = t2;
    } else {
      ct2 += t2st;
    }
    servo_1.write(ct1 * RAD_TO_DEG);
    servo_2.write(ct2 * RAD_TO_DEG);    
    delay(wait_ms);
  }
}
