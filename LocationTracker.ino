/*
  LocationTracker

  Author: Michael Sportelli

  This program works ouses the Arduino MKR WiFi 1010 with a 
    MKR GPS Shield attached on top. It communicates via Serial

  Prints data to serial port every 10 seconds in CSV format as follows:

  longitude, latitude, altitude, speed, time, course, variation, sattelites

  TODO:

  * print altitude in feet
  * print speed in mph
  * format time to Y M D H M S
  * save data to SD card instead of serial
  * Add LiPo battery support
  * Add some sort of User Interface
  * Add bluetooth support to work as follow
      - input coordinates via app
      - UI will tell the user the direction to the destination as well as how far the destination is

*/

#include <Arduino_MKRGPS.h>

void setup() {
  
  // initialize serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // If you are using the MKR GPS as shield, change the next line to pass
  // the GPS_MODE_SHIELD parameter to the GPS.begin(...)
  if (!GPS.begin(GPS_MODE_SHIELD)) {
    Serial.println("Failed to initialize GPS!");
    while (1);
  } else {
    Serial.println("Success: Waiting for data . . . . ");
  }
}

void loop() {

  // check if there is new GPS data available
  if (GPS.available()) {
    //read GPS values
    float latitude   = GPS.latitude();
    float longitude  = GPS.longitude();
    float altitude   = GPS.altitude();
    float speed      = GPS.speed();
    unsigned long time       = GPS.getTime();
    float course   = GPS.course();
    float variation      = GPS.variation();
    int   satellites = GPS.satellites();

    //print long / lat values values
    Serial.print(longitude, 7);
    Serial.print(", ");
    Serial.print(latitude, 7);
    Serial.print(", ");
    Serial.print(altitude);
    Serial.print(", ");
    Serial.print(speed);
    Serial.print(", ");
    Serial.print(time);
    Serial.print(", ");
    Serial.print(course);
    Serial.print(", ");
    Serial.print(variation);
    Serial.print(", ");
    Serial.println(satellites);

    delay(10000);
  }
}
