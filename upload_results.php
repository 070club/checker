<?php

//
// upload_results.php
//
// Take input from the uploader form and return results to the user
//

// TODO: add contest name as a possible GET to allow direct selection of results
// TODO: exclude membership form in ID search
// TODO: change the "upload again" link to reflect the current contest

//
// Various calls to set up Joomla! access
//
// Initialize Joomla framework
const _JEXEC = 1;

// Load system defines
if (file_exists(dirname(__DIR__) . '/defines.php'))
{
	require_once dirname(__DIR__) . '/defines.php';
}
if (!defined('_JDEFINES'))
{
	define('JPATH_BASE', dirname(__DIR__));
	require_once JPATH_BASE . '/includes/defines.php';
}
// Get the framework.
require_once JPATH_LIBRARIES . '/import.legacy.php';
// Bootstrap the CMS libraries.
require_once JPATH_LIBRARIES . '/cms.php';

// load site CSS
$css = '/templates/protostar/css/template.css';


//
// Get and filter our GET form details
//
$filter = JFilterInput::getInstance();
$lookup_call = $filter->clean($_GET["call"], 'base64');
$debug = $filter->clean($_GET["debug"], 'int');
$id = $filter->clean($_GET["id"], 'int');
$adif = $filter->clean($_GET["adif"], 'int');
$scorer_url = $_SERVER["HTTP_REFERER"];

// Set our URL for re-uploading if we came from an upload form
if(isset($scorer_url)){
	$back_url = '<a href="' . $scorer_url . '">try uploading again</a>';
} else {
	$back_url = '<a href="http://www.podxs070.com">try uploading again</a>';
}

if($debug == 1){
	echo "GET contents";
	echo "<pre>";
	print_r($_GET);
	echo "</pre>";
}

if($debug == 1){
	echo "SERVER contents";
	echo "<pre>";
	print_r($_SERVER);
	echo "</pre>";
}

// Use callsign to look up most recent record ID for the subsequent queries
$db = JFactory::getDbo();
$query = $db->getQuery(true);
$query
	->select($db->quoteName(array('record')))
	->from($db->quoteName('#__facileforms_subrecords'))
	->where($db->quoteName('value') . ' LIKE ' . $db->quote($lookup_call))
	->where($db->quoteName('name') . ' LIKE ' . $db->quote('callsign'))
	->order($db->quoteName('record') . ' DESC');

$db->setQuery($query);
$record_ids = $db->loadColumn();

if($debug == 1){
	echo "Record IDs for callsign $lookup_call";
	echo "<pre>";
	print_r($record_ids);
	echo "</pre>";
}

// supplying specific record id overrides callsign lookup
if($id > 0){
	$record_id = $id;
} else {
	$record_id = $record_ids[0];
}

if($debug == 1){
	echo "Using Record ID";
	echo "<pre>";
	print_r($record_id);
	echo "</pre>";
}

if(! isset($record_id)){
	echo "Something went wrong.  Please check your ADIF file and $back_url.</br>";
	echo "If you continue to have issues, please contact webmaster@podxs070.com</br>";
	echo "and report the following: (No record found matching callsign $lookup_call)";
	exit;
}

// Get record
$query = $db->getQuery(true);
$query
	->select($db->quoteName(array('*')))
	->from($db->quoteName('#__facileforms_records'))
	->where($db->quoteName('id') . ' LIKE ' . $db->quote($record_id));
$db->setQuery($query);
$record_results = $db->loadObjectList();
if($debug == 1){
	echo "ff_record";
	echo "<pre>";
	print_r($record_results);
	echo "</pre>";
}

// Get subrecord (this is the meat we care about)
$query = $db->getQuery(true);
$query
	->select($db->quoteName(array('*')))
	->from($db->quoteName('#__facileforms_subrecords'))
	->where($db->quoteName('record') . ' LIKE ' . $db->quote($record_id));
$db->setQuery($query);
$subrecord_results = $db->loadObjectList();
if($debug == 1){
	echo "ff_subrecord";
	echo "<pre>";
	print_r($subrecord_results);
	echo "</pre>";
}


//
// write a summary file from the query
//
$header = array();
$record = array();
for( $i = 0; $i < count($subrecord_results); $i++) {
	array_push($header, $subrecord_results[$i]->name);
	array_push($record, $subrecord_results[$i]->value);
	if($subrecord_results[$i]->name == 'year'){
		$year = $subrecord_results[$i]->value;
	}
	if($subrecord_results[$i]->name == 'callsign'){
		$callsign = $subrecord_results[$i]->value;
	}
	if($subrecord_results[$i]->name == 'adif_file'){
		$adiffile = $subrecord_results[$i]->value;
	}
	if($subrecord_results[$i]->name == 'contest_name'){
		$contestname = $subrecord_results[$i]->value;
		$contest_script = $contestname . ".py ";
	}
}
$header_csv = implode(",", $header);
$header_csv_nl = $header_csv . "\n";
$record_csv = implode(",", $record);
$record_csv_nl = $record_csv . "\n";
$summary_content = $header_csv_nl . $record_csv_nl;

$summary = 'summaries/' . $record_id;

if (!$handle = fopen($summary, 'w')) {
	echo "Something went wrong.  Please check your ADIF file and $back_url.</br>";
	echo "If you continue to have issues, please contact webmaster@podxs070.com</br>";
	echo "and report the following: Cannot open file ($record_id)";
	fclose($handle);
	exit;
}
// Write $somecontent to our opened file.
if (fwrite($handle, $summary_content) === FALSE) {
	echo "Something went wrong.  Please check your ADIF file and $back_url.</br>";
	echo "If you continue to have issues, please contact webmaster@podxs070.com</br>";
	echo "and report the following: Cannot write file ($record_id)";
	fclose($handle);
	exit;
}


