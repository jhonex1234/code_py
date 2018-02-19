<?php
    $filename = $_GET['namedoc']; 
        /*header("Content-Type: application/octet-stream");*/
    header('Content-Type: application/json');
    header("Content-Type: application/force-download");
    header("Content-Disposition: attachment; filename=\"$filename\"");
    echo $filename;
?>

