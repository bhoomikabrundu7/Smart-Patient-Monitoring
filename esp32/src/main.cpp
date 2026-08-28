#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

// ============================================================
// CAREMATRIX
// Smart Patient Monitoring System
//
// DATA PATH:
// Wokwi ESP32
//      ↓ HTTP
// Local Flask server.py :5000
//      ↓
// Streamlit Dashboard
// ============================================================

// ============================================================
// WIFI
// ============================================================

const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";

// IMPORTANT:
// This is your LOCAL Flask backend.
// Do NOT use Render here.
const char* SERVER_URL =
    "http://host.wokwi.internal:5000/sensor-data";

// ============================================================
// HARDWARE PINS
// ============================================================

#define DHT_PIN 4
#define DHT_TYPE DHT22

#define FALL_SENSOR_PIN 5
#define MODE_BUTTON_PIN 18

DHT dht(DHT_PIN, DHT_TYPE);

// ============================================================
// TIMING
// ============================================================

const unsigned long SEND_INTERVAL = 5000;

unsigned long lastSendTime = 0;

// Automatic presentation timing
const unsigned long NORMAL_TIME = 15000;
const unsigned long ABNORMAL_TIME = 15000;
const unsigned long FALL_TIME = 10000;

unsigned long modeStartTime = 0;

// ============================================================
// STATE
// ============================================================

bool abnormalMode = false;
bool automaticFall = false;

bool lastButtonState = HIGH;

// ============================================================
// WIFI CONNECTION
// ============================================================

bool connectWiFi()
{
    Serial.println();
    Serial.println("Connecting to Wi-Fi...");

    WiFi.mode(WIFI_STA);

    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );

    int attempts = 0;

    while (
        WiFi.status() != WL_CONNECTED &&
        attempts < 30
    )
    {
        delay(500);

        Serial.print(".");

        attempts++;
    }

    Serial.println();

    if (WiFi.status() == WL_CONNECTED)
    {
        Serial.println("Wi-Fi connected!");

        Serial.print("ESP32 IP Address: ");
        Serial.println(WiFi.localIP());

        return true;
    }

    Serial.println("Wi-Fi connection failed!");

    return false;
}

// ============================================================
// SEND DATA TO LOCAL SERVER
// ============================================================

bool sendSensorData(
    float temperature,
    int heartRate,
    int spo2,
    bool fallDetected,
    const char* mode
)
{
    Serial.println();
    Serial.println("=================================");
    Serial.println("DEBUG: Sending sensor data...");
    Serial.println("Sending to LOCAL BACKEND...");

    Serial.println(
        "http://host.wokwi.internal:5000/sensor-data"
    );

    // --------------------------------------------------------
    // WIFI CHECK
    // --------------------------------------------------------

    if (WiFi.status() != WL_CONNECTED)
    {
        Serial.println(
            "Wi-Fi disconnected!"
        );

        if (!connectWiFi())
        {
            Serial.println(
                "Wi-Fi reconnect failed!"
            );

            return false;
        }
    }

    // --------------------------------------------------------
    // CREATE JSON
    // --------------------------------------------------------

    String jsonData = "{";

    jsonData += "\"temperature\":";
    jsonData += String(
        temperature,
        1
    );

    jsonData += ",\"heart_rate\":";
    jsonData += String(
        heartRate
    );

    jsonData += ",\"spo2\":";
    jsonData += String(
        spo2
    );

    jsonData += ",\"fall\":";

    if (fallDetected)
    {
        jsonData += "true";
    }
    else
    {
        jsonData += "false";
    }

    jsonData += ",\"mode\":\"";
    jsonData += mode;
    jsonData += "\"}";

    // --------------------------------------------------------
    // PRINT JSON
    // --------------------------------------------------------

    Serial.println();
    Serial.println("Sending:");
    Serial.println(jsonData);

    // --------------------------------------------------------
    // HTTP
    // --------------------------------------------------------

    HTTPClient http;

    http.setConnectTimeout(10000);
    http.setTimeout(10000);

    Serial.println();
    Serial.println("Opening HTTP connection...");

    if (!http.begin(SERVER_URL))
    {
        Serial.println(
            "HTTP begin FAILED!"
        );

        return false;
    }

    http.addHeader(
        "Content-Type",
        "application/json"
    );

    http.addHeader(
        "Accept",
        "application/json"
    );

    Serial.println(
        "Sending HTTP POST..."
    );

    int responseCode =
        http.POST(jsonData);

    // --------------------------------------------------------
    // RESPONSE
    // --------------------------------------------------------

    Serial.print(
        "HTTP Response Code: "
    );

    Serial.println(
        responseCode
    );

    if (responseCode > 0)
    {
        String response =
            http.getString();

        Serial.println();
        Serial.println(
            "Server response:"
        );

        Serial.println(
            response
        );
    }
    else
    {
        Serial.print(
            "HTTP Error: "
        );

        Serial.println(
            http.errorToString(
                responseCode
            )
        );
    }

    http.end();

    // --------------------------------------------------------
    // SUCCESS
    // --------------------------------------------------------

    if (
        responseCode >= 200 &&
        responseCode < 300
    )
    {
        Serial.println();
        Serial.println(
            "================================="
        );

        Serial.println(
            "SUCCESS: Data sent to local backend!"
        );

        Serial.println(
            "================================="
        );

        return true;
    }

    Serial.println();
    Serial.println(
        "ERROR: Local backend did not accept data."
    );

    return false;
}

