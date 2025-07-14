const byte OutPinTMS1 = 18;    // Magventure
const byte OutPinTMS2 = 14;    // Neurosoft
String commandShotTMS = "";
unsigned long DelayTime = 0;
unsigned long TriggerPeakDuration = 300; // em microssegundos
volatile unsigned long microsOfRisingTMS;
int myTimeout = 5;
unsigned long ISI_inib = 4;
int ISI_exci = 18;
int searchcoil1 = 2;
int searchcoil2 = 3;
unsigned long millisCondicionante = 0;
unsigned long millisTeste = 0;
unsigned long latenciaSearchcoils = 0;
int commandISI = 0;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(myTimeout);
  
  pinMode(OutPinTMS1, OUTPUT);
  pinMode(OutPinTMS2, OUTPUT);
  pinMode(searchcoil1, INPUT);
  pinMode(searchcoil2, INPUT);

  digitalWrite(OutPinTMS1, LOW);
  digitalWrite(OutPinTMS2, LOW);

  attachInterrupt(digitalPinToInterrupt(searchcoil1), cronometro1, RISING);
  attachInterrupt(digitalPinToInterrupt(searchcoil2), cronometro2, RISING);

  Serial.println("Sistema TMS pronto para receber comandos via Serial.");
}

void loop() {
  if (Serial.available() > 0) {
    commandShotTMS = ReadCommand();
    Serial.print("Comando recebido: [");
    Serial.print(commandShotTMS);
    Serial.println("]");

    if (commandShotTMS == "single") {
      Serial.println("Executando protocolo simples (SimpleProtocol)");
      SimpleProtocol();
    } else {
      commandISI = commandShotTMS.toInt();
      Serial.print("Executando protocolo pareado (ISIProtocol) com ISI = ");
      Serial.print(commandISI);
      Serial.println(" ms");
      ISIProtocol();
    }
  }
}

void cronometro1() {
  millisCondicionante = micros();
  Serial.print("Condicionante detectado em: ");
  Serial.println(millisCondicionante);
}

void cronometro2() {
  millisTeste = micros();
  Serial.print("Teste detectado em: ");
  Serial.println(millisTeste);
}

void SimpleProtocol() {
  digitalWrite(OutPinTMS2, HIGH);
  delayMicroseconds(TriggerPeakDuration);
  digitalWrite(OutPinTMS2, LOW);
  Serial.println("Pulso simples enviado.");
}

void ISIProtocol() {
  digitalWrite(OutPinTMS1, HIGH);               // condicionante
  delay(commandISI);                            // ISI em ms
  digitalWrite(OutPinTMS2, HIGH);               // teste
  delayMicroseconds(TriggerPeakDuration);
  digitalWrite(OutPinTMS1, LOW);
  digitalWrite(OutPinTMS2, LOW);

  latenciaSearchcoils = millisTeste - millisCondicionante;
  Serial.print("Latência entre searchcoils: ");
  Serial.print(latenciaSearchcoils);
  Serial.println(" us");
}

String ReadCommand() {
  String str = Serial.readString();
  str.trim();
  return str;
}
