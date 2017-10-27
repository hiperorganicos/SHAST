void controlEvent(ControlEvent theEvent) {
  if (theEvent.isGroup()) {
    String groupname = theEvent.group().getName();
    if (groupname.equals("checkbox") == true) {
      blobs = (int)theEvent.group().getArrayValue()[2] == 1;
      edges = (int)theEvent.group().getArrayValue()[3] == 1;
    }
  }
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

