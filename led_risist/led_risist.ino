void setup(){
   Serial.begin(9600);
   pinMode(11, OUTPUT); 

}

void loop(){
   int resistor = analogRead(A0);
   int bright = map(resistor, 0, 1023,0, 255);
   digitalWrite(11, bright);
}
