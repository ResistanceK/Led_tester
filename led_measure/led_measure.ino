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
    float resist = (analog_A1 - analog_A0)/current;

    char buffer[100];
    char v_buf[10], i_buf[10], r_buf[10], s_buf[10];

    dtostrf(unknown_voltage, 4, 2, v_buf);
    dtostrf(current, 6, 5, i_buf);
    dtostrf(unknown_resistor, 5, 2, r_buf);
    dtostrf(SUPPLY, 4, 2, s_buf);    

    snprintf(buffer, sizeof(buffer),
         "{\"voltage\":%s, \"current\":%s, \"resistor\":%s, \"supply\":%s}",
         v_buf, i_buf, r_buf, s_buf);
    
    Serial.println(buffer);     
    
    delay(1000);
}
