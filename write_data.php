<?php
// get the data from the POST message
$post_data = json_decode(file_get_contents('php://input'), true);
$data = $post_data['filedata'];
$fileName = $post_data['fileName'];
// the directory "data" must be writable by the server
$name = "data/{$fileName}.json"; 
// write the file to disk
file_put_contents($name, $data);
?>