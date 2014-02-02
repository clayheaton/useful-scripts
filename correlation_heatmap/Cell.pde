class Cell {
  float x, y;
  float w, h;
  float value;
  String term1, term2;

  // Cell Constructor
  Cell(float tempX, float tempY, float tempW, float tempH, float tempValue, String tempTerm1, String tempTerm2) {
    x = tempX;
    y = tempY;
    w = tempW;
    h = tempH;
    value = tempValue;
    term1 = tempTerm1;
    term2 = tempTerm2;
  } 

  void display() {

    if (mouseOver()) {
      // titleFont is global
      textFont(titleFont); 
      String s = term1 + " x " + term2 + ": " + value;
      fill(0);
      textAlign(CENTER);
      text(s, -offset + globalDim/2, -offset + globalDim - 40);
      strokeWeight(2);
      stroke(0);
    } else {
     noStroke(); 
    }

    color c;
    if (value == 1.0f) {
      c = color(255);
    } 
    else if (value < 0) {
      float a = map(abs(value), 0, abs(minValue), 30, 255);
      c = color(0, 0, 255, a); //255 * abs(value) * 30);
    } 
    else {
      float a = map(value, 0, maxValue, 30, 255);
      c = color(255, 0, 0, a);
    }

    fill(c);
    rect(x, y, w, h);
  }

  boolean mouseOver() {
    // Bad form to use the global offset variable here, but I'm too tired to change it.
    if (mouseX < x + offset + w && mouseX > x + offset && mouseY < y + offset + h && mouseY > y + offset) {
      return true;
    }
    return false;
  }
}

