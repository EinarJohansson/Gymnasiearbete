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

// Initierar ett Klient objekt.
Klient klient(PORT);

// setup funktionen körs en gång innan loopen:
void setup() {
    Serial.begin(BAUD);
    klient.anslut("SSID", "PASS");
}

// loop funktionen kallas kontinuerligt:
void loop()
{
    // Börja lyssna efter UDP-meddelanden.
    klient.lyssna();
}
