#define LEFT 0
#define RIGHT 180

#include "Snurris.hpp"
#include "../Distans/Distans.hpp"
#include "../DCMDriverL293D/DCMDriverL293D.hpp"
#include "../config.hpp"

int pos = LEFT;
DCMDriverL293D DCmotorer(DCMOTORDRIVERA_PIN_ENABLE1,DCMOTORDRIVERA_PIN_IN1,DCMOTORDRIVERA_PIN_IN2,DCMOTORDRIVERA_PIN_ENABLE2,DCMOTORDRIVERA_PIN_IN3,DCMOTORDRIVERA_PIN_IN4);

bool hanteraMeddelande(Servo &servo, Klient &klient)
{
    int vinkelsumma = 0;
    while(true)
    {
        yield();
        String stig = klient.lyssna();
        Serial.println(stig);
        if (stig.equals("slut")) return false;

        int splitIndex = stig.indexOf(';');

        int vinkel = stig.substring(0, splitIndex).toInt();
        int stig_len = stig.substring(splitIndex+1).toInt();

        vinkelsumma += vinkel;

        Serial.println(vinkel);
        Serial.println(stig_len);

        DCmotorer.setMotorA(1000,1);
        DCmotorer.setMotorB(1000,1);

        delay(500);

        //Stop both motors
        DCmotorer.stopMotors();
    }  
    // sätt servo motorn i start läget
    servo.write(LEFT);
    pos = 0;

    // Sväng tillbaka roboten till startläget 
    vinkelsumma %= 360;

    return true;
}

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
            delay(25);
            
            skanna(klient, String(vinkel), "0", "0");
            bool reset = hanteraMeddelande(servo, klient);

            Serial.println(reset);
            if (reset) break;
        }  
    } else if (pos == RIGHT)
    {
        for (int vinkel = RIGHT; vinkel > LEFT; vinkel -= 1)
        {
            // Snurra 1°
            servo.write(vinkel);
            pos -= 1;

            // Vänta på att den ska ha snurrat 1°
            delay(25);

            skanna(klient, String(vinkel), "0", "0");
            bool reset = hanteraMeddelande(servo, klient);

            Serial.println(reset);
            if (reset) break;
        }
    }
}

void skanna(Klient &klient, String vinkel, String stegX, String stegY)
{
    String dist = String(distans());

    String meddelande = String(dist + ";" + vinkel + ";" + stegX + ";" + stegY);
    
    // Bygger om strängen till en char pekare så den kan passas till klient.prata
    char *formatterad = const_cast<char*>(meddelande.c_str());
    
    klient.prata(formatterad);
}
