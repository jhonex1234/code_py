<?php
header('Content-Type: application/json');
$answer = shell_exec("python3.4 ai_agent.py " . escapeshellarg(json_encode($_GET)));
$json = json_decode($answer, true);
echo json_encode($json);
?>
