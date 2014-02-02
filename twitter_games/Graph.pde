class Graph {
  int w, h;
  float minX, maxX, maxY;
  PVector position;

  ArrayList<FloatList> bins;
  ArrayList<IntList> counts;
  ArrayList<String> series;
  IntList colors;
  
  String title;

  GraphData data;

  Graph(int tempW, int tempH, PVector tempPos, GraphData tempData, String tempTitle) {
    w = tempW;
    h = tempH;
    position = tempPos;
    data = tempData;
    bins = new ArrayList<FloatList>();
    counts = new ArrayList<IntList>();
    series = new ArrayList<String>();
    colors = new IntList();
    title = tempTitle;
  }

  void addSeries(String str, color c) {
    series.add(str);
    colors.append(c);
  }

  void display(int dateIndex) {
    bins.clear();
    counts.clear();
    for (int i = 0; i < series.size(); i++) {
      bins.add(data.provideBins(series.get(i), dateIndex));
      counts.add(data.provideCounts(series.get(i), dateIndex));
    }

    pushMatrix();
    translate(position.x, position.y);
    drawAxes(); 
    drawCurves();
    drawTitle();
    drawBoxes();
    popMatrix();
  }
  
  void drawBoxes() {
    noStroke();
    fill(255);
    rect(0,1,w,30);
  }
  
  void drawTitle() {
   textFont(graphFont);
   fill(0);
   text(title,5,-h/2); 
  }

  void drawCurves() {
    maxY = 0;
    minX = 1000;
    maxX = -1000;
    
    // Find the max Y
    for (int i = 0; i < counts.size(); i++) {
      if(counts.get(i).max() > maxY){
       maxY = counts.get(i).max(); 
      }
    }
    
    // Find the min and Max X
    for (int i = 0; i < bins.size(); i++) {
      if(bins.get(i).max() > maxX){
       maxX = bins.get(i).max(); 
      }
      
      if(bins.get(i).min() < minX){
       minX = bins.get(i).min(); 
      }
    }

    
    for (int i = 0; i < bins.size(); i++) {
      FloatList yPts = new FloatList();
      FloatList xPts = new FloatList();

      // Map the x points to the new space
      for (int j = 0; j < bins.get(i).size(); j++) {
        float x = bins.get(i).get(j);
        float xn = map(x,minX,maxX,0,w);
        xPts.append(xn);
      }
      
      // Map the y points to the new space
      for (int j = 0; j < counts.get(i).size(); j++) {
        float y = (int)counts.get(i).get(j);
        float yn = map(y,0,maxY,0,h);
        yPts.append(yn);
      }
      
      // Draw the curves
      fill(colors.get(i));
      beginShape();
      // stroke(colors.get(i));
      // strokeWeight(2);
      noStroke();
      vertex(0,0);
      for(int j = 0; j < counts.get(i).size(); j++){
        curveVertex(xPts.get(j), -yPts.get(j));
        // ellipse(xPts.get(j), -yPts.get(j), 2, 2); 
      }
      vertex(w,0);
      vertex(0,0);
      // vertex(xPts.get(0), -yPts.get(0));
      endShape();
    }
  }

  void drawAxes() {
    stroke(128);
    strokeWeight(1);
    // line(0, 0, 0, -h);
    line(0, 0, w, 0);
  }
}

