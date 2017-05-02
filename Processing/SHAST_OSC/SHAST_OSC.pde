import processing.video.*;
import controlP5.*;
import oscP5.*;
import netP5.*;
import ddf.minim.analysis.*;
import ddf.minim.*;

// ===== CONFIG. ABELHAS ===== //
static final int n_abelhas = 9;
static final int altura_abelha = 55;
// =========================== //

static final int TELA_X = 1024;
static final int TELA_Y = 768;

NetAddress myBroadcastLocation; 
OscP5 oscP5;
ControlP5 controlP5;
CheckBox checkbox;
Minim       minim;
AudioPlayer bzz;
FFT         fft;
Abelha[] abelha;

int milisegundos, millis_envio_ip;
int reconectar = 0;
int pos_abelha = 0, pos_anterior = 0;
boolean edges = true;
boolean blobs = true;
boolean osc_conectado = false;
int skip_blobs = 9;
float hexStr;

void setup(){
  // Porta 22243 está configurada no servidor.
  // Servidor local de OSC. Recebe as mensagens.
  oscP5 = new OscP5(this, 22243);
  
  // Configurando o servidor do NANO
  conectar_nano();
  
  println("Compiling...");
  // Tamanho da Janela
  size(TELA_X, TELA_Y);
  
  // ======= ABELHAS ======= //
  abelha = new Abelha[n_abelhas];
  inicializar_abelhas();

  // ======= AUDIO ======= //
  println("Set Audio...");
  minim = new Minim(this);
  bzz = minim.loadFile("abelhas.mp3", 1024);
  bzz.loop();
  fft = new FFT( bzz.bufferSize(), bzz.sampleRate() );

  // ===== CONFIGURAÇÕES ===== //
  controlP5 = new ControlP5(this);
  controlP5.addSlider("skip_blobs", 1, 20, skip_blobs, 20, 40, 100, 10);
  checkbox = controlP5.addCheckBox("checkbox", 20, 60);
  checkbox.addItem("blobs", blobs?1:0);
  checkbox.addItem("edges", edges?1:0);  
  controlP5.hide();
  
  println("Starting...");
  milisegundos = millis();
  millis_envio_ip = milisegundos;
}

void draw(){  
  background(0);
  for(int j = 0; j < n_abelhas; j++)
    abelha[j].move_aleatoriamente();
  
  drawShapes(blobs, edges);
  
  if(millis() - milisegundos > 1500000){ // a cada 15 segundos (15000 milisegundos).
    // Reinicializa as abelhas para manter a atividade.
    inicializar_abelhas();
    milisegundos = millis();
  }
  
  if(millis() - millis_envio_ip > 1800000){
    // A cada 30 minutos reconecta e envia o ip (evita muitos travamentos);
    conectar_nano();
    millis_envio_ip = millis();
  }
}

void oscEvent(OscMessage message) {
  if(message.checkAddrPattern("/shast/coordenada")){
    abelha[pos_abelha].setX((message.get(0).intValue() + message.get(2).intValue())/2);
    abelha[pos_abelha].setY((message.get(1).intValue() +  message.get(3).intValue())/2);
    pos_abelha++;
    if(pos_abelha >= n_abelhas)
      pos_abelha = 0;
  }
}

void conectar_nano(){
  myBroadcastLocation = new NetAddress("146.164.9.237",22244);
  String ip = NetInfo.wan();
  if(ip == null){
    osc_conectado = false;
  } else {
    osc_conectado = true;
    enviar_ip_ao_servidor(ip);
  }
}

void inicializar_abelhas(){
  for(int i = 0; i < n_abelhas; i++)
    abelha[i] = new Abelha();
}

void enviar_ip_ao_servidor(String ip){
  if(osc_conectado && ip != null){
    OscMessage mOscMessage = new OscMessage("/request");
    mOscMessage.add(ip);
    oscP5.send(mOscMessage, myBroadcastLocation);
  } else {
    osc_conectado = false; 
  }
}
