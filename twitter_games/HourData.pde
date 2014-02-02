class HourData {
  Date date;

  HashMap<String, FloatList> floatMap = new HashMap<String, FloatList>();
  HashMap<String, IntList> intMap = new HashMap<String, IntList>();

  int count_AFINN, count_ANEW;

  float afinn_mu_all, afinn_mu_ps4, afinn_mu_xb1;
  float afinn_sd_all, afinn_sd_ps4, afinn_sd_xb1;

  FloatList afinn_all_bins;
  FloatList afinn_ps4_bins;
  FloatList afinn_xb1_bins;

  IntList afinn_all_counts;
  IntList afinn_ps4_counts;
  IntList afinn_xb1_counts;

  float anew_v_mu_all, anew_v_mu_ps4, anew_v_mu_xb1;
  float anew_v_sd_all, anew_v_sd_ps4, anew_v_sd_xb1;

  float anew_a_mu_all, anew_a_mu_ps4, anew_a_mu_xb1;
  float anew_a_sd_all, anew_a_sd_ps4, anew_a_sd_xb1;

  float anew_d_mu_all, anew_d_mu_ps4, anew_d_mu_xb1;
  float anew_d_sd_all, anew_d_sd_ps4, anew_d_sd_xb1;

  FloatList anew_v_all_bins;
  FloatList anew_a_all_bins;
  FloatList anew_d_all_bins;
  FloatList anew_v_ps4_bins;
  FloatList anew_a_ps4_bins;
  FloatList anew_d_ps4_bins;
  FloatList anew_v_xb1_bins;
  FloatList anew_a_xb1_bins;
  FloatList anew_d_xb1_bins;

  IntList anew_v_all_counts;
  IntList anew_a_all_counts;
  IntList anew_d_all_counts;
  IntList anew_v_ps4_counts;
  IntList anew_a_ps4_counts;
  IntList anew_d_ps4_counts;
  IntList anew_v_xb1_counts;
  IntList anew_a_xb1_counts;
  IntList anew_d_xb1_counts;

  HourData(Date d) {
    date = d;

    afinn_all_bins   = new FloatList();
    afinn_ps4_bins   = new FloatList();
    afinn_xb1_bins   = new FloatList();
    afinn_all_counts = new IntList();
    afinn_ps4_counts = new IntList();
    afinn_xb1_counts = new IntList();

    anew_v_all_bins  = new FloatList();
    anew_a_all_bins  = new FloatList();
    anew_d_all_bins  = new FloatList();
    anew_v_ps4_bins  = new FloatList();
    anew_a_ps4_bins  = new FloatList();
    anew_d_ps4_bins  = new FloatList();
    anew_v_xb1_bins  = new FloatList();
    anew_a_xb1_bins  = new FloatList();
    anew_d_xb1_bins  = new FloatList();

    anew_v_all_counts = new IntList();
    anew_a_all_counts = new IntList();
    anew_d_all_counts = new IntList();
    anew_v_ps4_counts = new IntList();
    anew_a_ps4_counts = new IntList();
    anew_d_ps4_counts = new IntList();
    anew_v_xb1_counts = new IntList();
    anew_a_xb1_counts = new IntList();
    anew_d_xb1_counts = new IntList();

    initMaps();
  }

  void initMaps() {
    floatMap.put("afinn_all", afinn_all_bins);
    floatMap.put("afinn_ps4", afinn_ps4_bins);
    floatMap.put("afinn_xb1", afinn_xb1_bins);
    floatMap.put("anew_v_all", anew_v_all_bins);
    floatMap.put("anew_a_all", anew_a_all_bins);
    floatMap.put("anew_d_all", anew_d_all_bins);
    floatMap.put("anew_v_ps4", anew_v_ps4_bins);
    floatMap.put("anew_a_ps4", anew_a_ps4_bins);
    floatMap.put("anew_d_ps4", anew_d_ps4_bins);
    floatMap.put("anew_v_xb1", anew_v_xb1_bins);
    floatMap.put("anew_a_xb1", anew_a_xb1_bins);
    floatMap.put("anew_d_xb1", anew_d_xb1_bins);

    intMap.put("afinn_all", afinn_all_counts);
    intMap.put("afinn_ps4", afinn_ps4_counts);
    intMap.put("afinn_xb1", afinn_xb1_counts);
    intMap.put("anew_v_all", anew_v_all_counts);
    intMap.put("anew_a_all", anew_a_all_counts);
    intMap.put("anew_d_all", anew_d_all_counts);
    intMap.put("anew_v_ps4", anew_v_ps4_counts);
    intMap.put("anew_a_ps4", anew_a_ps4_counts);
    intMap.put("anew_d_ps4", anew_d_ps4_counts);
    intMap.put("anew_v_xb1", anew_v_xb1_counts);
    intMap.put("anew_a_xb1", anew_a_xb1_counts);
    intMap.put("anew_d_xb1", anew_d_xb1_counts);
  }
}

