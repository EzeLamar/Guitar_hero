
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH1106.h>
#include "OLED.h"

// CLK - GPIO14
#define PIN_CLK 14

// MOSI - GPIO 13
#define PIN_MOSI 13

// RESET - GPIO 26
#define PIN_RESET 16

// DC - GPIO 27
#define PIN_DC 17

// CS - GPIO 15
#define PIN_CS 15

Adafruit_SH1106 display(PIN_MOSI, PIN_CLK, PIN_DC, PIN_RESET, PIN_CS);

void OLEDsetup(){
  display.begin(SH1106_SWITCHCAPVCC);  
  // Clear the buffer.
  display.clearDisplay();
  
}


  
void conectar(){
  //display.clearDisplay();
  display.setTextSize(2.2);
  display.setTextColor(WHITE);
  display.setCursor(5,10);
  display.println("Conectando");
  display.setCursor(20,35);
  display.println(". . . .");
  
  display.display();
}


void desconectar(){
  display.clearDisplay();
  display.setTextSize(5);
  display.setTextColor(WHITE);
  display.setCursor(10,10);
  display.println("Desconectado");
  //display.println("!");
}

void vic_der(char letra){
  display.clearDisplay();
  display.setTextSize(5);
  display.setTextColor(WHITE);
  display.setCursor(10,10);
  switch(letra){
    case 'F':
      display.print("Horrible");
      break;
    case 'A':
    case 'B':
    case 'C':
    case 'D':
      display.print("Victoria");
      break;
    case 'S':
      display.print("Perfec");
      break;
    
  }
}

void multiplicador(int mul){
  display.clearDisplay();
  display.setTextSize(5);
  display.setTextColor(WHITE);
  display.setCursor((display.width()/4), (display.height()/3));
  switch(mul){
    case 1:
      display.println("1X");  
      break;
    case 2:
      display.println("2X");
      break;
    case 3:
      display.println("3X");
      break;
    case 4:
      //display.println("4X");
      break;
    case 6:
      display.println("6X");
      break;
    case 8:
      display.println("8X");
      break;
  }
  display.display();  
}

