#include <Servo.h>

#define ENA 5
#define IN1 4
#define IN2 3
#define ENB 9
#define IN3 7
#define IN4 8
#define SRV 11

bool forward = true;
int drive = 0;
int turn = 90;
Servo steering;

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);

  steering.attach(SRV);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char opt = Serial.read();

    switch(opt) {
      case 'F':
      case 'f':
        if (forward) {
          drive = Serial.parseInt();
        }
        else {
          forward = true;
          digitalWrite(IN1, HIGH);
          digitalWrite(IN2, LOW);
          digitalWrite(IN3, HIGH);
          digitalWrite(IN4, LOW);
          drive = Serial.parseInt();
        }
        break;

      case 'B':
      case 'b':
        if (!forward) {
          drive = Serial.parseInt();
        }
        else {
          forward = false;
          digitalWrite(IN1, LOW);
          digitalWrite(IN2, HIGH);
          digitalWrite(IN3, LOW);
          digitalWrite(IN4, HIGH);
          drive = Serial.parseInt();
        }
        break;

      case 'T':
      case 't':
        turn = Serial.parseInt();
        steering.write(turn);
        break;

      case 'S':
      case 's':  
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
        steering.write(90);
        break;
    }
  }

  analogWrite(ENA, drive);
  analogWrite(ENB, drive);

  delay(20);
}
