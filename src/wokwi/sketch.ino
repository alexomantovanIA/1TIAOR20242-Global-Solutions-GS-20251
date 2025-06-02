// === Bibliotecas necessárias ===
#include <WiFi.h>                  // Conexão Wi-Fi do ESP32
#include <PubSubClient.h>         // Biblioteca para MQTT
#include <Wire.h>                 // Comunicação I2C
#include <Adafruit_MPU6050.h>     // Biblioteca para sensor MPU6050
#include <Adafruit_Sensor.h>      // Base de sensores Adafruit
#include <LiquidCrystal_I2C.h>    // LCD com comunicação I2C

// === Parâmetros de rede Wi-Fi ===
const char* ssid = "Wokwi-GUEST";       // Nome da rede (SSID)
const char* password = "";              // Senha (Wokwi não exige)

// === Parâmetros do broker MQTT ===
const char* mqtt_server = "mqtt.eclipseprojects.io";   // Broker público gratuito
const char* mqtt_topic = "gs2025/grupo11/deslizamento";        // Tópico onde os dados serão publicados

// Objetos de rede
WiFiClient espClient;
PubSubClient client(espClient);

// === Inicialização de sensores ===
Adafruit_MPU6050 mpu;                   // Acelerômetro
const int POT_UMIDADE_PIN = 34;         // Potenciômetro 1 (simula umidade)
const int POT_CHUVA_PIN = 35;           // Potenciômetro 2 (simula chuva)

// === Inicialização do display LCD ===
LiquidCrystal_I2C lcd(0x27, 16, 2);     // Endereço I2C padrão do LCD 16x2

// === Função para conectar ao Wi-Fi ===
void setupWiFi() {
  WiFi.begin(ssid, password);           // Inicia conexão Wi-Fi
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado");
}

// === Função para reconectar ao MQTT ===
void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Reconectando MQTT...");
    if (client.connect("ESP32Client-GS2025")) {
      Serial.println(" conectado");
    } else {
      Serial.print(" falhou, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

// === Atualiza os dados no LCD ===
void updateLCD(int umidade, int chuva, float accZ) {
  lcd.clear();  // Limpa o display

  // Primeira linha: umidade (%) e chuva (mm/h)
  lcd.setCursor(0, 0);
  lcd.print("Umd:");
  lcd.print(umidade);
  lcd.print("% Chv:");
  lcd.print(chuva);

  // Segunda linha: aceleração Z (vibração vertical)
  lcd.setCursor(0, 1);
  lcd.print("Z Acc:");
  lcd.print(accZ, 1);   // Mostra com 1 casa decimal
  lcd.print("m/s2");
}

// === Setup principal (executado 1x ao ligar) ===
void setup() {
  Serial.begin(115200);       // Inicializa porta serial para debug
  Wire.begin(21, 22);         // Inicializa barramento I2C (pinos ESP32)

  // Inicializa o acelerômetro
  if (!mpu.begin()) {
    Serial.println("MPU6050 não encontrado!");
    while (1);  // Para tudo se não encontrar o sensor
  }

  // Configura sensibilidade do MPU6050
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);

  // Inicializa LCD
  lcd.init();
  lcd.backlight();  // Liga a luz de fundo

  // Conecta Wi-Fi e MQTT
  setupWiFi();
  client.setServer(mqtt_server, 1883);
  reconnectMQTT();
}

// === Loop principal (executado continuamente) ===
void loop() {
  if (!client.connected()) {
    reconnectMQTT();   // Verifica e reconecta ao MQTT se cair
  }
  client.loop();       // Mantém a conexão MQTT ativa

  // === Leitura dos sensores ===
  int rawUmidade = analogRead(POT_UMIDADE_PIN);   // Valor bruto do potenciômetro 1
  int rawChuva = analogRead(POT_CHUVA_PIN);       // Valor bruto do potenciômetro 2
  int umidade = map(rawUmidade, 0, 4095, 0, 100);  // Converte para % (0 a 100)
  int chuva = map(rawChuva, 0, 4095, 0, 150);      // Converte para mm/h (0 a 150)

  // Leitura do acelerômetro
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  float accZ = a.acceleration.z;   // Apenas o eixo Z (vertical)

  // === Monta payload JSON para o MQTT ===
  String payload = "{";
  payload += "\"umidade\":" + String(umidade) + ",";
  payload += "\"chuva\":" + String(chuva) + ",";
  payload += "\"acc_z\":" + String(accZ, 2);
  payload += "}";

  // === Publica os dados no broker MQTT ===
  client.publish(mqtt_topic, payload.c_str());

  // === Exibe dados no display LCD ===
  updateLCD(umidade, chuva, accZ);

  // === Mostra no Serial Monitor para debug ===
  Serial.println(payload);

  delay(2000);  // Aguarda 2 segundos antes da próxima leitura
}
