#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>

// =================================
// Wi-Fi
// =================================

const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";

// =================================
// Render Flask Backend
// =================================

const char* SERVER_URL =
    "https://smart-patient-monitoring.onrender.com/sensor-data";

// =================================
// Sensor Pins
// =================================

#define FALL_PIN 5
#define MODE_BUTTON_PIN 18

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

  // =================================
  // Check Wi-Fi
  // =================================

  if (WiFi.status() != WL_CONNECTED) {

    Serial.println("Wi-Fi not connected!");

    return;
  }

  // =================================
  // HTTPS Client
  // =================================

WiFiClientSecure client;

client.setInsecure();
client.setTimeout(15000);

HTTPClient http;
http.setTimeout(15000);

  Serial.println();
  Serial.println("Connecting to Render backend:");
  Serial.println(SERVER_URL);

  // =================================
  // Start HTTPS Connection
  // =================================

  if (!http.begin(client, SERVER_URL)) {

    Serial.println(
        "HTTP connection initialization failed!"
    );

    return;
  }

  // =================================
  // HTTP Header
  // =================================

  http.addHeader(
      "Content-Type",
      "application/json"
  );

  // =================================
  // Create JSON
  // =================================

  String jsonData = "{";

  jsonData += "\"temperature\":";
  jsonData += String(temperature, 1);

  jsonData += ",\"heart_rate\":";
  jsonData += String(heartRate);

  jsonData += ",\"spo2\":";
  jsonData += String(spo2);

  jsonData += ",\"fall\":";

  if (fallDetected) {

    jsonData += "true";

  } else {

    jsonData += "false";
  }

  jsonData += "}";

  // =================================
  // Display JSON
  // =================================

  Serial.println();
  Serial.println(
      "Sending data to Render:"
  );

  Serial.println(jsonData);

  // =================================
  // Send POST Request
  // =================================

  int httpResponseCode =
      http.POST(jsonData);

  // =================================
  // Response
  // =================================

  Serial.print(
      "HTTP Response Code: "
  );

  Serial.println(
      httpResponseCode
  );

  if (httpResponseCode > 0) {

    String response =
        http.getString();

    Serial.print(
        "Backend Response: "
    );

    Serial.println(
        response
    );

  } else {

    Serial.print(
        "HTTP Error: "
    );

    Serial.println(
        httpResponseCode
    );
  }

  // =================================
  // Close Connection
  // =================================

  http.end();

  Serial.println(
      "---------------------------------"
  );
}


// =================================
// SETUP
// =================================

void setup() {

  Serial.begin(115200);

  delay(1000);

  // =================================
  // Project Header
  // =================================

  Serial.println();

  Serial.println(
      "================================="
  );

  Serial.println(
      "     SMART PATIENT MONITORING"
  );

  Serial.println(
      "================================="
  );

  // =================================
  // Fall Sensor
  // =================================

  pinMode(
      FALL_PIN,
      INPUT_PULLUP
  );

  Serial.println(
      "Fall sensor initialized"
  );

  // =================================
  // Mode Button
  // =================================

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

  int attempts = 0;

  while (
      WiFi.status() != WL_CONNECTED &&
      attempts < 30
  ) {

    delay(500);

    Serial.print(".");

    attempts++;
  }

  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {

    Serial.println(
        "Wi-Fi connected!"
    );

    Serial.print(
        "ESP32 IP Address: "
    );

    Serial.println(
        WiFi.localIP()
    );

  } else {

    Serial.println(
        "Wi-Fi connection FAILED!"
    );
  }

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

    } else {

      Serial.println(
          "NORMAL MODE ACTIVATED"
      );
    }

    Serial.println(
        "*******************************"
    );

    // Debounce
    delay(300);
  }

  lastButtonState =
      buttonState;


  // =================================
  // FALL SENSOR
  // =================================

  bool fallDetected =
      (
          digitalRead(FALL_PIN)
          == LOW
      );


  // =================================
  // PATIENT VALUES
  // =================================

  int heartRate;
  int spo2;
  float temperature;


  // =================================
  // NORMAL MODE
  // =================================

  if (!abnormalMode) {

    heartRate =
        random(70, 91);

    spo2 =
        random(96, 101);

    temperature =
        random(365, 373) / 10.0;

  }

  // =================================
  // ABNORMAL MODE
  // =================================

  else {

    heartRate =
        random(105, 126);

    spo2 =
        random(88, 94);

    temperature =
        random(380, 396) / 10.0;
  }


  // =================================
  // DISPLAY MODE
  // =================================

  if (abnormalMode) {

    Serial.println(
        "MODE: ABNORMAL"
    );

  } else {

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
      temperature,
      1
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
  // SPO2
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

  } else {

    Serial.println(
        "Fall Status: SAFE"
    );
  }


  // =================================
  // PATIENT STATUS
  // =================================

  if (
      temperature > 38.0 ||
      heartRate > 100 ||
      heartRate < 60 ||
      spo2 < 94 ||
      fallDetected
  ) {

    Serial.println(
        "Patient Status: ALERT"
    );

  } else {

    Serial.println(
        "Patient Status: NORMAL"
    );
  }


  Serial.println(
      "---------------------------------"
  );


  // =================================
  // SEND TO RENDER
  // =================================

  sendSensorData(
      temperature,
      heartRate,
      spo2,
      fallDetected
  );


  // =================================
  // WAIT 2 SECONDS
  // =================================

  delay(2000);
}
