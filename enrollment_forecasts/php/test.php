<?php

$use = 3;
$max = 50;
#$max = 10000;
#$max = 1000000;

$startdate = date('m/d/Y h:i:s a', time());
#print "START: $startdate\n";

$count = 0;

for($i=1; $i<=$max; $i++)
{
  #print "$i\n";
  #$middate = date('m/d/Y h:i:s a', time());
  #print "MID: $middate\n";
  for($j=1; $j<=$max; $j++)
  {
    $middate = date('m/d/Y h:i:s a', time());
    #print "MID: $middate\n";
    for($k=1; $k<=$max; $k++)
    {
      print "php index.php -f$i -s$j -t$k >> log\n";
      #$result = shell_exec("php index.php -f$i -s$j -t$k");
      #print $result;
      #print "$i, $j, $k\n";
      $count++;
    }
  }
}

#print "COUNT: $count\n";

$enddate = date('m/d/Y h:i:s a', time());
#print "END: $enddate\n";
