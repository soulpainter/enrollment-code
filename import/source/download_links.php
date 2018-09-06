<?php

$years = ['2017-18','2016-17','2015-16','2014-15','2013-14',
                   '2012-13','2011-12','2010-11','2009-10','2008-09','2007-08',
                   '0607','0506','0405','0304','0203','0102','0001','9900',
                   '9899','9798','9697','9596','9495','9394',
                  ];

$download_url = "http://dq.cde.ca.gov/dataquest/dlfile/dlfile.aspx?cLevel=School&cYear=__DOWNLOAD__&cCat=Enrollment&cPage=filesenr.asp";

foreach ($years as $year) {
	$url = preg_replace("/__DOWNLOAD__/",$year,$download_url);
	print "$url\n";
	$cmd = "wget -O \"data/$year.txt\" \"$url\"";
	shell_exec($cmd);
}

