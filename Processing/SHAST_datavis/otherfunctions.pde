void movieEvent(Movie m) {
  m.read();
}

void luminosity(float val) {
  theBlobDetection.setThreshold(val);
}

void controlEvent(ControlEvent theEvent) {

  if (theEvent.isGroup()) {
    String groupname = theEvent.group().name();
    if (groupname.equals("checkbox") == true) {
    //  webcam = (int)theEvent.group().arrayValue()[0] == 1;
      striped = (int)theEvent.group().arrayValue()[0] == 1;
      video = (int)theEvent.group().arrayValue()[1] == 1;
      blobs = (int)theEvent.group().arrayValue()[2] == 1;
      edges = (int)theEvent.group().arrayValue()[3] == 1;

    }
  }
}


// ==================================================
// captureEvent()
// ==================================================
void captureEvent(Capture cam)
{
  cam.read();
  newFrame = true;
}

void mousePressed()
{
  if (mouseButton == RIGHT) {
    if (controlP5.isVisible()) {
      controlP5.hide();
    } 
    else {
      controlP5.show();
    }
  }
}

