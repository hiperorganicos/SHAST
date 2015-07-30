import processing.video.*;
import blobDetection.*;
import controlP5.*;
import ddf.minim.analysis.*;
import ddf.minim.*;

Movie movie;
Capture cam;
BlobDetection theBlobDetection;
ControlP5 controlP5;
CheckBox checkbox;
Minim       minim;
AudioPlayer bzz;
FFT         fft;


PImage img;
boolean newFrame=false;
//boolean webcam = false; // escolhe entre webcam ou video como fonte de imagem pro blob
boolean striped = false; // aparece as tiras
boolean video = false; // aparece video
boolean edges = true;
boolean blobs = true;
int skip_blobs = 5;
float stripes;
float hexStr;

float t, d;
// ==================================================
// setup()
// ==================================================
void setup()
{
  println("Compiling...");
  // Size of applet
  size(1280, 720);
  
  //--------------------------------------------------------------> video
  println("Set Video...");
  println("Set Movie...");
  movie = new Movie(this, "abelhas.mov");
  movie.loop();
  d = movie.duration();

  // --------------------------------------------------------->> sound
  println("Set Audio...");
  minim = new Minim(this);

  bzz = minim.loadFile("abelhas.mp3", 1024);
  bzz.loop();
  fft = new FFT( bzz.bufferSize(), bzz.sampleRate() );

  // -------------------------------------------------------> interface
  println("Set interface...");
  controlP5 = new ControlP5(this);

  controlP5.addSlider("luminosity", 0.0, 1.0, 0.15, 20, 20, 100, 10);
  controlP5.addSlider("skip_blobs", 1, 20, skip_blobs, 20, 40, 100, 10);

  checkbox = controlP5.addCheckBox("checkbox", 20, 60);
  checkbox.addItem("listrado", striped?1:0); 
  checkbox.addItem("video", video?1:0);
  checkbox.addItem("blobs", blobs?1:0);
  checkbox.addItem("edges", edges?1:0);
  
  // ----------------------------------------------------->  BlobDetection
  img = new PImage(80, 60); 
  theBlobDetection = new BlobDetection(img.width, img.height);
  theBlobDetection.setPosDiscrimination(true);
  theBlobDetection.setThreshold(0.5f); // will detect bright areas whose luminosity > 0.2f;
  println("Running...");
  
  controlP5.hide();
 
}


// ====================================================================================
// draw()
// ===================================================================================
void draw()
{
  if (striped) {
    fill(200, 150, 25);
    rect(0, 0, width, height);
    stroke(0);

    fft.forward( bzz.mix );
    stripes = fft.getBand(0);
  
    stripes = stripes*3;
    for (int i = 0; i < stripes; i++)
    {
      strokeWeight((height/stripes)/2);
      line(0, (height/stripes)*i, width, (height/stripes)*i);
    }
  } else {
    background(0);
  }

  
    img.copy(movie, 0, 0, movie.width, movie.height, 0, 0, img.width, img.height);
  

    if (video) {
      image(img, 0, 0, width, height);
    }

    theBlobDetection.computeBlobs(img.pixels);
    drawShapes(blobs, edges);
  
  if(frameCount < 10){
  saveFrame("SHAST_000" + frameCount);
  }
  if(frameCount >= 10 && frameCount < 100){
  saveFrame("SHAST_00" + frameCount);
  }
  if(frameCount >= 100 && frameCount < 1000){
  saveFrame("SHAST_0" + frameCount);
  }  
  if(frameCount >= 1000 && frameCount < 10000){
  saveFrame("SHAST_" + frameCount);
  } 
  
  t = movie.time();
  if(t>=d){
  exit(); 
  } 
}

