<?php
require_once("lib.php");

$school_lookup = [];

$schools = file('schools.csv');
foreach($schools as $school) {
  $bits = explode(',',trim($school));
  $school_lookup[$bits[0]] = $bits[1];
}

function generateCountyDistrictSchoolList($year,$filename) {
  global $format_years, $ethnic_2013, $ethnic_2008;

  $lookup = [];

  $contents = file($filename);

  $headers = $contents[0];
  unset($contents[0]);
  $header_fields = explode("\t",$headers);
  $data_headers = array_map('trim', array_slice($header_fields,3));

  $data = array();

  if($format_years[$year] == '2008') {
    foreach ($contents as $line) {
      $line = trim($line);
      $bits = explode("\t",$line);

      $cds_code = $bits[0];

      $data = array_slice($bits,3);

      if(isset($data_results[$cds_code][$year]))
      {
        $sum_data = array_map(function (...$arrays)
        {
          return array_sum($arrays);
        }, array_values($data_results[$cds_code][$year]), $data);

        $combined_data = array_combine($data_headers, $sum_data);
        $data_results[$cds_code][$year] = $combined_data;
      }
      else
      {
        $combined_data = array_combine($data_headers, $data);
        $data_results[$cds_code][$year] = $combined_data;
      }
    }
  }
  return array('lookup'=>$lookup, 'data_results'=>$data_results);
}

$all_data = [];
foreach ($years as $year=>$filename) {
	$fullname = 'source/data/' . $filename . '.txt';
	$all_data[$year] = generateCountyDistrictSchoolList($year,$fullname);
}

foreach ($all_data as $year=>$data)
{
  if(!isset($data['data_results'])) { continue; }

  foreach ($data['data_results'] as $cds_code=>$year_counts) {
    if(isset($school_lookup[$cds_code])) {
      $school_id = $school_lookup[$cds_code];
      foreach ($year_counts as $year_of_counts=>$counts) {
        print "INSERT INTO SchoolGradeCounts (" . join(',',array_map('strtolower',array_keys($counts))) . ",school_id,year) VALUES (" . join(',',array_values($counts)) . ",$school_id,$year_of_counts);\n";
       }
    }
  }
}

