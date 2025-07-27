#include <Servo.h>

Servo leftServo;
Servo rightServo;
int trigPin = 10;
int echoPin = 11;
int leftServoPin = 9;
int rightServoPin = 6;
int ledPin = 5;  // LED connected to Pin 5

void setup() {
    leftServo.attach(leftServoPin);
    rightServo.attach(rightServoPin);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    pinMode(ledPin, OUTPUT); // Set LED pin as OUTPUT
    Serial.begin(9600);
    leftServo.write(90);
    rightServo.write(90);
    digitalWrite(ledPin, LOW); // Start with LED OFF
}

void moveServoSmoothly(Servo &servo, int start, int end, int stepDelay) {
    if (start < end) {
        for (int pos = start; pos <= end; pos++) {
            servo.write(pos);
            delay(stepDelay);
        }
    } else {
        for (int pos = start; pos >= end; pos--) {
            servo.write(pos);
            delay(stepDelay);
        }
    }
}

void loop() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH);
    int distance = duration * 0.034 / 2;

    if (distance > 200 || distance < 0) { // Ignore invalid readings
        return;
    }

    Serial.println(distance);

    if (distance <= 5) {
        moveServoSmoothly(leftServo, leftServo.read(), 0, 5);
        moveServoSmoothly(rightServo, rightServo.read(), 180, 5);
        digitalWrite(ledPin, HIGH); //Turn LED ON
    } else {
        moveServoSmoothly(leftServo, leftServo.read(), 90, 5);
        moveServoSmoothly(rightServo, rightServo.read(), 90, 5);
        digitalWrite(ledPin, LOW);  // Turn LED OFF
    }
    delay(50); // Reduce delay for better reaction time
}
