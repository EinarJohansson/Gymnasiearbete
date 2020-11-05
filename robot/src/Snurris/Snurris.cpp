#define LEFT 0
#define RIGHT 180

#include "Snurris.hpp"
#include "../Distans/Distans.hpp"

int pos = LEFT;

void snurra(Servo &servo, Klient &klient) {
    if (!servo.attached())
        return;

    if (pos == LEFT)
    {
        for (int vinkel = LEFT; vinkel < RIGHT; vinkel += 1)
        {
            // Snurra 1°
            servo.write(vinkel);
            pos +=1;

            // Vänta på att den ska ha snurrat 1°
            delay(50);
            
            skanna(klient, String(vinkel), "0", "0");     
        }
        
    } else if (pos == RIGHT)
    {
        for (int vinkel = RIGHT; vinkel > LEFT; vinkel -= 1)
        {
            // Snurra 1°
            servo.write(vinkel);
            pos -= 1;

            // Vänta på att den ska ha snurrat 1°
            delay(50);

            skanna(klient, String(vinkel), "0", "0");    
        }
    }
    String stig = klient.lyssna();
    Serial.println(stig);
}

void skanna(Klient &klient, String vinkel, String stegX, String stegY)
{
    String dist = String(distans());

    String meddelande = String(dist + ";" + vinkel + ";" + stegX + ";" + stegY);
    
    // Bygger om strängen till en char pekare så den kan passas till klient.prata
    char *formatterad = const_cast<char*>(meddelande.c_str());
    
    klient.prata(formatterad);
}
