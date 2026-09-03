#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_SSD1306.h>

// =====================================================
// CAREMATRIX - SMART PATIENT MONITORING SYSTEM
// =====================================================

// ---------------- Wi-Fi / Backend ----------------

const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";

const char* BACKEND_URL =
    "http://host.wokwi.internal:5000/sensor-data";

// ---------------- Pin Configuration ----------------

#define DHT_PIN       4
#define DHT_TYPE      DHT22

#define I2C_SDA       21
#define I2C_SCL       22

#define BUZZER_PIN    25
#define GREEN_LED     26
#define RED_LED       27

#define FALL_BUTTON   18

// ---------------- Sensors ----------------

DHT dht(DHT_PIN, DHT_TYPE);

Adafruit_MPU6050 mpu;

// ---------------- OLED ----------------

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    &Wire,
    -1
);

// =====================================================
// DEMO MODES
// =====================================================

enum DemoMode {
  NORMAL_MODE,
  ABNORMAL_MODE,
  FALL_MODE
};

DemoMode currentMode = NORMAL_MODE;

// ---------------- Timing ----------------

unsigned long lastSend = 0;

const unsigned long SEND_INTERVAL = 3000;

// ---------------- Button ----------------

bool lastButtonState = HIGH;

// ---------------- Patient Data ----------------

float temperature = 36.5;
int heartRate = 75;
int spo2 = 98;

bool fallDetected = false;

// =====================================================
// FUNCTION DECLARATIONS
// =====================================================

void readSensors();
void updateOutputs();
void updateOLED();
void printReadings();
void sendToBackend();

// =====================================================
// SETUP
// =====================================================

void setup() {

  Serial.begin(115200);

  delay(1000);

  // ---------------- GPIO ----------------

  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);

  pinMode(FALL_BUTTON, INPUT_PULLUP);

  digitalWrite(GREEN_LED, LOW);
  digitalWrite(RED_LED, LOW);
  digitalWrite(BUZZER_PIN, LOW);

  // ---------------- DHT22 ----------------

  dht.begin();

  // ---------------- I2C ----------------

  Wire.begin(I2C_SDA, I2C_SCL);

  // =================================================
  // MPU6050
  // =================================================

  Serial.println("Initializing MPU6050...");

  if (!mpu.begin()) {

    Serial.println(
        "WARNING: MPU6050 not detected."
    );

  } else {

    Serial.println(
        "MPU6050 connected."
    );

    mpu.setAccelerometerRange(
        MPU6050_RANGE_8_G
    );

    mpu.setGyroRange(
        MPU6050_RANGE_500_DEG
    );

    mpu.setFilterBandwidth(
        MPU6050_BAND_21_HZ
    );
  }

  // =================================================
  // OLED
  // =================================================

  Serial.println("Initializing OLED...");

  if (!display.begin(
          SSD1306_SWITCHCAPVCC,
          0x3C)) {

    Serial.println(
        "WARNING: OLED not detected."
    );

  } else {

    Serial.println(
        "OLED connected."
    );

    display.clearDisplay();

    display.setTextColor(
        SSD1306_WHITE
    );

    display.setTextSize(1);

    display.setCursor(0, 0);

    display.println("CAREMATRIX");

    display.println();

    display.println(
        "Smart Patient"
    );

    display.println(
        "Monitoring System"
    );

    display.println();

    display.println(
        "Starting..."
    );

    display.display();

    delay(2000);
  }

  // =================================================
  // WIFI
  // =================================================

  Serial.println();
  Serial.println("Connecting to Wi-Fi...");

  WiFi.begin(
      WIFI_SSID,
      WIFI_PASSWORD
  );

  unsigned long wifiStart = millis();

  while (
      WiFi.status() != WL_CONNECTED &&
      millis() - wifiStart < 15000) {

    delay(500);

    Serial.print(".");
  }

  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {

    Serial.println(
        "Wi-Fi connected!"
    );

    Serial.print(
        "ESP32 IP: "
    );

    Serial.println(
        WiFi.localIP()
    );

  } else {

    Serial.println(
        "Wi-Fi connection failed."
    );
  }

  // =================================================
  // STARTUP MESSAGE
  // =================================================

  Serial.println();

  Serial.println(
      "================================="
  );

  Serial.println(
      "          CAREMATRIX"
  );

  Serial.println(
      " Smart Patient Monitoring System"
  );

  Serial.println(
      "================================="
  );

  Serial.println();

  Serial.println(
      "ESP32 READY"
  );

  Serial.println();

  Serial.println(
      "BUTTON PRESENTATION MODE"
  );

  Serial.println(
      "PRESS BUTTON TO CHANGE MODE"
  );

  Serial.println(
      "NORMAL -> ABNORMAL -> FALL -> NORMAL"
  );

  Serial.println();

  // Start in NORMAL mode
  currentMode = NORMAL_MODE;

  fallDetected = false;

  // Read initial button state
  lastButtonState =
      digitalRead(FALL_BUTTON);
}

