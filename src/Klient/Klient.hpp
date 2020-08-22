#include <WiFiUdp.h>
#pragma once

struct Klient 
{
    Klient(int);
    void anslut(char*, char*);
    void lyssna();

    private:
        char inkommandePaket[255]; 
        WiFiUDP Udp;
        int port;
};