// Inspiration från -> https://electropeak.com/learn/getting-started-with-ultrasonic-module-and-arduino/
#include <Arduino.h>
#include "Distans.hpp"

// Beräkna distansen mellan ett objekt och roboten.
int distans()
{
    // Nummerna på brädan för våra pins.
    const int triggerPin = 9;
    const int echoPin = 10;

    // Ljudets hastighet i mikrosekunder. -> https://www.bananarobotics.com/shop/HC-SR04-Ultrasonic-Distance-Sensor
    const double ljudHastighet = 0.0034;

    // Chilla lite i 2 ms.
    digitalWrite(triggerPin, LOW);
    delayMicroseconds(2);

    // Skickar ut en puls under 10 ms.
    digitalWrite(triggerPin, HIGH); 
    delayMicroseconds(10);

    // Dags att chilla igen.
    digitalWrite(triggerPin, LOW);

    // Tiden för signalen att studsa fram och tillbaks.
    long tid = pulseIn(echoPin, HIGH);

    // Delar ljudets hastighet med 2 eftersom det måste åka fram och tillbaks.
    int stracka = tid * ljudHastighet / 2; 

    return stracka;
}