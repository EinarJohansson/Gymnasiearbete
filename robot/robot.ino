#define BAUD 115200
#define PORT 8888
#define SERVO_PIN 0

// importerar kod. 
#include "src/Snurris/Snurris.hpp"
#include "src/Klient/Klient.hpp"

// Serverns ip
IPAddress IP(172, 29, 249, 62);

// Initierar ett Klient objekt.
Klient klient(IP, PORT);

// Objekt för servomotorn
Servo servo;

// setup funktionen körs en gång innan loopen:
void setup() {
    Serial.begin(BAUD);
    klient.anslut("nrk_edu2", "pskDgDans080108");
    servo.attach(SERVO_PIN);
}

// loop funktionen kallas kontinuerligt:
void loop()
{
  snurra(servo, klient);
}
