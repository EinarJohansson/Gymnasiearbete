#include <Arduino.h>
#include <ESP8266WiFi.h>
#include "Klient.hpp"

// Konstruktören för Klient strukturen.
Klient::Klient(int _port): port(_port)
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
}

// Börja lyssna efter meddelanden.
void Klient::lyssna()
{
    Udp.begin(port);
    Serial.printf("Lyssnar på ip-addressen %s, UDP port %d\n", WiFi.localIP().toString().c_str(), port);
}