#include <WiFi.h>
#include <iostream>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
using namespace std;

const char* ssid     = "TU VIEJA";
const char* password = "EN TANGA";

const char* streamId   = "192.168.0.21";
  

#define port 8888

  int sockfd = 0, n = 0;
  char recvBuff[1024];
  struct sockaddr_in serv_addr; 

/*CREACION DE UN SOCKET
 * La secuencia resumida de llamadas al sistema es:
 * 
 * 1. --> socket()
 * 2. --> bind()
 * 3. --> listen()
 * 4. --> accept()
 */

 //Teclas
 #define TECLA1 26
 #define TECLA2 25
 #define TECLA3 33
 #define TECLA4 32
 #define TECLA5 35
 #define TECLA6 34
 #define TECLA7 39
 #define TECLA8 48 //---> A CAMBIAR, FALTA SOLDAR ESTA TECLA
 #define VOLUME 27

//TIPOS DE MENSAJES
 #define KEYPRESS
 #define VOLUMEN
 #define POWUP
 #define INICIARJUEGO
 #define REFRESCO
 #define MASMENOSPOWUP
 #define VICTDERR
 #define MULTIPLICADOR
 
//esto sirve para saber si el juego esta en curso (1) o no (0)
 int flagIniFinGame=0;
void setup()
{
    Serial.begin(115200);
    delay(10);
    //Defino los pines como entrada
    pinMode(TECLA1,INPUT);
    pinMode(TECLA2,INPUT);
    pinMode(TECLA3,INPUT);
    pinMode(TECLA4,INPUT);
    pinMode(TECLA5,INPUT);
    pinMode(TECLA6,INPUT);
    pinMode(TECLA7,INPUT);

    // We start by connecting to a WiFi network

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    //SOCKET

    memset(recvBuff, '0',sizeof(recvBuff));
    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        Serial.print("\n Error : Could not create socket \n");
        //return 1;
    } 

    memset(&serv_addr, '0', sizeof(serv_addr)); 

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(port); 

    if(inet_pton(AF_INET, "192.168.0.21", &serv_addr.sin_addr)<=0)
    {
        Serial.print("\n inet_pton error occured\n");
        ///return 1;
    } 

    if( connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
       Serial.print("\n Error : Connect Failed \n");
       //return 1;
    }

}
int handleError(const char *s)
{
  printf("%s: %s\n", s, strerror(errno));
  exit(1);
}


int value = 0;

byte getBotones(){
  byte salida= 0;
  if(digitalRead(TECLA1)==LOW){
    //Serial.println("TECLA1");
    //write(sockfd, "TECLA1", 6);
    salida |= B00000001;
   }
   if(digitalRead(TECLA2)==LOW){
    //Serial.println("TECLA2");
    //write(sockfd, "TECLA2", 6);
    salida |= B00000010;
   }
   if(digitalRead(TECLA3)==LOW){
    //Serial.println("TECLA3");
    //write(sockfd, "TECLA3\n", 8);
    salida |= B00000100;
   }
   if(digitalRead(TECLA4)==LOW){
    //Serial.println("TECLA4");
    //write(sockfd, "TECLA4\n", 8);
    salida |= B00001000;
   }
   if(digitalRead(TECLA5)==LOW){
    //Serial.println("TECLA5");
    //close(sockfd); //TESTING de sesion
    //write(sockfd, "TECLA5\n", 8);
    salida |= B00010000;
   }
   if(digitalRead(TECLA6)==LOW){
    //Serial.println("TECLA6");
    //write(sockfd, "TECLA6\n", 8);
    salida |= B00100000;
   }
   if(digitalRead(TECLA7)==LOW){
    //Serial.println("TECLA7");
    //write(sockfd, "TECLA7\n", 8);
    salida |= B01000000;
   }
   Serial.println(salida);
   return salida;
}


