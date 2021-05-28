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
String command;

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
    Serial.print("ready");
  }

  // Set CLK0 to output 600 kHz (600 000.00)
  si5351.set_freq(frequency * 100, SI5351_CLK0);

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

  // Read the Status Register and print it only at the beginning
  //  si5351.update_status();
  //  if (si5351.dev_status.SYS_INIT && si5351.dev_status.LOL_A && si5351.dev_status.LOL_B && i5351.dev_status.LOS && i5351.dev_status.REVID){
  //    Serial.print("ready");
  //  }
  //  else{
  //    Serial.print("not ready");
  //  }
  //  Serial.print("SYS_INIT: ");
  //  Serial.print(si5351.dev_status.SYS_INIT);
  //  Serial.print("  LOL_A: ");
  //  Serial.print(si5351.dev_status.LOL_A);
  //  Serial.print("  LOL_B: ");
  //  Serial.print(si5351.dev_status.LOL_B);
  //  Serial.print("  LOS: ");
  //  Serial.print(si5351.dev_status.LOS);
  //  Serial.print("  REVID: ");
  //  Serial.println(si5351.dev_status.REVID);
}

void loop()
{
  // get any incoming bytes:
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n');

    // making sure the right byte has been received (for debugging):
    //    Serial.print("received: \'");
    //    Serial.print(command);
    //    Serial.print("\n");

    // Return current frequency if freq is typed in by user
    if (command.equals("freq")) {
      Serial.print(frequency);
    }
    //
    else if (command.equals("cap2")) {
      if (digitalRead(2)== 1) {
        digitalWrite(2, LOW);
        Serial.println("Cap 2 off");
      }
      else {
        digitalWrite(2, HIGH);
        Serial.println("Cap 2 on");
      }
    }
    else if (command.equals("cap3")) {
      if (digitalRead(3)== 1) {
        digitalWrite(3, LOW);
        Serial.println("Cap 3 off");
      }
      else {
        digitalWrite(3, HIGH);
        Serial.println("Cap 3 on");
      }
    }
    else if (command.equals("cap4")) {
      if (digitalRead(4)== 1) {
        digitalWrite(4, LOW);
        Serial.println("Cap 4 off");
      }
      else {
        digitalWrite(4, HIGH);
        Serial.println("Cap 4 on");
      }
    }
    else if (command.equals("cap5")) {
      if (digitalRead(5)== 1) {
        digitalWrite(5, LOW);
        Serial.println("Cap 5 off");
      }
      else {
        digitalWrite(5, HIGH);
        Serial.println("Cap 5 on");
      }
    }
    else if (command.equals("cap6")) {
      if (digitalRead(6)== 1) {
        digitalWrite(6, LOW);
        Serial.println("Cap 6 off");
      }
      else {
        digitalWrite(6, HIGH);
        Serial.println("Cap 6 on");
      }
    }
    else if (command.equals("cap7")) {
      if (digitalRead(7)== 1) {
        digitalWrite(7, LOW);
        Serial.println("Cap 7 off");
      }
      else {
        digitalWrite(7, HIGH);
        Serial.println("Cap 7 on");
      }
    }
    // Check if user enters a number
    else if (check_numeric(command)) {
      // If it is in the range the SI5351 can handle, change the frequency to the value of the number
      if (command.toFloat() >= 8000 && command.toFloat() <= 150000000) {
        frequency = (unsigned long) command.toFloat();
        si5351.set_freq(frequency * 100, SI5351_CLK0);
        Serial.print("Frequency set to: ");
        Serial.print(command);
        Serial.println(" Hz");
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
      Serial.print(command);
      Serial.println("Input not a command nor a number");
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
