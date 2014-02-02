/* 

correlation_heatmap
02 Feb 2014

This is an example of how to create
a simple interactive heatmap based
on a correlation matrix. The matrix
calculations were performed in 
python, using Pandas, and exported
as CSV.

*/


int globalDim  = 1000;
float scale    = 1.0;
float gridSize = globalDim * scale    * 0.9;
float offset   = globalDim - gridSize * 0.95;

String[] lines;
String[] labels;
float[][] numbers;

Cell[][] matrix;
float cellSize;

int   matrixFontSize = 11;
int   titleFontSize  = 36;
PFont matrixFont, titleFont;

float minValue = 0;
float maxValue = 0;

void setup() {
  lines = loadStrings("corr_test.csv");
  labels = split(lines[0], ',');

  for (int i = 0; i < labels.length; i++) {
    labels[i] = labels[i].trim();
  }

  numbers = new float[lines.length - 1][lines.length - 1];
  matrix  = new  Cell[lines.length - 1][lines.length - 1];

  // Create the array of numbers
  for (int i = 1; i < lines.length; i++) {
    float[] row = float(split(lines[i], ','));
    for (int j = 0; j < row.length; j++) {
      numbers[i-1][j] = row[j];
    }
  }

  // Set min and max
  for (int i = 0; i < numbers.length; i++) {
    if (min(numbers[i]) < minValue) { 
      minValue = min(numbers[i]);
    }
    for (int j = 0; j < numbers.length; j++) {
      if (numbers[i][j] == 1.0) {
        continue;
      } 
      else if (numbers[i][j] > maxValue) {
        maxValue = numbers[i][j];
      }
    }
  }

  println(minValue + ", " + maxValue);

  cellSize = (gridSize / labels.length) * 0.85;

  // Establish the cells
  for (int  i = 0; i < labels.length; i++) {
    for (int j = 0; j < labels.length; j++) {
      Cell c = new Cell(j*cellSize, i*cellSize, cellSize, cellSize, numbers[j][i], labels[j], labels[i]);
      matrix[j][i] = c;
    }
  }

  size(int(globalDim*scale), int(globalDim*scale));

  // Set up the fonts
  matrixFont = createFont("Arial", matrixFontSize, true);
  titleFont  = createFont("Arial", titleFontSize, true);
}

void draw() {
  background(255);
  pushMatrix();
  translate(offset, offset);
  fill(0);
  // Draw the cells
  for (int i = 0; i < matrix.length; i++) {
    for (int j = 0; j < matrix.length; j++) {
      matrix[j][i].display();
    }
  }
  // Draw the vertical labels
  textFont(matrixFont);
  fill(0);
  textAlign(RIGHT);

  for (int i = 0; i < labels.length; i++) {
    float dist = ((i+0.5) * cellSize) + matrixFontSize/2.5;
    text(labels[i], -3, dist);
  }


  // Draw the horizontal labels
  rotate(-radians(90));
  textAlign(LEFT);

  for (int i = 0; i < labels.length; i++) {
    float dist = ((i+0.5) * cellSize) + matrixFontSize/2.5;
    text(labels[i], 3, dist);
  }

  popMatrix();
}

