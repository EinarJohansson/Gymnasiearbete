/*
Einar Johansson, Albert Johansson, Ludvig Bergstrand
TE18A
Gymnasiearbete
*/

#define BAUD 9600
#define PORT 8888

// importerar vår kod. 
#include "src/Distans/Distans.hpp"
#include "src/Klient/Klient.hpp" 

// Serverns ip
IPAddress IP(8, 8, 8, 8);

// Initierar ett Klient objekt.
Klient klient(IP, PORT);

// setup funktionen körs en gång innan loopen:
void setup() {
    Serial.begin(BAUD);
    klient.anslut("SSID", "PASS");
}

// loop funktionen kallas kontinuerligt:
void loop()
{
    // Börja lyssna efter UDP-meddelanden.
    // klient.lyssna();
    klient.prata("Är du där?");
    delay(1000);
}
