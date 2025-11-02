#define STANDARD_RESISTOR 300.0
#define SUPPLY 5.0

void setup() {
    Serial.begin(9600);
}

void loop() {
    int digital_A1 = analogRead(A1);
    int digital_A0 = analogRead(A0);

    float analog_A1 = digital_A1 * (5.0/1023.0);
    float analog_A0 = digital_A0 * (5.0 / 1023.0);
    
    float voltage_descent = SUPPLY - analog_A1;
    float current = voltage_descent / STANDARD_RESISTOR;
    
    float unknown_voltage = analog_A1 - analog_A0;
    float unknown_resistor = unknown_voltage/current;

    Serial.print("led_name=");
    Serial.print("RED");
    Serial.print(", supply_voltage=");
    Serial.print(SUPPLY, 2);
    Serial.print(", led_voltage=");
    Serial.print(analog_A0, 3);
    Serial.print(", led_current=");
    Serial.println(current,6);
    delay(1000);
}
