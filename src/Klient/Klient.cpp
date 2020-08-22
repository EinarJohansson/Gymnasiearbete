#include <Arduino.h>
#include <ESP8266WiFi.h>
#include "Klient.hpp"

// Konstruktören för Klient strukturen.
Klient::Klient(int _port) : port(_port)
{
}

// Funktion för att ansluta roboten till ett wifi-nätverk.
void Klient::anslut(char* ssid, char* pass)
{
    // Initiera anslutningen.
    WiFi.begin(ssid, pass);

    // Väntar på att roboten ska anluta.
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("Kunde inte ansluta, försöker igen...");
        Serial.println(port);
        delay(500);
    }

    // Roboten är nu ansluten!
    Serial.println("Ansluten!");
    Serial.println(WiFi.localIP());

    // Förbered inför att börja lyssna efter meddelanden.
    Udp.begin(port);
    Serial.printf("Lyssnar på ip-addressen %s, UDP port %d\n", WiFi.localIP().toString().c_str(), port);
}

// Börja lyssna efter meddelanden.
void Klient::lyssna()
{
    // Kolla om vi har fått ett paket.
    int packetSize = Udp.parsePacket();
    if (packetSize)
    {
        Serial.printf("Tog emot %d bytes från %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
        
        // Skriv över bufferten med meddelandet om det inte är tomt.
        int len = Udp.read(inkommandePaket, 255);
        if (len > 0)
            inkommandePaket[len] = 0;
        
        Serial.printf("UDP paketet innehåller: %s\n", inkommandePaket);
    }
}