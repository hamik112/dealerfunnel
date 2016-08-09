<?php
$servername = '161.47.5.163';
$username = "xcel";
$password = "GZaSTXUY3ZK2XKPE";

// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully";
?>

