<?php
// Set headers for JSON response and CORS
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');

// Create response array
$response = array(
    'unix_timestamp' => time(),
    'status' => 'success'
);

// Convert array to JSON and output
echo json_encode($response);
?> 