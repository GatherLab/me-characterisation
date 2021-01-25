/*
 * si5351_example.ino - Simple example of using Si5351Arduino library
 *
 * Copyright (C) 2015 - 2016 Jason Milldrum <milldrum@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "si5351.h"
#include "Wire.h"

Si5351 si5351;

void setup()
{
  bool i2c_found;

  // Start serial and initialize the Si5351
  Serial.begin(9600);
  i2c_found = si5351.init(SI5351_CRYSTAL_LOAD_10PF, 0, 0);
  if(!i2c_found)
  {
    Serial.println("Device not found on I2C bus!");
  }

  // Set CLK0 to output 600 kHz (600 000.00)
  // si5351.set_freq(minimum * 100, SI5351_CLK0);

  // Query a status update and wait a bit to let the Si5351 populate the
  // status flags correctly.
  si5351.update_status();
  delay(500);
  
  // Read the Status Register and print it only at the beginning
  si5351.update_status();
  Serial.print("SYS_INIT: ");
  Serial.print(si5351.dev_status.SYS_INIT);
  Serial.print("  LOL_A: ");
  Serial.print(si5351.dev_status.LOL_A);
  Serial.print("  LOL_B: ");
  Serial.print(si5351.dev_status.LOL_B);
  Serial.print("  LOS: ");
  Serial.print(si5351.dev_status.LOS);
  Serial.print("  REVID: ");
  Serial.println(si5351.dev_status.REVID);
}

void loop()
{
  // get any incoming bytes:
  if (Serial.available() > 0) {
    char thisChar = Serial.read();
    
    // making sure the right byte has been received (for debugging):
    Serial.print("received: \'");
    Serial.print(thisChar);
    Serial.println("\'");

    // checking bytes with ASCII representations to open or close relays:
    if (thisChar == '1') {
      si5351.set_freq(thisChar, SI5351_CLK0);
      Serial.println("Frequency set to: ");
      Serial.println(thisChar);
      Serial.println(" Hz \'");

    }
  }
}
