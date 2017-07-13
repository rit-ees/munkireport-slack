<?php
header('Content-Type: application/json');
/*
 * This, in combination with the mr_api.py script is used for a Slack
 * slash command.
 */

$client_url = 'https://example.com/munkireport/clients/detail';

// if you need to fudge some data for testing use the following,
// replacing the comma separated data fields and hostname
$post = (isset($_POST['command'])) ? $_POST : array('command'=>'mr','text'=>'munkireport.manifestname,warranty.status hostname');
$command = $post['command'];
$input   = explode(' ', $post['text'], 2);
$arg     = $input[0];
$input   = (count($input>1)) ? $input[1] : '';

function get_data($input, $arg)
{
    if(isset($input)) {
       $d = json_decode(shell_exec('python mr_api.py -q '.$input.' -m '.$arg), true);
    }
    else {
        $d = json_decode(shell_exec('python mr_api.py -q '.$arg), true);
    }
    return $d[0];
}

$mr_data = get_data($input, $arg);
if (isset($mr_data)) {
    foreach ($mr_data as $k => $v) {
        if ($k == 'reportdata.timestamp') {
            $v = date('Y-m-d H:i', $v);
        }
        if ($k != 'machine.hostname' && $k != 'machine.serial_number') {
            $fields[] = array(
                'title' => $k,
                'value' => $v,
                'short' => true
            );
        }
    }
    echo json_encode(array(
        'response_type' => 'in_channel',
        'text'          => '',
        'attachments'   => array(array(
            'fallback'    => 'MunkiReport info',
            'author_name' => $mr_data['machine.hostname'],
            'author_link' => $client_url.'/'.$mr_data['machine.serial_number'],
            'fields'   => $fields
        ))
    ),JSON_UNESCAPED_SLASHES);
}
else {
    echo json_encode(array(
        'response_type' => 'in_channel',
        'text'          => 'no results',
    ),JSON_UNESCAPED_SLASHES);
}
?>
