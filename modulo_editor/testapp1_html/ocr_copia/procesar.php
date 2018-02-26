<?php
header('Content-Type: application/json');
$json = array();
$result = array();
$documento = "uploads/" . $_GET ["documento"];
$result = shell_exec("./ocr_process.sh {$documento} 2>&1");
$resultados = explode("\n", $result);
//echo ($result);
$fileout = $resultados[0] . ".txt";
$myfile = fopen($fileout, "r") or die("Unable to open file!");
fread($myfile, filesize($fileout));
fclose($myfile);
//echo($myfile);
$json["resultado"] = "exitoso";
//unlink('testocr.txt');
$json["error"] = "";
echo json_encode($json);
?>
