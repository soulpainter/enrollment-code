<html>
<body>
<script>
function submit_by_county(county) {
  if(document.getElementById("district_id"))
  {
    document.getElementById("district_id").value = '';
  }

  if(document.getElementById("school_id"))
  {
    document.getElementById("school_id").value = '';
  }

  document.getElementById("enrollment").submit(); //form submission
}

function submit_by_district(district) {
  if(document.getElementById("school_id"))
  {
    document.getElementById("school_id").value = '';
  }

  document.getElementById("enrollment").submit(); //form submission
}

</script>

<?php

require_once('db.php');

$county_id = isset($_GET['county_id']) ? $_GET['county_id'] : false;
$district_id = isset($_GET['district_id']) ? $_GET['district_id'] : false;
$school_id = isset($_GET['school_id']) ? $_GET['school_id'] : false;

$sql = new DBSql();
$counties = $sql->getCounties();

print "<form id='enrollment' name='enrollment' method='get'>\n";
print "<select name='county_id' onchange=\"submit_by_county(this)\">\n";
print "<option>County</option>\n";
foreach($counties as $county)
{
  if($county[0] == $county_id)
  {
    $select = 'selected';
  }
  else
  {
    $select = '';
  }

  print "<option $select value='" . $county[0] . "'>" . $county[1] . "</option>\n";
}
print "</select>\n";

if($county_id)
{
  print "<select id='district_id' name='district_id' onchange=\"submit_by_district(this)\">\n";
  print "<option value=''>District</option>";
  $districts = $sql->getDistrictsByCounty($county_id);
  foreach($districts as $district)
  {
    if($district[0] == $district_id)
    {
      $select = 'selected';
    }
    else
    {
      $select = '';
    }

    print "<option $select value='" . $district[0] . "'>" . $district[1] . "</option>\n";
  }
  print "</select>\n";
}

if($district_id)
{
  print "<select id='school_id' name='school_id' onchange=\"this.form.submit()\">\n";
  print "<option value=''>School</option>";
  $schools = $sql->getSchoolsByDistrictId($district_id);
  $counts = $sql->getCountsByDistrict($district_id);
  foreach($schools as $school)
  {
    if($school[0] == $school_id)
    {
      $select = 'selected';
    }
    else
    {
      $select = '';
    }

    print "<option $select value='" . $school[0] . "'>" . $school[1] . "</option>\n";
  }
  print "</select>\n";
}

print "</form><p>\n";

if($school_id)
{
  $data = $sql->getSchoolDataBySchoolId($school_id);
  $column_names = array_keys($data[0]);
  print "<table cellpadding=5 cellspacing=0 border=1>\n";
  print "<tr><th>" . implode("<th>", $column_names) . "</tr>\n";

  foreach($data as $row)
  {
    print "<tr><td>";
    print implode('<td>', $row);
    print "</tr>\n";

  }
}

?>

</body>
