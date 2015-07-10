// ==================================================
// drawBlobsAndEdges()
// ==================================================
void drawShapes(boolean drawBlobs, boolean drawEdges)
{
  noFill();
  Blob b;
  EdgeVertex eA, eB;
  for (int n=0 ; n<theBlobDetection.getBlobNb() ; n++)
  {
    b=theBlobDetection.getBlob(n);
    if (b!=null)
    {
      // Edges

      strokeWeight(3);
      stroke(0, 255, 0);

      int k = 0;
      int max = 5000;

      float[][] mypoints = new float[max][2];


      for (int m=0;m<b.getEdgeNb();m+=skip_blobs)
      {
        hexStr = random(0, 4);
        eA = b.getEdgeVertexA(m);
        eB = b.getEdgeVertexB(m);
        if (eA !=null && eB !=null) {
          if (drawEdges)
          {
            //line(eA.x*width, eA.y*height,eB.x*width, eB.y*height);
             noFill(); 
             strokeWeight(hexStr);
             stroke(255, 225, 0, hexStr*55);            
             hexagon(eA.x*width, eA.y*height, 9);
            //ellipse(eB.x*width, eB.y*height, 10,10);
          }
          if (k<max) {
            mypoints[k][0] = eA.x*width;
            mypoints[k][1] = eA.y*height;
            k++;
          }
        }
      }

      
      // Blobs
      if (drawBlobs)
      {      
        noStroke();
        fill(255, 190, 0, (255/b.h)*3);
        hexagon(b.x*width, b.y*height, (b.h*height)/2);
        
        stroke(0);
        strokeWeight(3);
        hexagon(b.x*width, b.y*height, (b.h*height)/3);
      }
    }
  }
}

