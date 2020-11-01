#define BAUD 9600
#define PORT 8888
#define SERVO_PIN 0
#define TRIGGER_PIN 5
#define ECHO_PIN 16

// importerar kod. 
#include "src/Snurris/Snurris.hpp"
#include "src/Klient/Klient.hpp"

// Serverns ip
IPAddress IP(8, 8, 8, 8);

// Initierar ett Klient objekt.
Klient klient(IP, PORT);

// Objekt för servomotorn
Servo servo;

// setup funktionen körs en gång innan loopen:
void setup() {
    Serial.begin(BAUD);
    pinMode(TRIGGER_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    klient.anslut("SSID", "PASS");
    servo.attach(SERVO_PIN);
}

// loop funktionen kallas kontinuerligt:
void loop()
{
    snurra(servo, klient);
}
