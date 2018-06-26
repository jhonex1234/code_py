<?php
header('Content-Type: application/json');
$target_file = str_replace(" ", "_", "uploads/" . basename($_FILES["archivo"]["name"]));
$result = array();
if (move_uploaded_file($_FILES["archivo"]["tmp_name"], $target_file)) {	
	$result["name"] = basename($_FILES["archivo"]["name"]);
} else {
	$result["error"] = $_FILES["archivo"]["error"];    
}

echo json_encode($result);
?>

