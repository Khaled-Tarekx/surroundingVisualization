# surroundingVisualization
 is a project that visualize the surroundings of a car working with a node mcu script

# updated servo file to send json

#include <Servo.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <NewPing.h>
#include <ArduinoJson.h>  

Servo myservo;  // Create servo object to control the servo

const int trigPin = D2;  // Trig pin of the ultrasonic sensor
const int echoPin = D3;  // Echo pin of the ultrasonic sensor
const int maxDistance = 200; // Maximum distance to measure (in cm)

NewPing sonar(trigPin, echoPin, maxDistance);  // Initialize NewPing

int distance;   // Variable to store the distance
int angle;      // Servo angle

// Replace with your network credentials
const char* ssid = "your_SSID"; 
const char* password = "your_PASSWORD"; // wife stuff

// Replace with your server URL
const char* serverUrl = "http://yourserver.com/endpoint";  // the django endpoint  or any server endpoint

void setup() {
  myservo.attach(D1);  // Attach the servo to pin D1 on the NodeMCU
  Serial.begin(9600);  // Start serial communication for debugging

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  // Array of angles to stop at
  int angles[] = {0, 45, 90, 135, 180};
  int numAngles = sizeof(angles) / sizeof(angles[0]);

  // Loop through each angle
  for (int i = 0; i < numAngles; i++) {
    angle = angles[i];
    
    // Move the servo to the current angle
    myservo.write(angle);
    delay(1000);  // Allow the servo to move to the position
    
    // Read distance from ultrasonic sensor
    distance = sonar.ping_cm();
    Serial.print("Angle: ");
    Serial.print(angle);
    Serial.print(" Distance: ");
    Serial.println(distance);
    StaticJsonBuffer<256> jsonBuffer;
    JsonObject& json = jsonBuffer.createObject();
    json["distance"] = distance;
    json["angle"] = angle;

    String jsonString;
    json.printTo(jsonString);

    sendDataToServer(jsonString);
    // sendDataToServer(distance, angle);

    delay(3000);  // Wait for 3 seconds before moving to the next angle
  }
}

// Function to send data to the server
void sendDataToServer(int distance, int angle) {
  if (WiFi.status() == WL_CONNECTED) { // Check if we are connected to WiFi
    HTTPClient http;
    String serverPath = serverUrl + "?distance=" + String(distance) + "&angle=" + String(angle);

    http.begin(serverPath.c_str());  // Specify request destination
    int httpResponseCode = http.GET();  // Send the GET request

    if (httpResponseCode > 0) {
      String response = http.getString();  // Get the response payload
      Serial.println(httpResponseCode);  // Print HTTP return code
      Serial.println(response);  // Print request response payload
    } else {
      Serial.print("Error on sending GET: ");
      Serial.println(httpResponseCode); 
    }
    http.end();  // Free resources
  } else {
    Serial.println("WiFi Disconnected");
  }
}


# running django server 
python manage.py runserver

# look for SurroundingVisualization
set DEMO_MODE = True

# replace in the server_url  in servo file
replace with real_endpoint (http://localhost:8000/car_mapping/12/)

# migrations needed before running (only use this commands one time)
python manage.py makemigrations
python manage.py migrate

# to run the programa for real data testing use the uvicorn command in the terminal
uvicorn SurroundingVisualization.asgi:application --port 8000
