const byte OutPinEMG = 18;    // Send TTL to EMG
const byte OutPinTMS = 21;    // Send TTL to TMS 
const byte InPinTMS = 2;      // Receive signal from TMS
String commandShotTMS = "";   // String received command for Stimulus
unsigned long DelayTime = 4;            // Delay compared to Trigger pulse in us
unsigned long TriggerPeakDuration = 49; // Trigger pulse Peak duration in us
volatile bool Triggered = false;           // Receive signal from TMS flag
volatile unsigned long microsOfRisingEMG;  // Timing control for Trigger
volatile unsigned long microsOfRisingTMS;  // Timing control for Stimulus and Trigger

void setup() {
  //Serial.begin(115200);
  Serial.begin(9600);
  pinMode(OutPinEMG, OUTPUT);
  pinMode(OutPinTMS, OUTPUT);
  pinMode(InPinTMS, INPUT);
  digitalWrite(OutPinTMS, LOW);
  digitalWrite(OutPinEMG, LOW);
  attachInterrupt(digitalPinToInterrupt(InPinTMS), Trigger, RISING);
}

void loop() {
  // Identify the command on serial port and take the value
  if (Serial.available() > 0) commandShotTMS = ReadCommand();

  // Send TTL to TMS and EMG if the command corresponds -> process 1
  if ((commandShotTMS == "a") && (micros() - microsOfRisingTMS) >= DelayTime) SendTTL(2,1);
  
  // Finish the process 1
  if ((commandShotTMS == "a") && ((micros() - microsOfRisingTMS) >= TriggerPeakDuration)) {
    SendTTL(2,0);
    commandShotTMS = "";
  }

  // Send TTL to EMG if TMS was triggered -> process 2
  if ((Triggered) && ((micros() - microsOfRisingEMG) >= DelayTime)) SendTTL(1,1);

  // Finish the process 2
  if ((Triggered) && ((micros() - microsOfRisingEMG) >= TriggerPeakDuration)) {
    SendTTL(1,0);
    Triggered = false;
  }
}

// Identify the trigger from TMS
void Trigger() {
  if ((!Triggered) && (commandShotTMS == "")) {
    microsOfRisingEMG = micros();
    Triggered = true;
    //Serial.println("Trigger");
  }  
}

// Read the serial port and return command
String ReadCommand() {
  String str = Serial.readString();
  str.trim();
  microsOfRisingTMS = micros();
  return str;
}

// Switch to open or close pins on demand
void SendTTL(int numOfPins, int state) {
  if ((numOfPins == 1) && (state == 0)) digitalWrite(OutPinEMG, LOW);
  if ((numOfPins == 1) && (state == 1)) digitalWrite(OutPinEMG, HIGH);
  if ((numOfPins == 2) && (state == 0)) {
      digitalWrite(OutPinTMS, LOW);
      digitalWrite (OutPinEMG, LOW);
  }
  if ((numOfPins == 2) && (state == 1)) {
      digitalWrite(OutPinTMS, HIGH);
      digitalWrite (OutPinEMG, HIGH);
  }
}