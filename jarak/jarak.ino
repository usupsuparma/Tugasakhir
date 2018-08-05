int pTrig = 11;
int pEcho = 4;
long durasi;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pTrig, OUTPUT);
  pinMode(pEcho, INPUT);
}

void loop() {  
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

