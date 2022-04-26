#include "Arduino.h"
#include "EspMQTTClient.h" /* https://github.com/plapointe6/EspMQTTClient */
                           /* https://github.com/knolleary/pubsubclient */
#define PUB_DELAY (5 * 1000) /* 5 seconds */

#define MSG_PREFIX "METEO_"
#define WIFI_FAIL "1"
#define WIFI_OK	"2"
#define MQTT_FAIL "3"
#define MQTT_OK "4"

EspMQTTClient client(
  "DuckNet_2G",
  "duckyduck",
  //"poco",
  //"pocopoco",

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

bool wifi_is_connected = true;
bool mqtt_is_connected = true;

void setup() 
{
	Serial.begin(115200);
}

void onConnectionEstablished() 
{
	// wifi_is_connected = true;
	// mqtt_is_connected = true;

	client.subscribe("base/relay/led1", [] (const String &payload)  
		{
			//Serial.println(payload);
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
	data.clean();
	if (str.charAt(0) != 'A') 
	{
		uint8_t i = 0; 
		uint8_t space_counter = 0;
		
		// eliminating \r\n characters
		for ( ; i < str.length() - 2; i++)
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
	return;
}

void send_command(const String& command, const String& expected_ack)
{
	bool got_ack = false;

	while(!got_ack)
	{
		Serial.print(MSG_PREFIX);
		Serial.println(command);
		delay(5);

		if (Serial.available())
		{
			String s = Serial.readString();
			if (s.startsWith(expected_ack))
			{
				got_ack = true;
			}
		}
		delay(10);
	}
	return;
}


void check_connection()
{
	// зажечь зелёный светодиод
	if ( !client.isWifiConnected() && wifi_is_connected)
	{
		wifi_is_connected = false;
		send_command(WIFI_FAIL, "ACK_1");
	}
	// погасить зелёный светодиод
	else if ( client.isWifiConnected() && !wifi_is_connected)
	{
		wifi_is_connected = true;
		send_command(WIFI_OK, "ACK_2");
	}
	// зажечь красный светодиод
	if ( !client.isMqttConnected() && mqtt_is_connected)
	{
		mqtt_is_connected = false;
		send_command(MQTT_FAIL, "ACK_3");
	}
	// погасить красный светодиод
	else if ( client.isMqttConnected() && !mqtt_is_connected)
	{
		mqtt_is_connected = true;
		send_command(MQTT_OK, "ACK_4");
	}
	return;
}


void loop() 
{
	UartData uart_parcel;
	check_connection();

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
