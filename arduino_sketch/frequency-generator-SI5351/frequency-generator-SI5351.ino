/*
   si5351_example.ino - Simple example of using Si5351Arduino library

   Copyright (C) 2015 - 2016 Jason Milldrum <milldrum@gmail.com>

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include "si5351.h"
#include "Wire.h"

unsigned long frequency = 100000ULL;
long resistance = 2000;
String input;
String command;
unsigned long value;

Si5351 si5351;

void setup()
{
  bool i2c_found;

  // Start serial and initialize the Si5351
  Serial.begin(9600);
  i2c_found = si5351.init(SI5351_CRYSTAL_LOAD_8PF, 0, 0);
  if (!i2c_found)
  {
    Serial.print("si5351 not found");
  }
  else
  {
    Serial.println("ready");
  }

  // Set CLK0 to output 600 kHz (600 000.00)
  si5351.set_freq(frequency * 100, SI5351_CLK0);

  // Set standard resistance
  change_resistance(value);
  resistance = value;

  // Query a status update and wait a bit to let the Si5351 populate the
  // status flags correctly.
  si5351.update_status();
  delay(500);

  // Now define the cap controlling pins
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);

  // Set all low (but 6 which NC is damaged)
  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  digitalWrite(6, HIGH);
  digitalWrite(7, LOW);
}

void loop()
{
  // get any incoming bytes:
  if (Serial.available() > 0) {
    input = Serial.readStringUntil('\n');
    command = getValue(input, '_', 0);
    
    if (check_numeric(getValue(input, '_', 1))) {
//      value = getValue(input, '_', 1).toInt();
      value = strtoul(getValue(input, '_', 1).c_str(), NULL, 10);
    }
    else{
      value = -1;
    }

    // making sure the right byte has been received (for debugging):
    //    Serial.print("received: \'");
    //    Serial.print(command);
    //    Serial.print("\n");

    // Return current frequency if freq is typed in by user
    if (command.equals("cap")){
      if (value >= 2 && value <= 7){
        if (digitalRead(value)== 1) {
          digitalWrite(value, LOW);
          Serial.print("Cap ");
          Serial.print(value);
          Serial.print(" off\n");
        }
        else {
          digitalWrite(value, HIGH);
          Serial.print("Cap ");
          Serial.print(value);
          Serial.print(" on\n");
        }
      }
      else{
       Serial.println("Please enter a valid capacitor number");
      }
    }
    // Check if user enters a changed resistance
    else if (command.equals("res")) {
      if (value == -1) {
          Serial.print(resistance); 
        }
      else if (value >= 69 && value <= 2640){
        change_resistance(value);
        resistance = value;
        Serial.print("Resistance changed to: ");
        Serial.print(value);
        Serial.print(" Ohm\n");
      }
      else {
        Serial.println("Please enter a valid resistance between 0 and 2500 Ohm");
      }
    }
    // Check if user enters a frequency
    else if (command.equals("freq")) {
        Serial.println("Success"); 
        // If it is in the range the SI5351 can handle, change the frequency to the value of the number
        if (value == -1) {
          Serial.print(frequency); 
        }
        else if (value >= 8000 && value <= 150000000) {
          si5351.set_freq(value * 100, SI5351_CLK0);
          frequency = value;
          Serial.print("Frequency set to: ");
          Serial.print(value);
          Serial.println(" Hz");
          frequency = value;
        }
        // If not return an error
        else
        {
          Serial.println("Frequency out of range");
        }
    }
    // If the input is not a valid number nor a command, return an error
    else
    {
      Serial.println(command);
      Serial.println("Input not a valid command please choose command_number as a format.");
    }
  }
}

// Function to check if a string is a number or not
boolean check_numeric(String str) {
    unsigned int stringLength = str.length();
 
    if (stringLength == 0) {
        return false;
    }
 
    boolean seenDecimal = false;
 
    for(unsigned int i = 0; i < stringLength; ++i) {
        if (isDigit(str.charAt(i))) {
            continue;
        }
 
        if (str.charAt(i) == '.') {
            if (seenDecimal) {
                return false;
            }
            seenDecimal = true;
            continue;
        }
        return false;
    }
    return true;
}

// Function to change the resistance of the rheostat
void change_resistance(long resistance) {
  // byte(resistance * 256 / 2500);
  byte val = byte((resistance - 70) * 256 / 2640);
  Wire.beginTransmission(44); // transmit to device #44 (0x2c)
                              // device address is specified in datasheet
  Wire.write(byte(0x00));            // sends instruction byte  
  Wire.write(val);             // sends potentiometer value byte  
  Wire.endTransmission();     // stop transmitting
}

// Function to split string
String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = { 0, -1 };
  int maxIndex = data.length() - 1;
  
  for (int i = 0; i <= maxIndex && found <= index; i++) {
      if (data.charAt(i) == separator || i == maxIndex) {
          found++;
          strIndex[0] = strIndex[1] + 1;
          strIndex[1] = (i == maxIndex) ? i+1 : i;
      }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
