import java.util.*;
import java.text.*;

class GraphData {
  String incomingData[];
  String titles[];

  String tz;
  DateFormat df;

  ArrayList<Date> dates;
  ArrayList<HourData> hourdata;

  GraphData(String fileName) {
    df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss Z");
    tz = " +0000";
    dates = new ArrayList<Date>();
    hourdata = new ArrayList<HourData>();

    incomingData = loadStrings(fileName);
    establishData();
  } 

  ArrayList lineHeight(int dateIndex) {
    ArrayList<FloatList> pack = new ArrayList<FloatList>();
    FloatList anew_v_all = new FloatList();
    FloatList anew_v_ps4 = new FloatList();
    FloatList anew_v_xb1 = new FloatList();

    for (int i= 0; i < dateIndex+1; i++) {
      HourData hd = hourdata.get(i);
      // print(hd.anew_v_mu_all);
      anew_v_all.append(hd.anew_v_mu_all);
      anew_v_ps4.append(hd.anew_v_mu_ps4);
      anew_v_xb1.append(hd.anew_v_mu_xb1);
    }
    pack.add(anew_v_all);
    pack.add(anew_v_ps4);
    pack.add(anew_v_xb1);
        // println(pack);
    return pack;
  }



  FloatList provideBins(String type, int dateIndex) {
    HourData hd = hourdata.get(dateIndex);
    FloatList toReturn = hd.floatMap.get(type);
    return toReturn;
  }

  IntList provideCounts(String type, int dateIndex) {
    HourData hd = hourdata.get(dateIndex);
    IntList toReturn = hd.intMap.get(type);
    return toReturn;
  }

  Date getDate(int dateIndex) {
    return dates.get(dateIndex);
  }

  void establishData() {
    // What am I going to do with the titles?
    titles = split(incomingData[0], '\t');
    for (int i = 0; i < titles.length; i++) {
      titles[i] = titles[i].trim();
    }

    for (int i = 1; i < incomingData.length; i++) {
      // Set up the HourData objects

      // Split the row into string components
      String[] row = split(incomingData[i], '\t');

      // Create the date and initialize the 
      String datestr = row[0] + tz;
      datestr = datestr.trim();
      HourData hd;
      Date d = new Date();
      DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss Z");
      try {
        d = df.parse(datestr);
      } 
      catch (Exception e) {
        println("Unable to parse date stamp:" + e);
      }

      hd = new HourData(d);
      dates.add(d);
      hourdata.add(hd);

      // Populate the int and float variables
      hd.count_AFINN   = int(row[1]);
      hd.count_ANEW    = int(row[2]);
      hd.afinn_mu_all  = float(row[3]);
      hd.afinn_mu_ps4  = float(row[4]);
      hd.afinn_mu_xb1  = float(row[5]);
      hd.afinn_sd_all  = float(row[6]);
      hd.afinn_sd_ps4  = float(row[7]);
      hd.afinn_sd_xb1  = float(row[8]);
      hd.anew_v_mu_all = float(row[9]);
      hd.anew_v_mu_ps4 = float(row[10]);
      hd.anew_v_mu_xb1 = float(row[11]);
      hd.anew_v_sd_all = float(row[12]);
      hd.anew_v_sd_ps4 = float(row[13]);
      hd.anew_v_sd_xb1 = float(row[14]);
      hd.anew_a_mu_all = float(row[15]);
      hd.anew_a_mu_ps4 = float(row[16]);
      hd.anew_a_mu_xb1 = float(row[17]);
      hd.anew_a_sd_all = float(row[18]);
      hd.anew_a_sd_ps4 = float(row[19]);
      hd.anew_a_sd_xb1 = float(row[20]);
      hd.anew_d_mu_all = float(row[21]);
      hd.anew_d_mu_ps4 = float(row[22]);
      hd.anew_d_mu_xb1 = float(row[23]);
      hd.anew_d_sd_all = float(row[24]);
      hd.anew_d_sd_ps4 = float(row[25]);
      hd.anew_d_sd_xb1 = float(row[26]);

      hd.afinn_all_bins = floatListFromRow(row[27]);
      hd.afinn_ps4_bins = floatListFromRow(row[28]);
      hd.afinn_xb1_bins = floatListFromRow(row[29]);

      hd.afinn_all_counts = intListFromRow(row[30]);
      hd.afinn_ps4_counts = intListFromRow(row[31]);
      hd.afinn_xb1_counts = intListFromRow(row[32]);

      hd.anew_v_all_bins  = floatListFromRow(row[33]);
      hd.anew_a_all_bins  = floatListFromRow(row[36]);
      hd.anew_d_all_bins  = floatListFromRow(row[39]);
      hd.anew_v_ps4_bins  = floatListFromRow(row[34]);
      hd.anew_a_ps4_bins  = floatListFromRow(row[37]);
      hd.anew_d_ps4_bins  = floatListFromRow(row[40]);
      hd.anew_v_xb1_bins  = floatListFromRow(row[35]);
      hd.anew_a_xb1_bins  = floatListFromRow(row[38]);
      hd.anew_d_xb1_bins  = floatListFromRow(row[41]);

      hd.anew_v_all_counts  = intListFromRow(row[42]);
      hd.anew_a_all_counts  = intListFromRow(row[45]);
      hd.anew_d_all_counts  = intListFromRow(row[48]);
      hd.anew_v_ps4_counts  = intListFromRow(row[43]);
      hd.anew_a_ps4_counts  = intListFromRow(row[46]);
      hd.anew_d_ps4_counts  = intListFromRow(row[49]);
      hd.anew_v_xb1_counts  = intListFromRow(row[44]);
      hd.anew_a_xb1_counts  = intListFromRow(row[47]);
      hd.anew_d_xb1_counts  = intListFromRow(row[50]);

      hd.initMaps();
    }
    // Testing dates
    // HourData test = hourdata.get(0);
    // println(test.floatMap);
    // println(test.afinn_xb1_counts);
  }

  FloatList floatListFromRow(String rowData) {
    float[] l = float(split(rowData, ','));
    FloatList fl = new FloatList();
    for (int j=0; j < l.length; j++) {
      fl.append(l[j]);
    }
    return fl;
  }

  IntList intListFromRow(String rowData) {
    int[] l = int(split(rowData, ','));
    IntList il = new IntList();
    for (int j=0; j < l.length; j++) {
      il.append(l[j]);
    }
    return il;
  }
}

