<?php

//
// upload_results.php
//
// Take input from the uploader form and return results to the user
//


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
$lookup_contest = $filter->clean($_GET["contest"], 'base64');
$lookup_year = $filter->clean($_GET["year"], 'int');
$debug = $filter->clean($_GET["debug"], 'int');
$raw = $filter->clean($_GET["raw"], 'int');
$lookup_form = $lookup_contest . "_upload";

if(!isset($raw)){ $raw = 0; }

if($debug > 0){
	echo "GET contents";
	echo "<pre>";
	print_r($_GET);
	echo "</pre>";
}

if($debug > 0){
	echo "SERVER contents";
	echo "<pre>";
	print_r($_SERVER);
	echo "</pre>";
}

// Use callsign to look up most recent record ID for the subsequent queries
$db = JFactory::getDbo();
$query = $db->getQuery(true);
$query
	->select($db->quoteName(array('id')))
	->from($db->quoteName('#__facileforms_records'))
	->where($db->quoteName('name') . ' LIKE ' . $db->quote($lookup_form))
	->order($db->quoteName('id') . ' ASC');

$db->setQuery($query);
$record_ids = $db->loadColumn();

if($debug > 0){
	echo "Listing of Record IDs";
	echo "<pre>";
	print_r($record_ids);
	echo "</pre>";
}

$columns = $db->getTableColumns('#__facileforms_subrecords');
if($debug > 0){
	echo "Subrecord Table Columns";
	echo "<pre>";
	print_r($columns);
	echo "</pre>";
}

$header = array('id','name','callsign','email','070number','powerlevel','contest_name','year','adif_file');
if($lookup_contest == 'vdsprint'){
    array_push($header, 'om_yl', 'block_start_time');
}
if($lookup_contest == 'thirtyone'){
    array_push($header, 'block_start_time');
}
if($lookup_contest == 'firecracker'){
    array_push($header, 'block_start_time');
}
if($lookup_contest == 'jayhudak'){
    array_push($header, 'block_start_time');
}
if($lookup_contest == 'greatpumpkin'){
    array_push($header, 'block_start_time');
}
$header_csv = implode(",", $header);
$header_csv_nl = $header_csv . "\n";

if($raw == 0) {echo "<pre>";}
echo "$header_csv_nl";

// For each id, build a summary line
foreach($record_ids as $record_id){
	$query = $db->getQuery(true);
	$query
		->select($db->quoteName(array('*')))
		->from($db->quoteName('#__facileforms_subrecords'))
		->where($db->quoteName('record') . ' LIKE ' . $db->quote($record_id));
	$db->setQuery($query);
	$subrecord_results = $db->loadAssocList('name');
	if($debug > 1){
		echo "Subrecord results";
		echo "<pre>";
		print_r($subrecord_results);
		echo "</pre>";
	}

	//
	// build the record output based on the header fields defined earlier
	//
    if($subrecord_results['year']['value'] == $lookup_year){
        $record = array($record_id);
        foreach($header as $key){
            if($key != 'id'){
                array_push($record, $subrecord_results[$key]['value']);
            }
        }

        $record_csv = implode(",", $record);
        $record_csv_nl = $record_csv . "\n";
        echo "$record_csv_nl";
    }
}
if($raw == 0) {echo "</pre>";}
