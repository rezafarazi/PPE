#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <AES.h>
#include <base64.h>
#include <ArduinoJson.h>

// Global variables
String leftCipher = "";
String rightCipher = "";
String leftText = "";
String rightText = "";

// WiFi credentials
const char* ssid = "Reza";
const char* password = "@Key123456";

// AES instance
AES aes;

// Function prototypes
void connectWiFi();
String getUnixTime();
String getCurrentTimeKey(String salt);
String getKey(String keyStr);
String padString(String str);
String unpadString(String str);
String singleCoreEncrypt(String data, String keyStr);
String singleCoreDecrypt(String encData, String keyStr);
String PPE(String inp, String salt);
String PPD(String inp, String salt);

void setup() {
  Serial.begin(115200);
  connectWiFi();
}

void loop() {
  // Main program loop
  // You can add your encryption/decryption calls here
  delay(1000);
}

// WiFi connection function
void connectWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 10) {
    delay(1000);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected successfully!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFailed to connect");
  }
}

// Get Unix timestamp from server
String getUnixTime() {
  WiFiClient client;
  HTTPClient http;
  String unixtime = "0";
  
  if (http.begin(client, "http://future.izino.ir/index.php")) {
    int httpCode = http.GET();
    
    if (httpCode == HTTP_CODE_OK) {
      String payload = http.getString();
      StaticJsonDocument<200> doc;
      DeserializationError error = deserializeJson(doc, payload);
      
      if (!error) {
        unixtime = doc["unixtime"].as<String>();
      }
    }
    http.end();
  }
  return unixtime;
}

// Generate key from Unix timestamp
String getCurrentTimeKey(String salt) {
  String keybase = "";
  String key = "";
  
  String timestep = getUnixTime();
  String timestep8 = timestep.substring(0, 8);
  
  // Build keybase using the same pattern as in MicroPython version
  keybase = timestep8;
  for (int i = timestep8.length() - 1; i >= 0; i--) {
    keybase += timestep8[i];
  }
  // Repeat pattern as in original code
  for (int j = 0; j < 5; j++) {
    for (int i = 0; i < timestep8.length(); i++) {
      keybase += timestep8[i];
    }
    for (int i = timestep8.length() - 1; i >= 0; i--) {
      keybase += timestep8[i];
    }
  }
  
  // Generate key from keybase
  for (int i = 0; i < keybase.length() / 2; i += 2) {
    String numA = String(keybase[i]);
    String numB = String(keybase[i + 1]);
    int addNum = (numA + numB).toInt();
    key += char(addNum);
  }
  
  key = salt + key;
  key = key.substring(0, 16);
  return base64::encode(key);
}

// Ensure key is 16 characters
String getKey(String keyStr) {
  while (keyStr.length() < 16) {
    keyStr += " ";
  }
  return keyStr.substring(0, 16);
}

// Padding function for AES
String padString(String str) {
  int padLen = 16 - (str.length() % 16);
  for (int i = 0; i < padLen; i++) {
    str += char(padLen);
  }
  return str;
}

// Remove padding
String unpadString(String str) {
  int padLen = str.charAt(str.length() - 1);
  return str.substring(0, str.length() - padLen);
}

// Single core encryption
String singleCoreEncrypt(String data, String keyStr) {
  String key = keyStr.substring(0, 16);
  String paddedData = padString(data);
  
  byte keyBytes[16];
  byte dataBytes[paddedData.length()];
  
  key.getBytes(keyBytes, 16);
  paddedData.getBytes(dataBytes, paddedData.length());
  
  aes.set_key(keyBytes, 16);
  aes.encrypt(dataBytes, dataBytes, paddedData.length() / 16);
  
  return base64::encode(dataBytes, paddedData.length());
}

// Single core decryption
String singleCoreDecrypt(String encData, String keyStr) {
  String key = keyStr.substring(0, 16);
  
  int decodedLen = base64::decodeLength(encData);
  byte decodedData[decodedLen];
  base64::decode(encData, decodedData);
  
  byte keyBytes[16];
  key.getBytes(keyBytes, 16);
  
  aes.set_key(keyBytes, 16);
  aes.decrypt(decodedData, decodedData, decodedLen / 16);
  
  String result = String((char*)decodedData);
  return unpadString(result);
}

// Main encryption function
String PPE(String inp, String salt) {
  String key = getCurrentTimeKey(salt);
  return singleCoreEncrypt(inp, key);
}

// Main decryption function
String PPD(String inp, String salt) {
  String key = getCurrentTimeKey(salt);
  return singleCoreDecrypt(inp, key);
} 