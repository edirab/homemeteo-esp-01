

#include <DHT_U.h>
#include <DHT.h>

 
#define DHTPIN 6     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)


struct luminance
{
    uint16_t r1;
    uint16_t r2;
};

struct meteo_data
{
    String temp, hum, soil;
    String lum1, lum2;
};

class MyMeteo
{
    public:
        explicit MyMeteo() : dht(DHTPIN, DHTTYPE) 
        {
            dht.begin();
        }

        void send_parsel()
        {
            get_DHT();
            get_soil();
            get_luminance();

            String parsel = data.temp + " " + data.hum + " " +
                data.soil + " " + data.lum1 + " " + data.lum2;
            
            Serial.println(parsel);
            return;
        }

    private:
        DHT dht;
        meteo_data data;

        /*
            1023 - разрыв цепи, абсолютно сухой грунт
            ~350-400 если окунуть в воду
        */
        void get_soil()
        {
            int a0 = analogRead(A0);

            if (a0 < 350)
                a0 = 350;
            
            // переворачиваем диапазон. 0 - сухая почва
            a0 = map(a0, 350, 1023, 100, 0);
            data.soil = String(a0);
            return;
        }

        /*
            0 - абсолютная темнота, 
            ~700-800 - направленная яркая лампа  
        */
        void get_luminance()
        {
            uint16_t lum_r1 = analogRead(A1);
            uint16_t lum_r2 = analogRead(A2);

            data.lum1 = String(lum_r1);
            data.lum2 = String(lum_r2);
            return;
        }

        void get_DHT()
        {
            float tempC = dht.readTemperature();
            float hum = dht.readHumidity();

            if (isnan(hum) )
            {
                Serial.println("Failed to read humidity from DHT sensor!");
                data.hum = String("-99");
            }
            else
            {
                data.hum = String(hum);
            }

            if (isnan(tempC))
            {
                Serial.println("Failed to read temp from DHT sensor!");
                data.temp = String("-99");
            }
            else
            {
                data.temp = String(tempC);
            }
            return;
        }
}; // end MyMeteo




MyMeteo mymeteo;

void setup()
{
    Serial.begin(115200);
}


void loop()
{
    mymeteo.send_parsel();

    delay(2000);
    return;
}