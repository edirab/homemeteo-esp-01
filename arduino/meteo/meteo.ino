

#include <DHT_U.h>
#include <DHT.h>

 
#define DHTPIN 6     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)

#define LED_WIFI 2
#define LED_MQTT 3
#define LED_SOIL 4

#define PERIOD 2000 // msec

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

        void check_connection()
        {

            uint64_t timest = millis();
            uint64_t now_;

            do 
            {
                now_ = millis();
                
                if (Serial.available())
                {
                    String s1 = Serial.readString();
                    /*
                        Сделано с целью избежать проблем с разными символами окончания строк \r\n vs \n
                        у ESP 01 и терминала VS Code
                    */
                    if (s1.startsWith("WIFI_FAIL") )
                    {
                        digitalWrite(LED_WIFI, HIGH);
                    } 
                    else if (s1.startsWith("WIFI_OK"))
                    {
                        digitalWrite(LED_WIFI, LOW);
                    } 
                    else if (s1.startsWith("MQTT_FAIL"))
                    {
                        digitalWrite(LED_MQTT, HIGH);
                    }
                    else if ( s1.startsWith("MQTT_OK"))
                    {
                        digitalWrite(LED_MQTT, LOW);
                    }
                    Serial.print(s1);
                }

            }
            while (now_ - timest < PERIOD );
            return;
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
    pinMode(LED_WIFI, OUTPUT);
    pinMode(LED_MQTT, OUTPUT);
    Serial.begin(115200);
}


void loop()
{
    mymeteo.send_parsel();
    mymeteo.check_connection();

    return;
}
