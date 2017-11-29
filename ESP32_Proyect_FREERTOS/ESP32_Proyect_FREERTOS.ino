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

 //Teclas
 #define TECLA1 26
 #define TECLA2 25
 #define TECLA3 33
 #define TECLA4 32
 #define TECLA5 35
 #define TECLA6 34
 #define TECLA7 39
 #define TECLA8 48 //---> A CAMBIAR, FALTA SOLDAR ESTA TECLA
 #define VOLUME 36

 //LEDS PINS
 #define Led1 4 
 #define Led2 17
 #define Led3 2
 #define Led4 16

 //TIPOS DE MENSAJES
 #define KEYPRESS 0
 #define VOLUMEN 2
 #define POWUP 1
 #define INICIARJUEGO 12 //borrar
 #define REFRESCO 3
 #define MASMENOSPOWUP 4
 #define VICTDERR 5
 #define MULTIPLICADOR 6
 
 //WIFI
 //const char* ssid     = "BVNET-A1F2";
 //const char* password = "YHA34R4KN7TLUEXY";
 //const char* ssid     = "GARCIA";
 //const char* password = "00438038265";
 const char* ssid     = "CECom's WiFi";
 const char* password = "graciasfabi";
 //const char* ssid     = "r_laboratorios";
 //const char* password = "laquesea-2012";
 const char* IPservidor   = "192.168.1.126";
 #define port 8888
 int sockfd = 0, n = 0;
 char recvBuff[1024];
 struct sockaddr_in serv_addr; 
  
  int VolAnt=0;
  int contador=0;
  int cambio=0;
  bool  activado=false;
  int flagIniFinGame=0;

  //variable de FREERTOS
  char task1Param[12] = "taskParam";
  //FREERTOS Tareas
  TaskHandle_t t1 = NULL;
  TaskHandle_t t2 = NULL;
  TaskHandle_t tVic = NULL;
  TaskHandle_t tDer = NULL;
  int count = 0;

void setup() {

  Serial.begin(112500);
  
  pinMode(Led1,OUTPUT);
  pinMode(Led2,OUTPUT);
  pinMode(Led3,OUTPUT);
  pinMode(Led4,OUTPUT);  

   
  
  /* we create a new task here */
  xTaskCreate(
      task1,           /* Task function. */
      "task1",        /* name of task. */
      10000,                    /* Stack size of task */
      (void *)task1Param,                     /* parameter of the task */
      1,                        /* priority of the task */
      &t1);                    /* Task handle to keep track of created task */
  /* let task1 run first then create task2 */
  xTaskCreate(
      task2,           /* Task function. */
      "task2",        /* name of task. */
      10000,                    /* Stack size of task */
      (void *)task1Param,                     /* parameter of the task */
      1,                        /* priority of the task */
      &t2);                    /* Task handle to keep track of created task */
}

/* the forever loop() function is invoked by Arduino ESP32 loopTask */
void loop() {

}
/* this function will be invoked when additionalTask was created */
void EncenderLEDS(int x){ //enciende los LEDS de a uno o mas, esto indica la cant de power up que tenemos
  switch(x){
    case 0:
      activado=false;
      digitalWrite(Led1,LOW);
      digitalWrite(Led2,LOW);
      digitalWrite(Led3,LOW);
      digitalWrite(Led4,LOW);
      break;
    case 1:
      digitalWrite(Led1,HIGH);
      break;
    case 2:
      digitalWrite(Led2,HIGH);
      break;
    case 3:
      digitalWrite(Led3,HIGH);
      break;
    case 4:
      digitalWrite(Led4,HIGH);
      break;
      
   }
  }

