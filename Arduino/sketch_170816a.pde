import processing.serial.*;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.*;
import java.lang.*;

Serial mySerial;
PrintWriter output;
int flag = 0;
String datafile = "testData.txt";

void setup() {
  mySerial = new Serial( this, Serial.list()[0], 9600 );  //"/dev/ttyACM1", 9600 );// Serial.list()[0], 9600 );
  output = createWriter( "test.txt" );
}
void draw() {
  
  try{
    if (mySerial.available() > 0 ) {
      String value = mySerial.readString();
      if ( value != null ) {
        output.println( value );
        request(value);
        if (flag==0){
          saveData(datafile, value, false);
          flag = 1;
        }
        else{
          saveData(datafile, value, true);
        }
      }
    }
  } catch(IOException ioEx){}
}

void keyPressed() {
  output.flush();  // Writes the remaining data to the file
  output.close();  // Finishes the file
  exit();  // Stops the program
}

void saveData(String fileName, String newData, boolean appendData){
  BufferedWriter bw = null;
  try {  
    FileWriter fw = new FileWriter(fileName, appendData);
    bw = new BufferedWriter(fw);
    bw.write(newData + System.getProperty("line.separator"));
  } catch (IOException e) {
  } finally {
    if (bw != null){
      try { 
        bw.close(); 
      } catch (IOException e) {}  
    }
  }
}

void request(String newData) throws IOException{
  try{
    String[] cmd = {"./Publish.sh", newData};  //"sh", "Publish.sh", "~/home/panos/Desktop/Arduino/processing-3.3.5/Publish.sh"
    Runtime.getRuntime().exec(cmd);
  } catch (IOException e){}
}