// 
// Build the command string and get the output
// 
$cmd_tail = " 2>&1";
$cmd_string = "python3 " . $contest_script . " --year " . $year . " --summary " . $summary . " --call " . $callsign . " --adif " . $adiffile . $cmd_tail;
//$cmd_string = "python3 " . $contest_script . " --year " . $year . " --summary " . $summary . " --call " . $callsign . " --adif-summary " . $cmd_tail;
$output=null;
$retval=null;
exec($cmd_string, $output, $retval);

if($debug == 1){
    // instead of just restating commandline, maybe run the command with a debug flag?
    echo "<h3>Command output results</h3>";
    $debug_cmd_string = "python3 " . $contest_script . " --debug --year " . $year . " --summary " . $summary . " --call " . $callsign . " --adif " . $adiffile . $cmd_tail;
    $debug_output=null;
    $debug_retval=null;
    exec($debug_cmd_string, $debug_output, $debug_retval);
    print_r($debug_cmd_string);
    print_r($debug_retval);
    echo "<pre>";
    for($i = 0; $i < count($debug_output); $i++) {
        print $debug_output[$i] . "</br>";
    }
    echo "</br>";
    echo "</pre>";
}


//
// Output Section
// 
echo "<head><title>Upload Results</title><link rel=\"stylesheet\" href=\"$css\">";

echo '<style>

	h1, h2, h3, h4, h5, h6, .site-title {
		font-family: \'Open Sans\', sans-serif;
	}
	body.site {
		border-top: 3px solid #0088cc;
		background-color: #f4f6f7;
	}
	a {
		color: #0088cc;
	}
	.nav-list > .active > a,
	.nav-list > .active > a:hover,
	.dropdown-menu li > a:hover,
	.dropdown-menu .active > a,
	.dropdown-menu .active > a:hover,
	.nav-pills > .active > a,
	.nav-pills > .active > a:hover,
	.btn-primary {
		background: #0088cc;
	}
	</style></head>';

echo '
<body class="site com_content view-featured no-layout no-task itemid-101 fluid">
<!-- Body -->
<div class="body" id="top">
<div class="container-fluid">
<!-- Header -->
<header class="header" role="banner">
	<div class="header-inner clearfix">
		<a class="brand pull-left" href="/">
			<span class="site-title" title="PODXS Ø7Ø Club">PODXS Ø7Ø Club</span>											</a>
		<div class="header-search pull-right">

		</div>
	</div>
</header>
<hr>';


switch ($contestname) {
  case "pskfest":
    $contestname = "PSKfest";
    $back_url = '<a href="https://www.podxs070.com/pskfest-uploader">try uploading again</a>';
    break;
  case "vdsprint":
    $contestname = "Valentines Sprint";
    $back_url = '<a href="https://www.podxs070.com/vd-sprint-uploader">try uploading again</a>';
    break;
  case "saintpat":
    $contestname = "Saint Patrick's";
	$back_url = '<a href="https://www.podxs070.com/saint-pats-uploader">try uploading again</a>';
    break;
  case "thirtyone":
    $contestname = "31 Flavors";
	$back_url = '<a href="https://www.podxs070.com/31-flavors-uploader">try uploading again</a>';
    break;
  case "tdw":
    $contestname = "Three Day Weekend";
    $back_url = '<a href="https://www.podxs070.com/tdw-uploader">try uploading again</a>';
    break;
  case "firecracker":
    $contestname = "40m Firecracker Sprint";
    $back_url = '<a href="https://www.podxs070.com/firecracker-uploader">try uploading again</a>';
    break;
  case "jayhudak":
    $contestname = "Jay Hudak Memorial 80m Sprint";
    $back_url = '<a href="https://www.podxs070.com/jay-hudak-uploader">try uploading again</a>';
    break;
  case "greatpumpkin":
    $contestname = "160m Great Pumpkin Sprint";
    $back_url = '<a href="https://www.podxs070.com/great-pumpkin-uploader">try uploading again</a>';
    break;
  case "tripleplay":
    $contestname = "Triple Play Low Band";
    $back_url = '<a href="https://www.podxs070.com/tripleplay-uploader">try uploading again</a>';
    break;
  case "doubleheader":
    $contestname = "Double Header";
    $back_url = '<a href="https://www.podxs070.com/doubleheader-uploader">try uploading again</a>';
    break;
  default:
    $contestname = $contestname;
}

echo "<h3>$contestname $year uploader results</h3>";
echo "if the results below don't look right, please check your adif file and $back_url.</br>";
echo "final scores will still be tallied after the submission period closes a week after the contest.</br></br>";
echo "if you have any questions about your results, please contact <a href=\"mailto:contests@podxs070.com\">contests@podxs070.com</a></br>";
if($retval == 0){
	echo "<pre>";
	for($i = 0; $i < count($output); $i++) {
		print $output[$i] . "</br>";
	}
	echo "</br>";
	echo "</pre>";
} else {
	echo "Something went wrong.  Please check your ADIF file and $back_url.</br>";
	echo "If you continue to have issues, please contact webmaster@podxs070.com</br>";
}

if($adif == 1){
	echo "<h4>ADIF Contents:</h4>";
	echo "<pre>";
	//echo htmlspecialchars(file_get_contents($adiffile));
	$adif_lines=file($adiffile);
	foreach($adif_lines as $line) { echo htmlspecialchars($line); }
	echo "</pre>";
}

echo '<!-- Footer -->
<footer class="footer" role="contentinfo">
	<div class="container-fluid">
		<hr>

		<p class="pull-right">
			<a href="#top" id="back-top">
				Back to Top				</a>
		</p>
		<p>
			© 2021 PODXS Ø7Ø Club			</p>
	</div>
</footer>';

echo '</div></body>';
