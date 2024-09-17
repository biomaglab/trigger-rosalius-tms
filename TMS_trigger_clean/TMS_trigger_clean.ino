const byte OutPinTMS1 = 18;    // Send TTL to TMS, define Arduino port NUM
const byte OutPinTMS2 = 14;    // Send TTL to TMS, define Arduino port NUM
String commandShotTMS = "";   // String received command for Stimulus
unsigned long DelayTime = 0;            // Delay compared to Trigger pulse in us
unsigned long TriggerPeakDuration = 200; // Trigger pulse Peak duration in us
volatile unsigned long microsOfRisingTMS;  // Timing control for Stimulus and Trigger
int myTimeout = 5; // milliseconds for Serial.readString
int ISI_inib = 4; // in miliseconds
int ISI_exci = 18; // in miliseconds
bool checkHigh = false;
#define searchcoil1 2; // searchcoil associada ao estímulo condicionante, ligada ao pino 2 (interrupção 0 no Arduino Mega)
#define searchcoil2 3; // searchcoil associada ao estímulo teste, ligada ao pino 3 (interrupção 1 no Arduino Mega)
unsigned long millisCondicionante=0; //tempo associado à detecção do estímulo condicionante (talvez transformar essa variável num vetor)
unsigned long millisTeste=0; //tempo associado à detecção do estímulo teste (talvez transformar essa variável num vetor)
unsigned long latenciaSearchcoils=0; //latência entre os pulsos, determinada a partir das respostas das searchcoils (talvez transformar num vetor)


void setup() {
  //Serial.begin(115200);
  Serial.begin(9600);
  Serial.setTimeout(myTimeout);
  pinMode(OutPinTMS1, OUTPUT);
  pinMode(OutPinTMS2, OUTPUT);
  pinMode(searchcoil1,INPUT);
  pinMode(searchcoil2,INPUT);
  digitalWrite(OutPinTMS1, LOW);
  digitalWrite(OutPinTMS2, LOW);
  attachinterrupt(digitalPinToInterrupt(searchcoil1), cronometro1, RISING); //interromper o código quando detectar RISING na searchcoil1, pra chamar a função cronometro1 e salvar o instante do estímulo condicionante
  attachinterrupt(digitalPinToInterrupt(searchcoil2), cronometro2, RISING); //interromper o código quando detectar RISING na searchcoil2, pra chamar a função cronometro2 e salvar o instante do estímulo teste
}

void loop() {
  // Identify the command on serial port and take the value
  if (Serial.available() > 0) commandShotTMS = ReadCommand();

  // Send TTL to TMS and EMG if the command corresponds -> process 1

//////////////////////////////////////// SIMPLES ////////////////////////////////////////
  if ((commandShotTMS == "1") && checkHigh){
   digitalWrite(OutPinTMS2, HIGH);
   checkHigh = false;
  }
  // Finish the process 1
  if ((commandShotTMS == "1") && ((micros() - microsOfRisingTMS) >= TriggerPeakDuration)) {
    digitalWrite(OutPinTMS2, LOW);
    commandShotTMS = "";
  }

//////////////////////////////////////// INIBITORIO ////////////////////////////////////////

  if ((commandShotTMS == "2") && checkHigh){
   digitalWrite(OutPinTMS1, HIGH);
   //Serial.print(digitalRead(OutPinTMS1));
   delay(ISI_inib);
   digitalWrite(OutPinTMS2, HIGH);
   checkHigh = false;
  }
  // Finish the process 1
  if ((commandShotTMS == "2") && ((micros() - microsOfRisingTMS) >= TriggerPeakDuration)) {
    digitalWrite(OutPinTMS1, LOW);
    digitalWrite(OutPinTMS2, LOW);
    //Serial.print(digitalRead(OutPinTMS1));
    commandShotTMS = "";
    latenciaSearchcoils = millisTeste - millisCondicionante;
    serial.println(latenciaSearchcoils);
  }

//////////////////////////////////////// EXCITATORIO ////////////////////////////////////////
  if ((commandShotTMS == "3") && checkHigh){
   digitalWrite(OutPinTMS1, HIGH);
   //Serial.print(digitalRead(OutPinTMS1));
   delay(ISI_exci);
   digitalWrite(OutPinTMS2, HIGH);
   checkHigh = false;
  }
  // Finish the process 1
  if ((commandShotTMS == "3") && ((micros() - microsOfRisingTMS) >= TriggerPeakDuration)) {
    digitalWrite(OutPinTMS1, LOW);
    digitalWrite(OutPinTMS2, LOW);
    //Serial.print(digitalRead(OutPinTMS1));
    commandShotTMS = "";
    latenciaSearchcoils = millisTeste - millisCondicionante;
    serial.println(latenciaSearchcoils);
  }

}

void cronometro1 () {
  millisCondicionante = millis();
}

void cronometro2 () {
  millisTeste = millis();
}

// Read the serial port and return command
String ReadCommand() {
  String str = Serial.readString();
  str.trim();
  microsOfRisingTMS = micros();
  checkHigh = true;
  return str;
}