<?php
header('Content-Type: application/json');
$namedoc = "/".$_GET["namedoc"];
$result = array();
$result = shell_exec("python3.4 main_modulo.py"+$namedoc+" 2>&1");
echo json_encode($result);
?>
