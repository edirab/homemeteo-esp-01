#include "Arduino.h"
#include "EspMQTTClient.h" /* https://github.com/plapointe6/EspMQTTClient */
                           /* https://github.com/knolleary/pubsubclient */
#define PUB_DELAY (5 * 1000) /* 5 seconds */

EspMQTTClient client(
  "DuckNet_2G",
  "duckyduck",

  "192.168.1.75",
  "esp", 	// login
  "esp",	// pswd
  "esp_02" // edirab-vrxq8g
);

void setup() 
{
	Serial.begin(115200);
}

void onConnectionEstablished() 
{
	client.subscribe("base/relay/led1", [] (const String &payload)  
		{
			Serial.println(payload);
		}
	);
}

long last = 0;
void publishTemperature() 
{
	long now = millis();
	if (client.isConnected() && (now - last > PUB_DELAY)) 
	{
		client.publish("home/temperature", String(random(20, 30)));
		client.publish("home/humidity", String(random(40, 90)));
		last = now;
	}
	return;
}

void loop() 
{
	client.loop();
	publishTemperature();
}