// ============================================================
// SETUP
// ============================================================

void setup()
{
    Serial.begin(115200);

    delay(1000);

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

    // --------------------------------------------------------
    // DHT22
    // --------------------------------------------------------

    dht.begin();

    Serial.println(
        "DHT22 initialized"
    );

    // --------------------------------------------------------
    // FALL SENSOR
    // --------------------------------------------------------

    pinMode(
        FALL_SENSOR_PIN,
        INPUT_PULLUP
    );

    Serial.println(
        "Fall sensor initialized"
    );

    // --------------------------------------------------------
    // MODE BUTTON
    // --------------------------------------------------------

    pinMode(
        MODE_BUTTON_PIN,
        INPUT_PULLUP
    );

    Serial.println(
        "Mode button initialized"
    );

    // --------------------------------------------------------
    // RANDOM
    // --------------------------------------------------------

    randomSeed(
        micros()
    );

    // --------------------------------------------------------
    // WIFI
    // --------------------------------------------------------

    connectWiFi();

    // --------------------------------------------------------
    // READY
    // --------------------------------------------------------

    Serial.println();
    Serial.println(
        "ESP32 READY"
    );

    Serial.println(
        "================================="
    );

    Serial.println();

    Serial.println(
        "AUTOMATIC PRESENTATION MODE"
    );

    Serial.println(
        "NORMAL -> ABNORMAL -> FALL -> NORMAL"
    );

    Serial.println();

    modeStartTime =
        millis();

    // Send first reading immediately
    lastSendTime =
        millis() - SEND_INTERVAL;
}

// ============================================================
// LOOP
// ============================================================

