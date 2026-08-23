#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

// =================================
// Wi-Fi
// =================================

const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";

// Python Flask backend
const char* SERVER_URL =
    "http://host.wokwi.internal:5000/sensor-data";


// =================================
// Sensor Pins
// =================================

#define DHT_PIN 4
#define DHT_TYPE DHT22

#define FALL_PIN 5
#define MODE_BUTTON_PIN 18


// =================================
// DHT Sensor
// =================================

DHT dht(DHT_PIN, DHT_TYPE);


// =================================
// Patient Mode
// false = NORMAL
// true  = ABNORMAL
// =================================

bool abnormalMode = false;


// =================================
// Button State
// =================================

bool lastButtonState = HIGH;


// =================================
// SEND DATA TO PYTHON BACKEND
// =================================

void sendSensorData(
    float temperature,
    int heartRate,
    int spo2,
    bool fallDetected
) {
  Serial.println("DEBUG: Entering sendSensorData()");

  if (WiFi.status() != WL_CONNECTED) {

    Serial.println("Wi-Fi not connected!");

    return;
  }

  HTTPClient http;

  http.begin(SERVER_URL);

  http.addHeader(
      "Content-Type",
      "application/json"
  );


  // Create JSON data

  String jsonData = "{";

  jsonData += "\"temperature\":";
  jsonData += String(temperature, 1);

  jsonData += ",\"heart_rate\":";
  jsonData += String(heartRate);

  jsonData += ",\"spo2\":";
  jsonData += String(spo2);

  jsonData += ",\"fall\":";
  jsonData += fallDetected ? "true" : "false";

  jsonData += "}";


  // Display JSON

  Serial.println();
  Serial.println("Sending data to Python backend:");

  Serial.println(jsonData);


  // Send HTTP POST

  int httpResponseCode =
      http.POST(jsonData);


  Serial.print("HTTP Response Code: ");

  Serial.println(httpResponseCode);


  // Backend response

  if (httpResponseCode > 0) {

    String response =
        http.getString();

    Serial.print("Backend Response: ");

    Serial.println(response);

  }

  else {

    Serial.print("HTTP Error: ");

    Serial.println(httpResponseCode);
  }


  http.end();
}


// =================================
// SETUP
// =================================

void setup() {

  Serial.begin(115200);

  delay(1000);


  Serial.println();

  Serial.println("=================================");

  Serial.println(
      "    SMART PATIENT MONITORING"
  );

  Serial.println("=================================");


  // Start DHT22

  dht.begin();

  Serial.println(
      "DHT22 initialized"
  );


  // Fall button

  pinMode(
      FALL_PIN,
      INPUT_PULLUP
  );

  Serial.println(
      "Fall sensor initialized"
  );


  // Normal / Abnormal button

  pinMode(
      MODE_BUTTON_PIN,
      INPUT_PULLUP
  );

  Serial.println(
      "Mode button initialized"
  );


  // =================================
  // Wi-Fi
  // =================================

  WiFi.begin(
      WIFI_SSID,
      WIFI_PASSWORD
  );


  Serial.print(
      "Connecting to Wi-Fi"
  );


  while (
      WiFi.status() != WL_CONNECTED
  ) {

    delay(500);

    Serial.print(".");
  }


  Serial.println();

  Serial.println(
      "Wi-Fi connected!"
  );


  Serial.print(
      "ESP32 IP Address: "
  );

  Serial.println(
      WiFi.localIP()
  );


  Serial.println(
      "ESP32 READY"
  );

  Serial.println(
      "================================="
  );
}


// =================================
// LOOP
// =================================

void loop() {


  // =================================
  // NORMAL / ABNORMAL BUTTON
  // =================================

  bool buttonState =
      digitalRead(
          MODE_BUTTON_PIN
      );


  // Detect button press

  if (
      lastButtonState == HIGH &&
      buttonState == LOW
  ) {

    abnormalMode =
        !abnormalMode;


    Serial.println();

    Serial.println(
        "******** MODE CHANGED ********"
    );


    if (abnormalMode) {

      Serial.println(
          "ABNORMAL MODE ACTIVATED"
      );

    }

    else {

      Serial.println(
          "NORMAL MODE ACTIVATED"
      );
    }


    Serial.println(
        "*******************************"
    );


    // Small debounce delay

    delay(300);
  }


  lastButtonState =
      buttonState;


  // =================================
  // FALL BUTTON
  // =================================

  bool fallDetected =
      (
          digitalRead(FALL_PIN)
          == LOW
      );


  // =================================
  // READ TEMPERATURE
  // =================================

  float realTemperature =
      dht.readTemperature();


  // If DHT reading fails

  if (isnan(realTemperature)) {

    Serial.println(
        "DHT22 reading failed!"
    );

    realTemperature = 36.8;
  }


  // =================================
  // SIMULATED PATIENT VALUES
  // =================================

  int heartRate;

  int spo2;

  float temperature;


  if (abnormalMode == false) {

    // NORMAL VALUES

    heartRate =
        random(70, 91);

    spo2 =
        random(96, 101);

    // Use DHT22 temperature

    temperature =
        realTemperature;

  }

  else {

    // ABNORMAL VALUES

    heartRate =
        random(105, 126);

    spo2 =
        random(88, 94);

    temperature =
        random(380, 396)
        / 10.0;
  }


  // =================================
  // DISPLAY MODE
  // =================================

  if (abnormalMode) {

    Serial.println(
        "MODE: ABNORMAL"
    );

  }

  else {

    Serial.println(
        "MODE: NORMAL"
    );
  }


  // =================================
  // TEMPERATURE
  // =================================

  Serial.print(
      "Temperature: "
  );

  Serial.print(
      temperature
  );

  Serial.println(
      " °C"
  );


  // =================================
  // HEART RATE
  // =================================

  Serial.print(
      "Heart Rate: "
  );

  Serial.print(
      heartRate
  );

  Serial.println(
      " BPM"
  );


  // =================================
  // SpO2
  // =================================

  Serial.print(
      "SpO2: "
  );

  Serial.print(
      spo2
  );

  Serial.println(
      " %"
  );


  // =================================
  // FALL STATUS
  // =================================

  if (fallDetected) {

    Serial.println(
        "Fall Status: FALL DETECTED"
    );

  }

  else {

    Serial.println(
        "Fall Status: SAFE"
    );
  }


  // =================================
  // PATIENT STATUS
  // =================================

  if (
      temperature > 38.0 ||
      heartRate < 60 ||
      heartRate > 100 ||
      spo2 < 94 ||
      fallDetected
  ) {

    Serial.println(
        "Patient Status: ALERT"
    );

  }

  else {

    Serial.println(
        "Patient Status: NORMAL"
    );
  }


  Serial.println(
      "---------------------------------"
  );


  // =================================
  // SEND DATA TO BACKEND
  // =================================

  sendSensorData(
      temperature,
      heartRate,
      spo2,
      fallDetected
  );
  


  delay(2000);
}