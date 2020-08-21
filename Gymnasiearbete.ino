/*
Einar Johansson, Albert Johansson, Ludvig Bergstrand
TE18A
Gymnasiearbete
*/

// ESP8266 baudrate ligger på 9600 bits-per-sekund.
#define BAUD 9600
#define PORT 4210

// importerar vår kod. 
#include "src/Distans/Distans.hpp"
#include "src/Klient/Klient.hpp" 

// Initierar ett Klient objekt.
Klient klient(PORT);

// setup funktionen körs en gång innan loopen:
void setup() {
    Serial.begin(BAUD);
    klient.anslut("SSID", "PASS");
    klient.lyssna();
}

// loop funktionen kallas kontinuerligt:
void loop()
{

}