void loop()
{
    // ========================================================
    // MODE BUTTON
    // ========================================================

    bool buttonState =
        digitalRead(
            MODE_BUTTON_PIN
        );

    if (
        buttonState == LOW &&
        lastButtonState == HIGH
    )
    {
        abnormalMode =
            !abnormalMode;

        automaticFall =
            false;

        modeStartTime =
            millis();

        Serial.println();
        Serial.println(
            "******** MODE CHANGED ********"
        );

        if (abnormalMode)
        {
            Serial.println(
                "ABNORMAL MODE ACTIVATED"
            );
        }
        else
        {
            Serial.println(
                "NORMAL MODE ACTIVATED"
            );
        }

        Serial.println(
            "*******************************"
        );

        delay(300);
    }

    lastButtonState =
        buttonState;

    // ========================================================
    // PHYSICAL FALL SENSOR
    // ========================================================

    bool physicalFall =
        digitalRead(
            FALL_SENSOR_PIN
        ) == LOW;

    // ========================================================
    // AUTOMATIC PRESENTATION MODE
    // ========================================================

    unsigned long elapsed =
        millis() - modeStartTime;

    // --------------------------------------------------------
    // NORMAL -> ABNORMAL
    // --------------------------------------------------------

    if (
        !abnormalMode &&
        !automaticFall &&
        elapsed >= NORMAL_TIME
    )
    {
        abnormalMode =
            true;

        modeStartTime =
            millis();

        Serial.println();
        Serial.println(
            "================================="
        );

        Serial.println(
            "AUTOMATIC EVENT:"
        );

        Serial.println(
            "NORMAL -> ABNORMAL"
        );

        Serial.println(
            "================================="
        );

        Serial.println();
    }

    // --------------------------------------------------------
    // ABNORMAL -> FALL
    // --------------------------------------------------------

    else if (
        abnormalMode &&
        !automaticFall &&
        elapsed >= ABNORMAL_TIME
    )
    {
        automaticFall =
            true;

        modeStartTime =
            millis();

        Serial.println();
        Serial.println(
            "================================="
        );

        Serial.println(
            "AUTOMATIC EVENT:"
        );

        Serial.println(
            "ABNORMAL -> FALL DETECTED"
        );

        Serial.println(
            "================================="
        );

        Serial.println();
    }

    // --------------------------------------------------------
    // FALL -> NORMAL
    // --------------------------------------------------------

    else if (
        abnormalMode &&
        automaticFall &&
        elapsed >= FALL_TIME
    )
    {
        automaticFall =
            false;

        abnormalMode =
            false;

        modeStartTime =
            millis();

        Serial.println();
        Serial.println(
            "================================="
        );

        Serial.println(
            "AUTOMATIC EVENT:"
        );

        Serial.println(
            "FALL -> NORMAL"
        );

        Serial.println(
            "================================="
        );

        Serial.println();
    }

    // ========================================================
    // TEMPERATURE
    // ========================================================

    float temperature =
        dht.readTemperature();

    if (isnan(temperature))
    {
        temperature =
            36.5;
    }

    // For presentation mode
    if (abnormalMode)
    {
        temperature =
            38.0 +
            (
                random(
                    0,
                    11
                ) / 10.0
            );
    }

    // ========================================================
    // HEART RATE
    // ========================================================

    int heartRate;

    if (abnormalMode)
    {
        heartRate =
            random(
                105,
                126
            );
    }
    else
    {
        heartRate =
            random(
                70,
                91
            );
    }

    // ========================================================
    // SPO2
    // ========================================================

    int spo2;

    if (abnormalMode)
    {
        spo2 =
            random(
                88,
                94
            );
    }
    else
    {
        spo2 =
            random(
                96,
                101
            );
    }

    // ========================================================
    // FALL STATUS
    // ========================================================

    bool fallDetected =
        physicalFall ||
        automaticFall;

    // ========================================================
    // MODE
    // ========================================================

    const char* mode =
        abnormalMode
            ? "ABNORMAL"
            : "NORMAL";

    // ========================================================
    // PATIENT STATUS
    // ========================================================

    const char* patientStatus;

    if (
        abnormalMode ||
        fallDetected
    )
    {
        patientStatus =
            "ABNORMAL";
    }
    else
    {
        patientStatus =
            "NORMAL";
    }

    // ========================================================
    // SERIAL DISPLAY
    // ========================================================

    Serial.println();
    Serial.println(
        "================================="
    );

    Serial.print(
        "MODE: "
    );

    Serial.println(
        mode
    );

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

    Serial.print(
        "Heart Rate: "
    );

    Serial.print(
        heartRate
    );

    Serial.println(
        " BPM"
    );

    Serial.print(
        "SpO2: "
    );

    Serial.print(
        spo2
    );

    Serial.println(
        " %"
    );

    Serial.print(
        "Fall Status: "
    );

    if (fallDetected)
    {
        Serial.println(
            "FALL DETECTED"
        );
    }
    else
    {
        Serial.println(
            "SAFE"
        );
    }

    Serial.print(
        "Patient Status: "
    );

    Serial.println(
        patientStatus
    );

    Serial.println(
        "---------------------------------"
    );

    // ========================================================
    // SEND DATA EVERY 5 SECONDS
    // ========================================================

    if (
        millis() - lastSendTime >=
        SEND_INTERVAL
    )
    {
        lastSendTime =
            millis();

        sendSensorData(
            temperature,
            heartRate,
            spo2,
            fallDetected,
            mode
        );
    }

    delay(1000);
}