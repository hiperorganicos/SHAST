class Abelha{
  
  int x;
  int y;
  int z; // profundidade
  
  Abelha(){
    setX(int(random(0, TELA_X)));
    setY(int(random(0, TELA_Y)));
    setZ(int(random(-5, 10)));
  }
  
  Abelha(int x, int y){
    this.setX(x);
    this.setY(y);
  }
  
  int getX(){
    return x;
  }
  
  int getY(){
    return y;
  }
  
  int getZ(){
    return z;
  }
  
  void setX(int x){
    // Testa se esta fora da tela
    if(x < TELA_X && x > 0)
      this.x = x;
  }
  
  void setY(int y){
    if(y < TELA_Y && y > 0)
      this.y = y;
  }
  
  void setZ(int z){
    if(z < altura_abelha && z > 0)
      this.z = z; 
  }
  
  void move_aleatoriamente(){
    this.setZ(this.getZ() + int(random(-1, 1)));
    if(getX() > (TELA_X*5)/4 || getY() > (TELA_Y*5)/6){
      this.setX(this.getX() + int(random(-5, 3)));
      this.setY(this.getY() + int(random(-5, 3)));
    } else if(getX() < TELA_X/6 || getY() < TELA_Y/6){      
      this.setX(this.getX() + int(random(-3, 5)));
      this.setY(this.getY() + int(random(-3, 5)));      
    } else {      
      this.setX(this.getX() + int(random(-6, 6)));
      this.setY(this.getY() + int(random(-6, 6)));
    }
  }
  
}
