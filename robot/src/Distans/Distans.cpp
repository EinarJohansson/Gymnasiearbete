// Inspiration från -> https://electropeak.com/learn/getting-started-with-ultrasonic-module-and-arduino/
#include <Arduino.h>
#include "Distans.hpp"

// Beräkna distansen mellan ett objekt och roboten i enhet centimeter.
int distans()
{
    // Nummerna på brädan för våra pins. Lite snuskigt att både ha de här och i robot.ino :(
    const int triggerPin = 5; // D1
    const int echoPin = 16; // D0

    // Ljudets hastighet -> https://create.arduino.cc/projecthub/abdularbi17/ultrasonic-sensor-hc-sr04-with-arduino-tutorial-327ff6
    const double ljudHastighet = 0.034;

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