// ==================================================
// drawBlobsAndEdges()
// ==================================================
void drawShapes(boolean drawBlobs, boolean drawEdges){
  
  noFill();
  
  for (int i = 0 ; i < n_abelhas; i++){
      // Edges
      strokeWeight(3);
      stroke(0, 255, 0);

      int k = 0;
      int max = 5000;

      hexStr = random(0, 4);
      
      if (drawEdges){
         noFill(); 
         strokeWeight(hexStr);
         stroke(255, 225, 0, 255);            
         hexagon(abelha[i].getX(), abelha[i].getY(), (altura_abelha - abelha[i].getZ()));         
         hexagon(abelha[i].getX(), abelha[i].getY(), (altura_abelha - abelha[i].getZ())/3);
      }
      
      if (drawBlobs){
        noStroke();
        fill(255, 190, 0, 255);
        hexagon(abelha[i].getX(), abelha[i].getY(), altura_abelha - abelha[i].getZ());
        
        stroke(0);
        strokeWeight(3);
        hexagon(abelha[i].getX(), abelha[i].getY(), (altura_abelha - abelha[i].getZ())*2/3);
      }
   }
}

