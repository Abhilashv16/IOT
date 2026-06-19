#include <WiFi.h>

const char* ssid = "Abhilash";
const char* password = "Abhi.142..";

void setup() {

  Serial.begin(115200);

  delay(1000);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);

    Serial.print(".");
  }

  Serial.println("\nConnected");
}

void loop() {

  int rssi = WiFi.RSSI();

  Serial.println(rssi);

  delay(3000);
}