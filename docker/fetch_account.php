<?php
    function fetch_account() {
        include "db_connect.php";
        $sql = "SELECT `id`, `user`, `password` FROM `account`";
        return $db->query($sql);
    }
    function fetch_user($user) {
        include "db_connect.php";
        $sql = "SELECT `id`, `user`, `password` FROM `account` where user='$user'";
        return $db->query($sql);
    }
    function fetch_id($id) {
        include "db_connect.php";
        $sql = "SELECT `id`, `user`, `password` FROM `account` where id=$id";
        return $db->query($sql);
    }
?>
