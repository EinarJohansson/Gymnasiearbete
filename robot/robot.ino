/*
Einar Johansson, Albert Johansson, Ludvig Bergstrand
TE18A
Gymnasiearbete
*/

#define BAUD 9600
#define PORT 8888

// importerar vår kod. 
#include "src/Distans/Distans.hpp"
#include "src/UDPServer/UDPServer.hpp" 

// Initierar ett UDPServer objekt.
UDPServer server(PORT);

// setup funktionen körs en gång innan loopen:
void setup() {
    Serial.begin(BAUD);
    server.anslut("SSID", "PASS");
}

// loop funktionen kallas kontinuerligt:
void loop()
{
    // Börja lyssna efter UDP-meddelanden.
    server.lyssna();
}
