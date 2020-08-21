#include <WiFiUdp.h>
#pragma once

struct Klient 
{
    Klient(int);
    void anslut(char*, char*);
    void lyssna();

    private:
        WiFiUDP Udp;
        int port;
};