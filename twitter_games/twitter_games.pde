/*

twitter_games visualization
Processing v. 2.1.1
ccheaton@ncsu.edu

This script takes compiled Twitter data and presents the
ANEW sentiment analysis of it as a series of distribution 
charts. Each row of data represents an hour of time during
which the tweets were collected. For each of the diagrams,
you see the distribution of PS4, Xbox One, and overall tweet
sentiment.

The lines that cross in the center represents the average ANEW
Valence score for the Xbox One and PS4 tweets. Look for spikes
in that line to locate interesting points in the data where the 
sentiment values spiked away from the norm.

When looking through the various hours of tweets, look for 
multi-modal patters and odd spikes. These either represent times
of note in the release of the PS4 and Xbox One, or you can pick
out times with lots of positive or negative retweets.

If you notice an interesting point in the data, just press < or > 
to stop the flow of the sketch and to navigate to that point.
Given the original data, that provides a time point to investigate
in the raw tweets.

Raw Tweets
^^^^^^^^^^
https://drive.google.com/folderview?id=0Bzvk4in6r1jjTGprWWZvUGFfOTA&usp=sharing

PS4 Release date: 11/15/2013
XB1 Release date: 11/22/2013

Basic Function
^^^^^^^^^^^^^^
Press / after starting the sketch to start
the flow of the sketch/time.

Other Keys
^^^^
1: Decrease the rate of time
2: Increase the rate of time
>: Move forward by one hour
<: Move backward by one hour
/: Resume flow at 12 hours/second
Space: Pause / Unpause

AFINN Sentiment Dictionary
^^^^^^^^^^^^^^^^^^^^^^^^^^
http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010

ANEW Sentiment Dictionary
^^^^^^^^^^^^^^^^^^^^^^^^^
http://csea.phhp.ufl.edu/media/anewmessage.html

*/

import java.util.*;
import java.text.*;

GraphData data;
ArrayList<Graph> graphs;

int dateIndex, maxDateIndex;

PFont titleFont, graphFont, keyFont;

DateFormat showDate;

boolean paused = false;
boolean dateForward = false;

int fr = 12;

color c1,c2,c3,c4,c5;
IntList colors = new IntList();

void setup() {
  size(1024, 768);
  data = new GraphData("histogram_data_2.txt");
  graphs = new ArrayList();

  PVector p1 = new PVector(10, height - 10);
  PVector p2 = new PVector(width/2 + 5, height - 10);
  PVector p3 = new PVector(width/2 + 5, height / 2 + 10);
  PVector p4 = new PVector(10, height / 2 + 10);

  Graph g1 = new Graph(500, 300, p4, data, "ANEW Valence");
  Graph g2 = new Graph(500, 300, p3, data, "ANEW Arousal");
  Graph g3 = new Graph(500, 300, p1, data, "ANEW Dominance");
  Graph g4 = new Graph(500, 300, p2, data, "AFINN Sentiment");

  c1 = color(0, 0, 0, 40);
  c2 = color(100, 149, 237, 128);
  c3 = color(255, 0, 0, 128);
  
  c4 = color(100, 149, 237, 255);
  c5 = color(255, 0, 0, 128);
  
  colors.append(c4);
  colors.append(c5);

  g1.addSeries("anew_v_all", c1);
  g1.addSeries("anew_v_ps4", c2);
  g1.addSeries("anew_v_xb1", c3);

  g2.addSeries("anew_a_all", c1);
  g2.addSeries("anew_a_ps4", c2);
  g2.addSeries("anew_a_xb1", c3);

  g3.addSeries("anew_d_all", c1);
  g3.addSeries("anew_d_ps4", c2);
  g3.addSeries("anew_d_xb1", c3);

  g4.addSeries("afinn_all", c1);
  g4.addSeries("afinn_ps4", c2);
  g4.addSeries("afinn_xb1", c3);

  graphs.add(g1);
  graphs.add(g2);
  graphs.add(g3);
  graphs.add(g4);

  frameRate(fr);
  dateIndex = 0;

  maxDateIndex = data.dates.size() - 1;

  showDate = new SimpleDateFormat("MM/dd/yyyy HH:mm");
  
  // force the date to display in UTC, which is what the original timestamp was
  showDate.setTimeZone(TimeZone.getTimeZone("GMT"));
  
  titleFont = loadFont("Aharoni-Bold-30.vlw");
  graphFont = loadFont("Aharoni-Bold-22.vlw");
  keyFont   = loadFont("GillSansMT-Bold-18.vlw");
  
}

void draw() {
  frameRate(fr);
  background(255);
  String d = showDate.format(data.getDate(dateIndex));
  textFont(titleFont, 30);
  fill(0);
  textAlign(CENTER,TOP);
  text(d, width*0.5, 35);
  
  textAlign(CENTER,CENTER);
  text("Playstation 4 vs. Xbox One Twitter Sentiment Analysis",width * 0.5,20);
  textAlign(LEFT,CENTER);
  for (Graph graph : graphs) {
    graph.display(dateIndex);
  }
  
  // Key
  noStroke();
  fill(c2);
  textFont(keyFont);
  pushMatrix();
  translate(width/2 - 200,65);
  int base = 40;
  rect(base + 0,0,30,20);
  fill(0);
  text("PS 4",base + 32,10);
  fill(c3);
  rect(base + 80,0,30,20);
  fill(0);
  text("Xbox One",base + 112,10);
  fill(c1);
  rect(base + 210,0,30,20);
  fill(0);
  text("Overall",base + 242,10);
  popMatrix();
  
  // Draw the line
  ArrayList<FloatList> lh = data.lineHeight(dateIndex);
  float tMin = 9999;
  float tMax = -9999;
  for(int i=1; i<lh.size(); i++){
    if(lh.get(i).min() < tMin){
     tMin = lh.get(i).min(); 
    }
    if(lh.get(i).max() > tMax){
     tMax = lh.get(i).max(); 
    }
  }
  
  pushMatrix();
  translate(0,height*0.5 + 20);
  noSmooth();
  for(int i=1; i<lh.size(); i++){
    stroke(colors.get(i-1));
    strokeWeight(2);
    noFill();
    beginShape();
    for(int j=0; j<lh.get(i).size(); j++){
      float xPt = map(j+1,0,1300,0,width);
      float yPt = map(lh.get(i).get(j),3,9,-150,50);
      vertex(xPt,-yPt);
    }
    endShape();
  }
  smooth();
  popMatrix();
  
  
  
  if (dateForward) {
    dateIndex += 1;
  }

  if (dateIndex > maxDateIndex) {
    dateIndex = 0;
  }
}


boolean sketchFullScreen() {
  return true;
}


void mouseClicked() {
  dateIndex += 1;
  println("dateIndex:" + dateIndex);
}

void keyPressed() {
  // println("pressed " + int(key) + " " + keyCode);

  // Backward <
  if (key == 44) {
    dateForward = false;
    dateIndex -= 1;
    if (dateIndex < 0) {
      dateIndex = maxDateIndex;
    }
  }
  // Forwards >
  if (key == 46) {
    dateForward = false;
    dateIndex += 1;
    if (dateIndex > maxDateIndex) {
      dateIndex = 0;
    }
  }

  if (key == 47) {
    dateForward = true;
  }

  if (key == 49) {
    println("frameRate:" + fr);
    if (fr == 1) {
      return;
    }
    fr -= 1;
  }

  if (key == 50) {
    println("frameRate:" + fr);
    fr += 1;
  }

  // Spacebar
  if (key == 32) {
    if (paused == false) {
      paused = true;
      noLoop();
    } 
    else {
      paused = false;
      loop();
    }
  }
}