byte getBotones(){
  byte salida= 0;
  if(digitalRead(TECLA5)==LOW){
    //Serial.println("TECLA1");
    //write(sockfd, "TECLA1", 6);
    salida |= B00000001;
   }
   if(digitalRead(TECLA4)==LOW){
    //Serial.println("TECLA2");
    //write(sockfd, "TECLA2", 6);
    salida |= B00000010;
   }
   if(digitalRead(TECLA3)==LOW){
    //Serial.println("TECLA3");
    //write(sockfd, "TECLA3\n", 8);
    salida |= B00000100;
   }
   if(digitalRead(TECLA2)==LOW){
    //Serial.println("TECLA4");
    //write(sockfd, "TECLA4\n", 8);
    salida |= B00001000;
   }
   if(digitalRead(TECLA1)==LOW){
    //Serial.println("TECLA5");
    //close(sockfd); //TESTING de sesion
    //write(sockfd, "TECLA5\n", 8);
    salida |= B00010000;
   }
   if(digitalRead(TECLA7)==LOW){
    //Serial.println("TECLA6");
    //write(sockfd, "TECLA6\n", 8);
    salida |= B00100000;
    
   }
   if(digitalRead(TECLA6)==LOW){
    //Serial.println("TECLA7");
    //write(sockfd, "TECLA7\n", 8);
    salida |= B01000000;
    
   }
   //RESET
   if(salida==96){
    close(sockfd);
    ESP.restart();
   }
    
   Serial.println(salida);
   return salida;
}
byte obtVolumen(){
  byte volumen=0;
  int adc=analogRead(VOLUME);
  //delay(10);
  //if(abs(antADC-adc)>500)
  //volumen=0;
  
  Serial.print("ADC: ");
  Serial.println(adc);

  if(adc<820)
    volumen=0;
  else if(adc<1640)
         volumen=1;
       else if(adc<2460)
              volumen=2;
            else if(adc<3280)
                    volumen=3;
                 else
                 volumen=4; 
  
  if(adc<50)
        volumen=0;
  if(adc<450 && adc>=50)
        volumen=0;
  if(adc<850 && adc>=500)
        volumen=1;
  if(adc<1250 && adc>=900)
        volumen=1;
  if(adc<1650 && adc>=1300)
        volumen=2;
  if(adc<2050 && adc>=1700)
        volumen=2;
  if(adc<2450 && adc>=2100)
        volumen=3;
  if(adc<2850 && adc>=2500)
        volumen=3;
  if(adc<3250 && adc>=2900)
        volumen=4;   
  if(adc<3650 && adc>=3300)
        volumen=4;  
  if(adc<4096 && adc>=3700)
        volumen=4;  
  Serial.print("VOLUMEN: ");
  Serial.println(volumen);
       
  return volumen;

}
void EfectoVicDerrot(int y){ //efecto de luces que dice si se gano o perdio el juego
  if(y==1)
  xTaskCreate(
      taskGane,           /* Task function. */
      "taskGane",        /* name of task. */
      10000,                    /* Stack size of task */
      (void *)task1Param,                     /* parameter of the task */
      1,                        /* priority of the task */
      &tVic);                    /* Task handle to keep track of created task */
  else
   xTaskCreate(
      taskPerdi,           /* Task function. */
      "taskPerdi",        /* name of task. */
      10000,                    /* Stack size of task */
      (void *)task1Param,                     /* parameter of the task */
      1,                        /* priority of the task */
      &tDer);
  
}

void CambiarOLEDMult(int z){ //muestra un x1 o x2
  
}
 int handleError(const char *s)
{
  printf("%s: %s\n", s, strerror(errno));
  exit(1);
}

void taskGane( void * parameter )
{
  for(;;){
    for(int w=0; w<5; w++)
    EncenderLEDS(w);
    
    vTaskDelay(50);
    EncenderLEDS(0);
    vTaskDelay(50);
  }
  vTaskDelete(NULL);
}
void taskPerdi( void * parameter )
{
 for(;;){
   EncenderLEDS(2);
   EncenderLEDS(3);
   vTaskDelay(100);
   EncenderLEDS(0);//apago
   EncenderLEDS(4);
   EncenderLEDS(1);
   vTaskDelay(100);
   EncenderLEDS(0);
   vTaskDelay(50);
   for(int w=0; w<4; w++){
    EncenderLEDS(1);
    EncenderLEDS(2);
    EncenderLEDS(3);
    EncenderLEDS(4);
    vTaskDelay(500);
    EncenderLEDS(0);
    vTaskDelay(500);
   }
   vTaskDelete(NULL);
   
 }
}
void task1( void * parameter )
{
  
  
  
  
  
  Serial.println((char *)parameter);
  /* loop forever */
  int i=0;
  for(;;){
    //Serial.println("Task1");
    EncenderLEDS(i);
    i++;
    
    if(i>4)
    i=0;
    vTaskDelay(200);
    //multiplicador(i);
    //conectar();
  }
  /* delete a task when finish, 
  this will never happen because this is infinity loop */
  vTaskDelete( NULL );
}