// =====================================================
// MAIN LOOP
// =====================================================

void loop() {

  // -------------------------------------------------
  // Read push button
  // -------------------------------------------------

  bool buttonState =
      digitalRead(FALL_BUTTON);

  // Detect a NEW button press
  // HIGH -> LOW means button was pressed

  if (
      lastButtonState == HIGH &&
      buttonState == LOW) {

    // ===============================================
    // NORMAL -> ABNORMAL
    // ===============================================

    if (
        currentMode == NORMAL_MODE) {

      currentMode =
          ABNORMAL_MODE;

      fallDetected = false;

      Serial.println();

      Serial.println(
          "========== BUTTON PRESSED =========="
      );

      Serial.println(
          "MODE CHANGED:"
      );

      Serial.println(
          "NORMAL -> ABNORMAL"
      );

      Serial.println(
          "===================================="
      );
    }

    // ===============================================
    // ABNORMAL -> FALL
    // ===============================================

    else if (
        currentMode == ABNORMAL_MODE) {

      currentMode =
          FALL_MODE;

      fallDetected = true;

      Serial.println();

      Serial.println(
          "========== BUTTON PRESSED =========="
      );

      Serial.println(
          "MODE CHANGED:"
      );

      Serial.println(
          "ABNORMAL -> FALL"
      );

      Serial.println(
          "FALL / EMERGENCY DETECTED!"
      );

      Serial.println(
          "===================================="
      );
    }

    // ===============================================
    // FALL -> NORMAL
    // ===============================================

    else if (
        currentMode == FALL_MODE) {

      currentMode =
          NORMAL_MODE;

      fallDetected = false;

      Serial.println();

      Serial.println(
          "========== BUTTON PRESSED =========="
      );

      Serial.println(
          "MODE CHANGED:"
      );

      Serial.println(
          "FALL -> NORMAL"
      );

      Serial.println(
          "PATIENT SAFE"
      );

      Serial.println(
          "===================================="
      );
    }

    // Simple button debounce
    delay(250);
  }

  // Save current button state
  lastButtonState =
      buttonState;

  // -------------------------------------------------
  // Read sensors
  // -------------------------------------------------

  readSensors();

  // -------------------------------------------------
  // Update hardware outputs
  // -------------------------------------------------

  updateOutputs();

  // -------------------------------------------------
  // Update OLED
  // -------------------------------------------------

  updateOLED();

  // -------------------------------------------------
  // Print readings to Serial Monitor
  // -------------------------------------------------

  printReadings();

  // -------------------------------------------------
  // Send data to Flask backend
  // -------------------------------------------------

  if (
      millis() - lastSend >=
      SEND_INTERVAL) {

    lastSend = millis();

    sendToBackend();
  }

  delay(200);
}

// =====================================================
// READ SENSORS
// =====================================================

