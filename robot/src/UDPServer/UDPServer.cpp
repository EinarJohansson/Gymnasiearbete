#include <Arduino.h>
#include <ESP8266WiFi.h>
#include "UDPServer.hpp"

// Konstruktören för UDPServer strukturen.
UDPServer::UDPServer(int _port) : port(_port)
{
}

// Funktion för att ansluta roboten till ett wifi-nätverk.
void UDPServer::anslut(char* ssid, char* pass)
{
    // Gör inte en AP!
    WiFi.mode(WIFI_STA);

    // Initiera anslutningen.
    WiFi.begin(ssid, pass);

    // Väntar på att roboten ska anluta.
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("Kunde inte ansluta, försöker igen...");
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
void UDPServer::lyssna()
{
    // Kolla om vi har fått ett paket.
    int packetSize = Udp.parsePacket();
    if (packetSize)
    {
        Serial.printf("Tog emot %d bytes från %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
        
        // Skriv över bufferten med meddelandet.
        int len = Udp.read(inkommandePaket, UDP_TX_PACKET_MAX_SIZE);
        inkommandePaket[len] = 0;
        
        Serial.printf("UDP paketet innehåller: %s\n", inkommandePaket);
        
        prata("test\r\n");
    }
}

// Skicka meddelandet till en avsändare som etablerat kontakt med roboten.
int UDPServer::prata(char* meddelande)
{    
    Serial.printf("Skickar till -> %s:%d\n", Udp.remoteIP().toString().c_str(), Udp.remotePort());

    // Starta en kontakt
    if (Udp.beginPacket(Udp.remoteIP(), Udp.remotePort()))
    {
        // Skicka meddelandet
        Udp.write(meddelande);
        return Udp.endPacket();
    } else return 0;
}

// Skicka meddelandet och etablera kontakt med lyssnaren.
int UDPServer::prata(char* meddelande, IPAddress ip, int port)
{
    Serial.printf("Skickar till -> %s:%d\n", ip.toString().c_str(), port);
    
    // Starta en kontakt
    if (Udp.beginPacket(ip, port))
    {
        // Skicka meddelandet
        Udp.write(meddelande);
        return Udp.endPacket();
    } else return 0;
}