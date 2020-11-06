#define TRIGGER_PIN 5
#define ECHO_PIN 16
#define MAX_DISTANCE 450
#define ITERATIONS 5

#include "Distans.hpp"
#include "../NewPing/NewPing.h"

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

unsigned int distans()
{
    unsigned long tid = sonar.ping_median(ITERATIONS);
    Serial.printf("\nMedian tiden:\t%lu\n", tid);
    unsigned int distans = sonar.convert_cm((unsigned int) tid);
    Serial.printf("\nSträcka:\t%d\n", distans);
    return distans;
}