/* this function will be invoked when additionalTask was created */
void task2( void * parameter )
{
  //Defino los pines como entrada
  pinMode(TECLA1,INPUT);
  pinMode(TECLA2,INPUT);
  pinMode(TECLA3,INPUT);
  pinMode(TECLA4,INPUT);
  pinMode(TECLA5,INPUT);
  pinMode(TECLA6,INPUT);
  pinMode(TECLA7,INPUT);
  pinMode(VOLUME,ANALOG);
  
  Serial.println((char *)parameter);
  Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.enableSTA(true);
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

    if(inet_pton(AF_INET, IPservidor, &serv_addr.sin_addr)<=0)
    {
        Serial.print("\n inet_pton error occured\n");
        ///return 1;
    } 

    if( connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
       Serial.print("\n Error : Connect Failed \n");
       //return 1;
    }
    //Al conectarme finalizo la tarea de los leds de estado inicial
    vTaskDelete(t1);
    EncenderLEDS(0); //apago todos los leds
    
  /* loop forever */
  for(;;){
    char apretados= getBotones()+63; //SE SUMA 63 DEBIDO A QUE LOS PRIMEROS 64 CARACTERES, SON PROBLEMATICOS

    int potenciometro=obtVolumen(); //IDEM

   uint8_t send_buf[8]; //arreglo que almacena la informacion a transmitir
   bzero(&recvBuff,8);
   int recibido=recv( sockfd, &recvBuff, 1024, 0);
   if (recibido>0){
     //veo el tipo de mensaje que me llega
     Serial.println(recvBuff);
     int j=0;
     while(recvBuff[j]!= '<'){
        j++; //consumo caracteres hasta llegar al caracter de inicio de trama (paquete del juego)
     }

      
     
     if(recvBuff[j+2]=='$'){
      int tipoMensaje= atoi(&(recvBuff[j+3])); //dependiendo del tipo, de mensaje recibido, se debe modificar el estado de la guitarra , o bien, indicar que la misma puede transmitir (tiempo de refresco)
      Serial.print(tipoMensaje);
       // if(tipoMensaje=INICIARJUEGO){
        //  flagIniFinGame=1;
          //}
        if(tipoMensaje==REFRESCO){ //tipo de refresco
          //comienzo a armar tramas para enviar mensajes
          //if(flagIniFinGame){
              //if(digitalRead(TECLA6)==LOW){
                contador++;
                sprintf((char*)send_buf, "<%i$%i$%c>",7, KEYPRESS, apretados); //solo se manda este mensaje si esta en modo juego
                write(sockfd, send_buf, 7);
                if(contador==10){
                if(potenciometro!=VolAnt){
                bzero(&send_buf,8);
                sprintf((char*)send_buf, "<%i$%i$%d>",7, VOLUMEN, potenciometro);
                //Serial.println((char *) send_buf);
                write(sockfd, send_buf, 7);
                VolAnt=potenciometro;
                }
                contador=0;
                }
                //Serial.println("entro a teclas");            //  }
              //FALTARIA HACER LA PARTE DE IN GAME, CUANDO MANDO EL POWER UP
              if(digitalRead(TECLA6)==LOW && cambio > 2 && !activado){
                  activado=true;
                  sprintf((char*)send_buf, "<%i$%i$>",6, POWUP); //solo se manda este mensaje si esta en modo juego
                  write(sockfd, send_buf, 6);
                 Serial.println("entro a power up"); 
                }
        }
       else{ 
        //es un mensaje de modificacion
          switch(tipoMensaje){
                case MASMENOSPOWUP: //incrementar o disminuir power up (encender leds)
                   {
                    if(recvBuff[j+4]=='$'){

                      cambio =atoi(&(recvBuff[j+5]));
                      
                      EncenderLEDS(cambio);
                    }
                   }
                break;
 
                case VICTDERR: //mensaje de victoria o derrota (cambiar colores de leds)
                  {
                    if(recvBuff[j+4]=='$'){

                      int victder =atoi(&(recvBuff[j+5]));
                      
                      EfectoVicDerrot(victder);
                      flagIniFinGame=0;
                    }
                  }
                break;

                case MULTIPLICADOR: //cuando junto suficientes aciertos aumenta el multiplicador (o uso el power up) y si erro vuelve a x1.
                  {
                     if(recvBuff[j+4]=='$'){

                      int mult =atoi(&(recvBuff[j+5]));
                      
                      CambiarOLEDMult(mult);
                    }
                  }
                break;
                }
        
        }
     }
   }else {
      //if(recibido==-1)
        //desconectar();
        //1=1;
   }
     // Serial.println((char *) send_buf);

  }
  /* delete a task when finish, 
  this will never happen because this is infinity loop */
  vTaskDelete( NULL );
}
