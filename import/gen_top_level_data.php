<?php
require_once("lib.php");

function generateCountyDistrictSchoolList($year,$filename) {
  global $format_years, $ethnic_2013, $ethnic_2008;

  $lookup = [];

  $contents = file($filename);

  $headers = $contents[0];
  unset($contents[0]);
  $header_fields = explode("\t",$headers);
  $data_headers = array_map('trim', array_slice($header_fields,6));

  $data = array();

  if ($format_years[$year] == '2013') {
    foreach ($contents as $line) {
      $line = trim($line);
      $bits = explode("\t",$line);

      $cds_code = $bits[0];
      $county = $bits[1];
      $district = $bits[2];
      $school = $bits[3];

#      if($district == 'Ross Valley Elementary')
#      {

      $data = array_slice($bits,6);
      #print_r($data);
      
      if(isset($data_results[$cds_code][$year]))
      {
        #print "SEEN BEFORE\n";
        #print_r(array_values($data_results[$cds_code][$year]));
        #print_r($data);
        $sum_data = array_map(function (...$arrays) 
        {
          return array_sum($arrays);
        }, array_values($data_results[$cds_code][$year]), $data);

        $combined_data = array_combine($data_headers, $sum_data);
        $data_results[$cds_code][$year] = $combined_data;
        #exit;
      }
      else
      {
        #print "FIRST TIME\n";
        $combined_data = array_combine($data_headers, $data);
        $data_results[$cds_code][$year] = $combined_data;
      }
      $lookup[$county][$district][$cds_code] = $school;


#      }
    }
  }
  #print_r($data_results); exit;
  return array('lookup'=>$lookup, 'data_results'=>$data_results);;
}

$all_data = array();
foreach ($years as $year=>$filename) {
	$fullname = 'source/data/' . $filename . '.txt';
	$all_data[$year] = generateCountyDistrictSchoolList($year,$fullname);
}

$base_data = [];
foreach ($all_data as $year=>$data)
{
  foreach($data['lookup'] as $county=>$district_data)
  {
    foreach($district_data as $district=>$school_data)
    {
      foreach($school_data as $cds_code=>$school)
      {
        $base_data[strtolower($county)][strtolower($district)][$cds_code]['school'] = strtolower($school);
        $base_data[strtolower($county)][strtolower($district)][$cds_code]['stats'][$year] = $data['data_results'][$cds_code][$year];
      }
    }
  }
}

print "TRUNCATE Counties;\n";
print "TRUNCATE Districts;\n";
print "TRUNCATE Schools;\n";
print "TRUNCATE SchoolGradeCounts;\n";

foreach($base_data as $county=>$district_data)
{
  print "INSERT INTO Counties (name) VALUES ('" .ucwords(addslashes($county)) ."');\n";
  print "SET @last_id_in_county = LAST_INSERT_ID();\n";
  foreach($district_data as $district=>$schools)
  {
    print "INSERT INTO Districts (name, county_id) VALUES ('" . ucwords(addslashes($district)) . "',@last_id_in_county);\n";
    print "SET @last_id_in_district = LAST_INSERT_ID();\n";
    foreach($schools as $cds_code=>$school_data)
    {
      print "INSERT INTO Schools (name, cds_code, district_id) VALUES ('" . ucwords(addslashes($school_data['school'])) . "','" . $cds_code . "',@last_id_in_district);\n";
      print "SET @last_id_in_school = LAST_INSERT_ID();\n";
      foreach($school_data['stats'] as $year=>$counts)
      {
        print "INSERT INTO SchoolGradeCounts (" . join(',',array_map('strtolower',array_keys($counts))) . ",school_id,year) VALUES (" . join(',',array_values($counts)) . ",@last_id_in_school,$year);\n";
      }
    }
  }
}

