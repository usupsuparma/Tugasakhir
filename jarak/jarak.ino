//Inisialisasi Pin
int pTrig = 11;
int pEcho = 4;
long durasi;
int jarak;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pTrig, OUTPUT);
  pinMode(pEcho, INPUT);
}

void loop() {  
  jarak = trig();
  Serial.println(jarak);
  delay(1000);
}

long trig(){
  digitalWrite(pTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pTrig, LOW);
  durasi = pulseIn(pEcho, HIGH);
  return (durasi / 29) / 2;
}

