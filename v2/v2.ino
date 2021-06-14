#define AIRPUMP 2
#define VALVE 3
#define LED_G 13
#define LED_R 12

#include <Wire.h>
#include <Adafruit_MLX90614.h>

#include "MAX30105.h" //sparkfun MAX3010X library
MAX30105 particleSensor;
#define USEFIFO

bool logicLed = LOW;
int x;

Adafruit_MLX90614 mlx = Adafruit_MLX90614();
double regress(double x) {
  double terms[] = {
    -8.5651165052019118e+004,
    6.2318407642005332e+003,
    2.4487694610792232e+002,
    -3.0033124983625783e+001,
    5.5314931440460646e-001,
    7.2528261720683843e-003,
    1.9478248907247100e-008,
    -1.0734112248788609e-005,
    2.6252214033891448e-007,
    7.8683495701639927e-010,
    -3.9491802024273945e-010,
    4.6856990053618978e-012,
    1.4920034956100530e-013,
    7.4152580192469598e-016,
    5.1452869403466000e-017,
    -4.1889255056483581e-018,
    -7.2426299872866526e-020,
    4.0789203603061179e-021,
    -4.0994548677290387e-024,
    -2.7618943330956162e-024,
    4.6993894959704993e-026,
    8.0145271096257985e-028,
    -1.1470472617524997e-029,
    -4.5942574292568771e-031,
    6.6331699501193899e-033
  };
  size_t csz = sizeof terms / sizeof * terms;
  double t = 1;
  double r = 0;
  for (int i = 0; i < csz; i++) {
    r += terms[i] * t;
    t *= x;
  }
  return r;
}

void beginMeasuring() {
  for (int i = 0; i < 10; i++) {
    digitalWrite(LED_R, LOW); delay(50);
    digitalWrite(LED_R, HIGH); delay(50);
  }
  digitalWrite(LED_R, HIGH);
}
void endMeasuring() {
  digitalWrite(LED_R, LOW);
  for (int i = 0; i < 10; i++) {
    digitalWrite(LED_G, HIGH); delay(50);
    digitalWrite(LED_G, LOW); delay(50);
  }
}

void kirimDummyOximeter(long waktuKirim) {
  Serial.println("");
  Serial.println("MAX30102");
  delay(100);

  for (long i = 0; i <= waktuKirim; i++) {
    Serial.print(micros());
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    Serial.println(123);
    digitalWrite(LED_R, !logicLed);
    logicLed = !logicLed;
    delay(500);
  }
}
void kirimOximeter(long waktuKirim) {

  //MAX30102===================================================================================
  while (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 was not found");
  }
  byte ledBrightness = 0x7F;
  byte sampleAverage = 4;
  byte ledMode = 2;
  int sampleRate = 400;
  int pulseWidth = 411;
  int adcRange = 16384;
  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange); //Configure sensor with these settings
  particleSensor.enableDIETEMPRDY();
  //MAX30102===================================================================================

  //Serial.println("");
  //Serial.println("MAX30102");
  //delay(100);
  long i = 0;
  while (1) {
#ifdef USEFIFO
    particleSensor.check(); //Check the sensor, read up to 3 samples
    if (particleSensor.available()) {
      Serial.print(micros());
      Serial.print(",");
      Serial.print(particleSensor.getFIFORed());
      Serial.print(",");
      Serial.println(particleSensor.getFIFOIR());
      particleSensor.nextSample();
      i++;
    }
    if (i >= waktuKirim) {
      break;
    }
#endif
  }
}
void kirimDummySuhu(long waktuKirim) {
  Serial.println("");
  Serial.println("MLX90614");
  delay(100);

  for (long i = 0; i <= waktuKirim; i++) {
    Serial.print(micros());
    Serial.print(",");
    Serial.print(i);
    Serial.print(",");
    Serial.println(789);
    digitalWrite(LED_R, !logicLed);
    logicLed = !logicLed;
    delay(500);
  }
}
void kirimSuhu(long waktuKirim) {
  mlx.begin();
  //Serial.println("");
  //Serial.println("MLX90614");
  delay(100);

  for (long i = 0; i <= waktuKirim; i++) {
    float suhuSurface = mlx.readObjectTempC();
    float suhuBody = regress(suhuSurface);
    Serial.print(micros());
    Serial.print(",");
    Serial.println(suhuBody);
    digitalWrite(LED_R, !logicLed);
    logicLed = !logicLed;
    delay(200);
  }
}



void setup() {
  pinMode(AIRPUMP, OUTPUT);
  pinMode(VALVE, OUTPUT);
  pinMode(LED_R, OUTPUT);
  pinMode(LED_G, OUTPUT);

  digitalWrite(LED_G, HIGH);
  digitalWrite(LED_R, LOW);

  Serial.begin(115200);
  Serial.setTimeout(1);

  while (!Serial.available());
  x = Serial.readString().toInt();
  
  if (x == 0) {
    beginMeasuring();
    kirimOximeter(2000);
    Serial.println("ENDMEASURE");
    Serial.println("ENDMEASURE");
    Serial.println("ENDMEASURE");
    Serial.println("ENDMEASURE");
    endMeasuring();
  }
  
  if (x == 1) {
    kirimSuhu(50);
    Serial.println("ENDMEASURE");
    Serial.println("ENDMEASURE");
    Serial.println("ENDMEASURE");
    Serial.println("ENDMEASURE");
    endMeasuring();
  }
  
  if (x == 2) {
    Serial.print("TENSI");
  }
  
  

}

void loop() {

}
