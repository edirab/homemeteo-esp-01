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

struct  UartData
{
	String hum, temp;
	String soil;
	String lum1, lum2;

	void clean()
	{
		hum = temp = soil = lum1 = lum2 = "";
	}
};



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
void publishTemperature(UartData& data) 
{
	// long now = millis();
	// if (client.isConnected() && (now - last > PUB_DELAY)) 
	// {
	// 	client.publish("home/temperature", String(random(20, 30)));
	// 	client.publish("home/humidity", String(random(40, 90)));
	// 	last = now;
	// }
	if (client.isConnected()) 
	{
		client.publish("home/temperature", data.temp);
		client.publish("home/humidity", data.hum);
		client.publish("home/soil", data.soil);
		client.publish("home/lum1", data.lum1);
		client.publish("home/lum2", data.lum2);
	}
	return;
}

/*
	Разбор строки вида
		23.4 50.4 1020 456 567
*/
void parseString(String& str, UartData& data)
{
	uint8_t i = 0; 
	uint8_t space_counter = 0;
	data.clean();

	for ( ; i < str.length(); i++)
	{
		char ch = str.charAt(i);
		if ( ch == ' ' )
		{
			space_counter++;
			continue;
		}

		switch (space_counter)
		{
		case 0:
			data.temp += ch;
			break;
		case 1:
			data.hum += ch;
			break;
		case 2:
			data.soil += ch;
			break;
		case 3:
			data.lum1 += ch;
			break;
		case 4:
			data.lum2 += ch;
			break;			
		default:
			break;
		}
	}
}


void loop() 
{
	UartData uart_parcel;

	client.loop();

	if (Serial.available())
	{
		String s = Serial.readString();
		parseString(s, uart_parcel);
		publishTemperature(uart_parcel);
	}
	delay(20);

	return;
}
