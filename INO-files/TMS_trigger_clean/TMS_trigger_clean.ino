const byte OutPinTMS1 = 18;    // Send TTL to TMS, define Arduino port NUM, Magventure
const byte OutPinTMS2 = 14;    // Send TTL to TMS, define Arduino port NUM, Neurosoft
String commandShotTMS = "";   // String received command for Stimulus
unsigned long DelayTime = 0;            // Delay compared to Trigger pulse in us
unsigned long TriggerPeakDuration = 300; // Trigger pulse Peak duration in us
volatile unsigned long microsOfRisingTMS;  // Timing control for Stimulus and Trigger
int myTimeout = 5; // milliseconds for Serial.readString
unsigned long ISI_inib = 4; // in miliseconds
int ISI_exci = 18; // in miliseconds
int searchcoil1=2; // Tem que estar na saída do TMS1, associado ao pulso condicionante
int searchcoil2=3; //Tem que estar na saída do TMS2, pulso teste
// #define searchcoil1 2; // searchcoil associada ao estímulo condicionante, ligada ao pino 2 (interrupção 0 no Arduino Mega)
// #define searchcoil2 3; // searchcoil associada ao estímulo teste, ligada ao pino 3 (interrupção 1 no Arduino Mega)
unsigned long millisCondicionante=0; //tempo associado à detecção do estímulo condicionante (talvez transformar essa variável num vetor)
unsigned long millisTeste=0; //tempo associado à detecção do estímulo teste (talvez transformar essa variável num vetor)
unsigned long latenciaSearchcoils=0; //latência entre os pulsos, determinada a partir das respostas das searchcoils (talvez transformar num vetor)


void setup() {
  Serial.begin(9600);
  Serial.setTimeout(myTimeout);
  pinMode(OutPinTMS1, OUTPUT);
  pinMode(OutPinTMS2, OUTPUT);
  pinMode(searchcoil1,INPUT);
  pinMode(searchcoil2,INPUT);
  digitalWrite(OutPinTMS1, LOW);
  digitalWrite(OutPinTMS2, LOW);
  attachInterrupt(digitalPinToInterrupt(searchcoil1), cronometro1, RISING); //interromper o código quando detectar RISING na searchcoil1, pra chamar a função cronometro1 e salvar o instante do estímulo condicionante
  attachInterrupt(digitalPinToInterrupt(searchcoil2), cronometro2, RISING); //interromper o código quando detectar RISING na searchcoil2, pra chamar a função cronometro2 e salvar o instante do estímulo teste
}

void loop() {
  // Identify the command on serial port and take the value
  if (Serial.available() > 0) commandShotTMS = ReadCommand();

  if (commandShotTMS == "1") SimpleProtocol();

  if (commandShotTMS == "2") InhibitoryProtocol();

  if (commandShotTMS == "3") ExcitatoryProtocol();
}

void cronometro1 () {
  //Serial.print("Tempo millisCondicionante: ");
   millisCondicionante = micros();
   //Serial.println(millisCondicionante);
}

void cronometro2 () {
  //Serial.print("Tempo millisTeste: ");
  millisTeste = micros();
  //Serial.println(millisTeste); //NAO TA PRINTANDO
  latenciaSearchcoils = millisTeste - millisCondicionante;
  Serial.println(latenciaSearchcoils);
}

void SimpleProtocol() {
  digitalWrite(OutPinTMS2, HIGH);
  delayMicroseconds(TriggerPeakDuration);
  digitalWrite(OutPinTMS2, LOW);
  commandShotTMS = "";
}

void InhibitoryProtocol() {
  //microsOfRisingTMS = micros();
  digitalWrite(OutPinTMS1, HIGH);
  delayMicroseconds(3950);
  //delay(1);
  //while ((micros() - microsOfRisingTMS) < TriggerPeakDuration) {

  //}
  digitalWrite(OutPinTMS2, HIGH);
  digitalWrite(OutPinTMS1, LOW);
  delayMicroseconds(TriggerPeakDuration);
  digitalWrite(OutPinTMS2, LOW);
  commandShotTMS = "";
}

void ExcitatoryProtocol() {
  digitalWrite(OutPinTMS1, HIGH);
  delay(ISI_exci);
  digitalWrite(OutPinTMS2, HIGH);
  digitalWrite(OutPinTMS1, LOW);
  delayMicroseconds(TriggerPeakDuration);
  digitalWrite(OutPinTMS2, LOW);
  commandShotTMS = "";
}

// Read the serial port and return command
String ReadCommand() {
  String str = Serial.readString();
  str.trim();
  return str;
}