
#include <DHT_U.h>
#include <DHT.h>

 
#define DHTPIN 6     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
 
 
DHT dht(DHTPIN, DHTTYPE);
 
void setup() 
{
  Serial.begin(9600); 
  dht.begin();
}
 
void loop() 
{
  // Wait a few seconds between measurements.
  delay(2000);
 
  float hum = dht.readHumidity();
  // Read temperature as Celsius
  float tempC = dht.readTemperature();
 
  // Check if readings have failed
  if (isnan(hum) || isnan(tempC)) 
  {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }     
 
  Serial.print("Humidity: "); 
  Serial.print(hum);
  Serial.print(" %\t");
  Serial.print("Temperature: "); 
  Serial.print(tempC);
  Serial.println(" *C ");
 
}