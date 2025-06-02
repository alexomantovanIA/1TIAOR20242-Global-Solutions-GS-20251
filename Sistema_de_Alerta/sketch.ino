#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <MPU6050.h>

// WiFi
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// MQTT Broker
const char* mqtt_server = "broker.hivemq.com";
WiFiClient espClient;
PubSubClient client(espClient);

// MPU6050
MPU6050 mpu;

// Pinos dos potenciômetros
const int potPin1 = 34;
const int potPin2 = 35;

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  mpu.initialize();

  // Conectar WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado");

  // Configurar MQTT
  client.setServer(mqtt_server, 1883);

  // Conectar MQTT
  while (!client.connected()) {
    Serial.print("Conectando MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println(" conectado");
    } else {
      Serial.print(" falhou, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Ler potenciômetros
  int potValue1 = analogRead(potPin1);
  int potValue2 = analogRead(potPin2);

  // Ler MPU6050
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // Montar string JSON de dados
  String payload = "{";
  payload += "\"pot1\":" + String(potValue1) + ",";
  payload += "\"pot2\":" + String(potValue2) + ",";
  payload += "\"ax\":" + String(ax) + ",";
  payload += "\"ay\":" + String(ay) + ",";
  payload += "\"az\":" + String(az);
  payload += "}";

  // Publicar MQTT
  client.publish("esp32/sensores", payload.c_str());

  // Debug
  Serial.println(payload);

  delay(2000); // a cada 2 segundos
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Reconectando MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println(" conectado");
    } else {
      Serial.print(" falhou, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

