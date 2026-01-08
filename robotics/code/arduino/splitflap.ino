// C++ code
//
#include <Stepper.h>

// character setup
char avaliable_characters[] = {
  ' ','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
};

// pin setup
int hall_effect_sensor_pin = 3;
int sm_in1 = 8;
int sm_in2 = 9;
int sm_in3 = 10;
int sm_in4 = 11;

// variable setup
const int stepsPerRevolution = 2048; // Steps for a 28BYJ-48 motor
int stepper_motor_rpm = 12;
int steps_per_tic = 5;
volatile int current_step = 0; // volatile because it is changed outside the loop function
int class_example = 1;
char class_example_message[] = "HELLO WORLD";
int time_between_characters = 2500;

// motor setup
Stepper myStepper(stepsPerRevolution, sm_in1, sm_in2, sm_in3, sm_in4);

void setup()
{
  Serial.begin(9600);
  myStepper.setSpeed(stepper_motor_rpm); // set motor RMP
  pinMode(hall_effect_sensor_pin, INPUT);
  attachInterrupt(digitalPinToInterrupt(hall_effect_sensor_pin), set_motor_to_zero, FALLING);
}

void loop()
{
  if (Serial.available() > 0 && class_example == 0) {
    float desired_angle = splitflap_character_angle(Serial.read());
    float desired_step = (desired_angle / 360) * stepsPerRevolution; 

    Serial.print("Desired angle - ");
    Serial.print(desired_angle);
    Serial.print("  |  Desired step - ");
    Serial.print(desired_step);
    Serial.print("  |  Current Step - ");
    Serial.println(current_step);
    
    while (current_step <= floor(desired_step) || current_step > (desired_step + 2 * steps_per_tic)) {
      myStepper.step(steps_per_tic);
      current_step += steps_per_tic;
    }

    stop_hold();
    Serial.print("  |  Current Step - ");
    Serial.println(current_step);
    delay(time_between_characters);
    }

  if (class_example == 1){
    int message_length = strlen(class_example_message);
    for (int i; i < message_length; i++) {
      float desired_angle = splitflap_character_angle(class_example_message[i]);
      float desired_step = (desired_angle / 360) * stepsPerRevolution; 

      Serial.print("Desired angle - ");
      Serial.print(desired_angle);
      Serial.print("  |  Desired step - ");
      Serial.print(desired_step);

      while (current_step <= floor(desired_step) || current_step > (desired_step + 2 * steps_per_tic)) {
        myStepper.step(steps_per_tic);
        current_step += steps_per_tic;
      }

      stop_hold();
      Serial.print("  |  Current Step - ");
      Serial.println(current_step);
      delay(time_between_characters);
    }
  }

  
}

int splitflap_character_angle(char character)
{
  int character_number =sizeof(avaliable_characters);
  float angle_multiple = 360/character_number;
  for (int i=0; i < character_number; i++) {
    if (avaliable_characters[i] == character) {
      return i*angle_multiple;
    }
  }
}

void set_motor_to_zero() 
{
  current_step = 0;
}

void stop_hold()
{
  digitalWrite(sm_in1, LOW);
  digitalWrite(sm_in2, LOW);
  digitalWrite(sm_in3, LOW);
  digitalWrite(sm_in4, LOW);
}