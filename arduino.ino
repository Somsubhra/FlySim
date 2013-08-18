/**
 * Sets up the Arduino board.
 */
void setup() {
  pinMode(A0, INPUT); // Take the x-xomponent of accelerometer as input to pin A0
  pinMode(A1, INPUT); // Take the y-component of accelerometer as input to pin A1 
  Serial.begin(9600); // Set the baud-rate for Serial communication at 9600
}

/**
 * The infinite loop. Sends constant x and y voltages of accelerometer
 * to the Serial port.
 */
void loop() {
  Serial.print("x");
  Serial.print(analogRead(A0)); // Print the x-component of accelerometer to Serial
  Serial.print("\n");
  
  delay(18);                    // Keep a delay of 18 ms
  
  Serial.print("y");
  Serial.print(analogRead(A1)); // Print the y-component of accelerometer to Serial 
  Serial.print("\n");
 
  delay(18);                    // Keep a delay of 18ms
}
