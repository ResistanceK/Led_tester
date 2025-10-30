#define REF_RESISTOR 10000.0
                              
void setup(){
    Serial.begin(9600);
}

void loop(){
    int adcValue = analogRead(0);
    float vMeasured = adcValue * (5.0/1023.0);
    float vSupply = 5.0;
    float rUnknown = REF_RESISTOR * (vMeasured/(vSupply - vMeasured));
    Serial.print("ADC : ");
    Serial.print(adcValue);
    Serial.print("\tV_measured: ");
    Serial.print(vMeasured,3);
    Serial.print("V\tR_unknown: ");
    Serial.print(rUnknown, 2);
    Serial.println(" ohm");
    delay(500);
}
