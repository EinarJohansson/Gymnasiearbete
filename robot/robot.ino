// importerar kod.
#include "src/config.hpp"
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
    klient.anslut(SSID, PASS);
    servo.attach(SERVO_PIN);
}

// loop funktionen kallas kontinuerligt:
void loop()
{
  snurra(servo, klient);
}
