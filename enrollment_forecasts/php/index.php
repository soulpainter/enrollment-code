<?php

$grade_years = [
  'K' => ['13' => 270, '14' => 242, '15' => 260, '16' => 230, '17' => 266],
  '1' => ['13' => 221, '14' => 260, '15' => 224, '16' => 222, '17' => 212],
  '2' => ['13' => 289, '14' => 216, '15' => 261, '16' => 219, '17' => 224],
  '3' => ['13' => 259, '14' => 282, '15' => 214, '16' => 254, '17' => 224],
  '4' => ['13' => 276, '14' => 257, '15' => 286, '16' => 210, '17' => 278],
  '5' => ['13' => 272, '14' => 281, '15' => 264, '16' => 281, '17' => 216],
  '6' => ['13' => 243, '14' => 254, '15' => 266, '16' => 243, '17' => 265],
  '7' => ['13' => 236, '14' => 249, '15' => 262, '16' => 268, '17' => 256],
  '8' => ['13' => 187, '14' => 247, '15' => 255, '16' => 265, '17' => 272],
];
$projections = $grade_years;

$opts = getopt("f:s:t:");

if(!empty($opts))
{
  $weights = [$opts['t'], $opts['s'], $opts['f']]; 
}
elseif(!isset($_GET['first']) || !isset($_GET['second']) || !isset($_GET['third']))
{
  $weights = [1, 2, 3];
}
else
{
  $weights = [$_GET['third'], $_GET['second'], $_GET['first']];
}

$sum_weight = array_sum($weights);

$diffs = [];

foreach ($grade_years as $grade=>$year_data)
{
  if($grade == "K")
  {
    $k_diff_array = [];
    $calc_diff_data = array_reverse(array_values($year_data));
    foreach($calc_diff_data as $key=>$value)
    {
      if(array_key_exists($key+1, $calc_diff_data))
      {
        $diff = $value - $calc_diff_data[$key+1];
        array_unshift($k_diff_array, $diff);
      }
    }
    $diffs[$grade] = $k_diff_array;
  }
  else
  {
    if($grade == '1')
    {
      $diff_array = [];
      $k_arr = array_values($grade_years['K']);

      $calc_diff_data = array_values($year_data);
      #$diff = $year_data[$i] - $k_arr[$i-1];
      for($i=1; $i < count($calc_diff_data); $i++)
      {
        $diff = $calc_diff_data[$i] - $k_arr[$i-1];
        $diff_array[] = $diff;
      } 
      $diffs[$grade] = $diff_array;
    }
    else
    {
     #exit;

      $diff_array = [];
      $k_arr = array_values($grade_years[$grade-1]);

      $calc_diff_data = array_values($year_data);
      for($i=1; $i < count($calc_diff_data); $i++)
      {
        $diff = $calc_diff_data[$i] - $k_arr[$i-1];
        $diff_array[] = $diff;
      }
      $diffs[$grade] = $diff_array;
    }
  }
}

$grade_avgs = [];
foreach($diffs as $grade=>$values)
{
  $array_ct = count($values);
  $starting_key = $array_ct - 3;
  $slice = array_slice($values,$starting_key,3);

  $avg_sum = 0;
  foreach($slice as $knum=>$num)
  {
    $use_weight = $weights[$knum];
    $weight_value = $use_weight * $num;
    $avg_sum += $weight_value;
  }
  $avg = $avg_sum / $sum_weight;
  $grade_avgs[$grade] = $avg;
}

$tmp = array_keys($grade_years['K']);
$last_year = array_pop($tmp);
$next_year = $last_year + 1;
$run_len = 10;

$last_year_values = [];
foreach ($grade_years as $grade=>$year_data)
{
   $rev = array_values($year_data);
   $last_year_values[$grade] = array_pop($rev);
}

$value_matrix = [];

foreach($grade_avgs as $kavg=>$vavg)
{

if($kavg == 'K')
{
  for($i=1; $i<=$run_len; $i++)
  {
    $next_year_plus_avg = $last_year_values[$kavg] + $vavg * $i;
    $projections[$kavg][17 + $i] = $next_year_plus_avg;
  }
}
else
{
  if($kavg==1)
  {
      $k_arr = array_values($grade_years['K']);
      $last_k_value = array_pop($k_arr);

      for($i=1; $i<=$run_len; $i++)
      {
        if($i==1)
        {
          $next_year_plus_avg = $last_k_value + $vavg * $i;
          $projections[$kavg][17 + $i] = $next_year_plus_avg;
        }
        else
        {
          $calc_value = $projections['K'][17 + ($i - 1)];
          $projections[$kavg][17 + $i] = $calc_value + $vavg;
        }
      }
  }
  else
  {
      $k_arr = array_values($grade_years[$kavg-1]);
      $last_k_value = array_pop($k_arr);

      for($i=1; $i<=$run_len; $i++)
      {
        if($i==1)
        {
          $next_year_plus_avg = $last_k_value + $vavg * $i;
          $projections[$kavg][17 + $i] = $next_year_plus_avg;
        }
        else
        {
          $calc_value = $projections[$kavg-1][17 + ($i - 1)];
          $projections[$kavg][17 + $i] = $calc_value + $vavg;
        }
      }
  }
}

// end of foreach loop
}

$sums = ['78' => [], 'K6' => [], 'total' => []];
foreach ($projections as $grade=>$values)
{
  foreach($values as $year=>$number)
  {
    if(!isset($sums['K6'][$year]))
    {
      $sums['K6'][$year] = 0;
    }

    if(!isset($sums['78'][$year]))
    {
      $sums['78'][$year] = 0;
    }

    if($grade == 7 || $grade == 8)
    {
      $sums['78'][$year] += $number;
    }
    else
    {
      $sums['K6'][$year] += $number;
    }
  }
}

foreach($sums as $idx=>$years)
{
  foreach($years as $year=>$amount)
  {
    if(!isset($sums['total'][$year]))
    {
      $sums['total'][$year] = $amount;
    }
    else
    {
      $sums['total'][$year] += $amount;
    }
  }
}

$everything = [ 'weights' => $weights, 'data' => $projections, 'sums' => $sums, 'avg' => $grade_avgs, 'diffs' => $diffs ];
#print_r($everything);

$json = json_encode($everything);
print $json ."\n";
exit;

?>

<form method="get">
Most Recent Year: <input name="first" type="text" value="3" /><br>
Second Most Recent Year: <input name="second" type="text" value="2" /><br>
Third Most Recent Year: <input name="third" type="text" value="1" /><br>
<input type="submit" />
</form>
<pre>
<?php print_r($everything); ?>
</pre>


