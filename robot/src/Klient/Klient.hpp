#include <WiFiUdp.h>
#pragma once

struct Klient 
{
    Klient(int);
    void anslut(char*, char*);
    void lyssna();
    int prata(char*);
    int prata(char*, IPAddress, int);

    private:
        char inkommandePaket[UDP_TX_PACKET_MAX_SIZE + 1]; 
        WiFiUDP Udp;
        int port;
};