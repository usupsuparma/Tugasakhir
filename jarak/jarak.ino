int pTrig = 11;
int pEcho = 4;
long durasi;
int percobaan= 1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pTrig, OUTPUT);
  pinMode(pEcho, INPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  
  int jarak = trig();
  Serial.println(jarak);
  delay(1000);
}

long trig(){
  digitalWrite(pTrig, LOW);
  delayMicroseconds(1000);
  digitalWrite(pTrig, HIGH);
  delayMicroseconds(1000);
  digitalWrite(pTrig, LOW);
  durasi = pulseIn(pEcho, HIGH);
  return durasi / 29 / 2;
}

