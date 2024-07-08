<?php
    $db_host = "mysql";
    $db_name = "mysql_time_based";
    $db_user = "root";
    $db_password = "root";
    $dsn = "mysql:host=$db_host;dbname=$db_name;charset=utf8mb4";
    
    try {
        $db = new PDO($dsn, $db_user, $db_password, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
        $db->query("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;");
    } catch (PDOException $e) {
        die('Connection failed: ' . $e->getMessage());
    }
?>