byte obtVolumen(){
  byte volumen=0;
  int adc=analogRead(TECLA6);
  if(adc<50)
        volumen=0;
  if(adc<450 && adc>=50)
        volumen=1;
  if(adc<850 && adc>=500)
        volumen=2;
  if(adc<1250 && adc>=900)
        volumen=3;
  if(adc<1650 && adc>=1300)
        volumen=4;
  if(adc<2050 && adc>=1700)
        volumen=5;
  if(adc<2550 && adc>=2100)
        volumen=6;
  if(adc<2850 && adc>=2600)
        volumen=7;
  if(adc<3350 && adc>=2900)
        volumen=8;   
  if(adc<3850 && adc>=3400)
        volumen=9;  
  if(adc<4000 && adc>=3900)
        volumen=10;       
  return volumen;

}

void EncenderLEDS(int x){ //enciende los LEDS de a uno o mas, esto indica la cant de power up que tenemos
  
  }

void EfectoVicDerrot(int y){ //efecto de luces que dice si se gano o perdio el juego
  
}

void CambiarOLEDMult(int z){ //muestra un x1 o x2
  
}

void loop()
{

  
   byte apretados= getBotones();

   byte potenciometro=obtVolumen();

   uint8_t send_buf[20]; //arreglo que almacena la informacion a transmitir
   
   if (recv( sockfd, *recvBuff, 1024, 0)>0){
     //veo el tipo de mensaje que me llega
     int j=0;
     while(recvBuff[j]!= '<'){
        j++; //consumo caracteres hasta llegar al caracter de inicio de trama (paquete del juego)
     }
      
     
     if(recvBuff[j+2]=='$'){
      int tipoMensaje= atoi(recvBuff[j+3]); //dependiendo del tipo, de mensaje recibido, se debe modificar el estado de la guitarra , o bien, indicar que la misma puede transmitir (tiempo de refresco)
        if(tipoMensaje=INICIARJUEGO){
          flagIniFinGame=1;
          }
        if(tipoMensaje==REFRESCO){ //tipo de refresco
          //comienzo a armar tramas para enviar mensajes
          if(flagIniFinGame){
              if(digitalRead(TECLA7)==LOW){
                sprintf((char*)send_buf, "<%i$%i$%i>",10, KEYPRESS, apretados); //solo se manda este mensaje si esta en modo juego
                write(sockfd, send_buf, 20);
              }
              //FALTARIA HACER LA PARTE DE IN GAME, CUANDO MANDO EL POWER UP
              if(digitalRead(TECLA8)==LOW)
                  sprintf((char*)send_buf, "<%i$%i$>",10, POWUP); //solo se manda este mensaje si esta en modo juego
                write(sockfd, send_buf, 20);
           }
          else {
              //si estoy en modo menu
              //deberia mandar de a un solo bit a la vez (solo mando si la combinacion es 0 y un solo 1)
              switch(apretados){
                case 1 , 2, 4, 8, 16, 32: // se necesitan 2 botones de seleccion y uno de start, luego ver esto
                  {
                  sprintf((char*)send_buf, "<%i$%i$%i>",10, KEYPRESS, apretados);
                  write(sockfd, send_buf, 20);
                  }
                break;
                
                }
              
            }
                
           sprintf((char*)send_buf, "<%i$%c$%i>",10, VOLUMEN, potenciometro); //el volumen se manda siempre, si no hay cambios, no cambia el volumen
           write(sockfd, send_buf, 20);
        }
       else{ 
        //es un mensaje de modificacion
          switch(tipoMensaje){
                case MASMENOSPOWUP: //incrementar o disminuir power up (encender leds)
                   {
                    if(recvBuff[j+4]=='$'){

                      int cambio =atoi(recvBuff[j+5]);
                      
                      EncenderLEDS(cambio);
                    }
                   }
                break;

                case VICTDERR: //mensaje de victoria o derrota (cambiar colores de leds)
                  {
                    if(recvBuff[j+4]=='$'){

                      int victder =atoi(recvBuff[j+5]);
                      
                      EfectoVicDerrot(victder);
                      flagIniFinGame=0;
                    }
                  }
                break;

                case MULTIPLICADOR: //cuando junto suficientes aciertos aumenta el multiplicador (o uso el power up) y si erro vuelve a x1.
                  {
                     if(recvBuff[j+4]=='$'){

                      int mult =atoi(recvBuff[j+5]);
                      
                      CambiarOLEDMult(mult);
                    }
                  }
                break;
                }
        
        }
     }
   }
   
      Serial.println((char *) send_buf);
    
   
   delay(5); 
}
