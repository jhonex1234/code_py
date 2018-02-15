<?php
header('Content-Type: application/json');
$answer = shell_exec("python3.4 main_modulo.py " . escapeshellarg(json_encode($_GET)));
$json = json_decode($answer, true);
echo json_encode($json);
?>