void readSensors() {

  // -------------------------------------------------
  // Read DHT22 temperature
  // -------------------------------------------------

  float dhtTemperature =
      dht.readTemperature();

  if (!isnan(dhtTemperature)) {

    temperature =
        dhtTemperature;
  }

  // -------------------------------------------------
  // Simulated patient readings
  // -------------------------------------------------

  // There is no physical heart-rate or SpO2
  // sensor in the current Wokwi circuit.
  //
  // Therefore these values are generated for
  // demonstration purposes.

  if (
      currentMode == NORMAL_MODE) {

    temperature = 36.5;

    heartRate =
        72 +
        (millis() / 1000) % 10;

    spo2 = 98;
  }

  else if (
      currentMode == ABNORMAL_MODE) {

    temperature = 38.7;

    heartRate =
        115 +
        (millis() / 1000) % 10;

    spo2 = 91;
  }

  else {

    temperature = 38.9;

    heartRate = 124;

    spo2 = 89;
  }

  // -------------------------------------------------
  // Read MPU6050
  // -------------------------------------------------

  sensors_event_t acceleration;
  sensors_event_t gyro;
  sensors_event_t temp;

  if (mpu.begin()) {

    mpu.getEvent(
        &acceleration,
        &gyro,
        &temp
    );
  }
}

// =====================================================
// UPDATE LED + BUZZER
// =====================================================

void updateOutputs() {

  // -------------------------------------------------
  // NORMAL
  // -------------------------------------------------

  if (
      currentMode == NORMAL_MODE) {

    digitalWrite(
        GREEN_LED,
        HIGH
    );

    digitalWrite(
        RED_LED,
        LOW
    );

    noTone(
        BUZZER_PIN
    );
  }

  // -------------------------------------------------
  // ABNORMAL
  // -------------------------------------------------

  else if (
      currentMode == ABNORMAL_MODE) {

    digitalWrite(
        GREEN_LED,
        LOW
    );

    digitalWrite(
        RED_LED,
        HIGH
    );

    // Beeping alarm
    if (
        (millis() / 1000) % 2 == 0) {

      tone(
          BUZZER_PIN,
          1200
      );

    } else {

      noTone(
          BUZZER_PIN
      );
    }
  }

  // -------------------------------------------------
  // FALL / EMERGENCY
  // -------------------------------------------------

  else {

    digitalWrite(
        GREEN_LED,
        LOW
    );

    digitalWrite(
        RED_LED,
        HIGH
    );

    // Continuous emergency alarm
    tone(
        BUZZER_PIN,
        2000
    );
  }
}

// =====================================================
// UPDATE OLED
// =====================================================

void updateOLED() {

  display.clearDisplay();

  display.setTextColor(
      SSD1306_WHITE
  );

  display.setTextSize(1);

  // -------------------------------------------------
  // Header
  // -------------------------------------------------

  display.setCursor(
      0,
      0
  );

  display.println(
      "CAREMATRIX"
  );

  display.drawLine(
      0,
      10,
      127,
      10,
      SSD1306_WHITE
  );

  // -------------------------------------------------
  // Status
  // -------------------------------------------------

  display.setCursor(
      0,
      14
  );

  if (
      currentMode == NORMAL_MODE) {

    display.println(
        "STATUS: NORMAL"
    );

  }

  else if (
      currentMode == ABNORMAL_MODE) {

    display.println(
        "STATUS: ABNORMAL"
    );

  }

  else {

    display.println(
        "STATUS: FALL!"
    );
  }

  // -------------------------------------------------
  // Temperature
  // -------------------------------------------------

  display.setCursor(
      0,
      27
  );

  display.print(
      "Temp: "
  );

  display.print(
      temperature,
      1
  );

  display.println(
      " C"
  );

  // -------------------------------------------------
  // Heart Rate
  // -------------------------------------------------

  display.setCursor(
      0,
      38
  );

  display.print(
      "Heart: "
  );

  display.print(
      heartRate
  );

  display.println(
      " BPM"
  );

  // -------------------------------------------------
  // SpO2
  // -------------------------------------------------

  display.setCursor(
      0,
      49
  );

  display.print(
      "SpO2: "
  );

  display.print(
      spo2
  );

  display.println(
      " %"
  );

  display.display();
}

// =====================================================
// SERIAL MONITOR READINGS
// =====================================================

