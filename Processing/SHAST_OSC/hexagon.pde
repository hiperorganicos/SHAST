void hexagon( float cx, float cy, float r){
  int n = 6; // Numero de lados
  float angle = 360.0 / n;

  beginShape();
  for (int i = 0; i < n; i++){
    vertex(cx + r * cos(radians(angle * i)),
      cy + r * sin(radians(angle * i)));
  }
  endShape(CLOSE);
}
