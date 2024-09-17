const byte OutPinTMS1 = 18;    // Send TTL to TMS, define Arduino port NUM
const byte OutPinTMS2 = 14;    // Send TTL to TMS, define Arduino port NUM
String commandShotTMS = "";   // String received command for Stimulus
unsigned long DelayTime = 0;            // Delay compared to Trigger pulse in us
unsigned long TriggerPeakDuration = 200; // Trigger pulse Peak duration in us
volatile unsigned long microsOfRisingTMS;  // Timing control for Stimulus and Trigger
int myTimeout = 5; // milliseconds for Serial.readString
int ISI_inib = 2; // in miliseconds
int ISI_exci = 18; // in miliseconds
bool checkHigh = false;

void setup() {
  //Serial.begin(115200);
  Serial.begin(9600);
  Serial.setTimeout(myTimeout);
  pinMode(OutPinTMS1, OUTPUT);
  pinMode(OutPinTMS2, OUTPUT);
  digitalWrite(OutPinTMS1, LOW);
  digitalWrite(OutPinTMS2, LOW);
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
  }

}

// Read the serial port and return command
String ReadCommand() {
  String str = Serial.readString();
  str.trim();
  microsOfRisingTMS = micros();
  checkHigh = true;
  return str;
}