void printReadings() {

  Serial.println();

  Serial.println(
      "----------- PATIENT DATA -----------"
  );

  // -------------------------------------------------
  // Mode
  // -------------------------------------------------

  if (
      currentMode == NORMAL_MODE) {

    Serial.println(
        "MODE: NORMAL"
    );

  }

  else if (
      currentMode == ABNORMAL_MODE) {

    Serial.println(
        "MODE: ABNORMAL"
    );

  }

  else {

    Serial.println(
        "MODE: FALL / EMERGENCY"
    );
  }

  // -------------------------------------------------
  // Temperature
  // -------------------------------------------------

  Serial.print(
      "Temperature: "
  );

  Serial.print(
      temperature,
      2
  );

  Serial.println(
      " °C"
  );

  // -------------------------------------------------
  // Heart Rate
  // -------------------------------------------------

  Serial.print(
      "Heart Rate: "
  );

  Serial.print(
      heartRate
  );

  Serial.println(
      " BPM"
  );

  // -------------------------------------------------
  // SpO2
  // -------------------------------------------------

  Serial.print(
      "SpO2: "
  );

  Serial.print(
      spo2
  );

  Serial.println(
      " %"
  );

  // -------------------------------------------------
  // Fall Status
  // -------------------------------------------------

  Serial.print(
      "Fall Status: "
  );

  if (
      fallDetected) {

    Serial.println(
        "FALL DETECTED"
    );

  } else {

    Serial.println(
        "SAFE"
    );
  }

  Serial.println(
      "------------------------------------"
  );
}

// =====================================================
// SEND DATA TO FLASK BACKEND
// =====================================================

void sendToBackend() {

  // -------------------------------------------------
  // Check Wi-Fi
  // -------------------------------------------------

  if (
      WiFi.status() != WL_CONNECTED) {

    Serial.println(
        "Wi-Fi not connected. Data not sent."
    );

    return;
  }

  Serial.println();

  Serial.println(
      "DEBUG: Sending sensor data..."
  );

  Serial.println(
      "Sending to LOCAL BACKEND..."
  );

  Serial.println(
      BACKEND_URL
  );

  // -------------------------------------------------
  // HTTP Client
  // -------------------------------------------------

  HTTPClient http;

  http.begin(
      BACKEND_URL
  );

  http.addHeader(
      "Content-Type",
      "application/json"
  );

  // -------------------------------------------------
  // Determine mode
  // -------------------------------------------------

  String mode;

  if (
      currentMode == NORMAL_MODE) {

    mode = "NORMAL";

  }

  else if (
      currentMode == ABNORMAL_MODE) {

    mode = "ABNORMAL";

  }

  else {

    // Backend understands FALL through
    // fall=true + mode=ABNORMAL

    mode = "ABNORMAL";
  }

  // -------------------------------------------------
  // Create JSON
  // -------------------------------------------------

  String jsonData = "{";

  jsonData +=
      "\"temperature\":" +
      String(
          temperature,
          1
      );

  jsonData +=
      ",\"heart_rate\":" +
      String(
          heartRate
      );

  jsonData +=
      ",\"spo2\":" +
      String(
          spo2
      );

  jsonData +=
      ",\"fall\":" +
      String(
          fallDetected
              ? "true"
              : "false"
      );

  jsonData +=
      ",\"mode\":\"" +
      mode +
      "\"";

  jsonData += "}";

  // -------------------------------------------------
  // Print JSON
  // -------------------------------------------------

  Serial.println(
      "Sending:"
  );

  Serial.println(
      jsonData
  );

  // -------------------------------------------------
  // POST
  // -------------------------------------------------

  int responseCode =
      http.POST(
          jsonData
      );

  Serial.print(
      "HTTP Response Code: "
  );

  Serial.println(
      responseCode
  );

  // -------------------------------------------------
  // Server Response
  // -------------------------------------------------

  if (
      responseCode > 0) {

    String response =
        http.getString();

    Serial.println(
        "Server response:"
    );

    Serial.println(
        response
    );

    if (
        responseCode == 200) {

      Serial.println(
          "SUCCESS: Data sent to local backend!"
      );
    }

  } else {

    Serial.println(
        "ERROR: Failed to connect to Flask backend."
    );
  }

  // -------------------------------------------------
  // Close HTTP connection
  // -------------------------------------------------

  http.end();
}