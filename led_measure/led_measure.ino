#define R_REF 1000.0   // 기준 저항 (1kΩ)
#define SUPPLY 5.0     // 공급 전압 (5V)

void setup() {
  Serial.begin(9600);
}

void loop() {
  // --- ADC 읽기 ---
  int rawA1 = analogRead(A1);
  int rawA0 = analogRead(A0);

  // --- 전압 변환 ---
  float vA1 = rawA1 * (5.0 / 1023.0);
  float vA0 = rawA0 * (5.0 / 1023.0);

  // --- 계산 ---
  float v_ref = SUPPLY - vA1;          // 기준저항 전압강하
  float v_unknown = vA1 - vA0;         // 미지저항 전압강하
  float v_led = vA0;                   // LED 전압
  float current = v_ref / R_REF;       // 전류 (A)
  float r_unknown = v_unknown / current; // 미지저항 값 (Ω)

  // --- 문자열 버퍼 ---
  char buf_vled[10], buf_i[10], buf_r[10], buf_ref[10], buf_sup[10];
  dtostrf(v_led, 4, 3, buf_vled);
  dtostrf(current, 7, 6, buf_i);
  dtostrf(r_unknown, 6, 2, buf_r);
  dtostrf(v_ref, 4, 3, buf_ref);
  dtostrf(SUPPLY, 4, 2, buf_sup);

  // --- JSON 형식으로 포맷 ---
  char json[200];
  snprintf(json, sizeof(json),
    "{\"supply_voltage\":%s, \"reference_voltage\":%s, \"led_voltage\":%s, "
    "\"current\":%s, \"resistor\":%s}",
    buf_sup, buf_ref, buf_vled, buf_i, buf_r);

  // --- 출력 ---
  Serial.println(json);

  delay(1000);
}
