<?php
    function fetch_account() {
        include "db_connect.php";
        $sql = "SELECT `id`, `user`, `password` FROM `account`";
        return $db->query($sql);
    }
    function fetch_post($user) {
        include "db_connect.php";
        $sql = "SELECT `id`, `user`, `password` FROM `account` where user='$user'";
        return $db->query($sql);
    }
?>