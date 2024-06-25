<?php
    error_reporting(0);
    ini_set("session.cookie_httponly", 1);
    ini_set('display_errors', 1);
    session_start();
?>

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Time-Based-SQL-Injection</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

    <style>
        .center-form {
            display: flex;
            justify-content: center;
            height: 50vh;
        }
    </style>

  </head>
  <body>
    <div class="container">
      <div class="navbar navbar-default" role="navigation">
        <div class="container-fluid">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
          </div>
          <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
              <li class="active"><a href="/">Account</a></li>
          </div><!--/.nav-collapse -->
        </div><!--/.container-fluid -->
      </div><!-- /.navbar -->
      <!-- Main component for a primary marketing message or call to action -->


<?php
    include "fetch_account.php";
    $username = isset($_POST['Username']) ? $_POST['Username'] : '';
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
      if($username == ""){
           $result_post = fetch_account();
      }else{
           $result_post = fetch_post($username);
      }

    }
?>

      <div class="row center-form">
            <div class="col-md-4">
                <h3>Search Account</h3>
                <form action="/" method="POST">
                    <div class="form-group">
                        <label for="Username">Username:</label>
                        <input type="text" class="form-control" id="Username" name="Username">
                    </div>
                    <button type="Submit" class="btn btn-primary">Search</button>
                </form>
            </div>
        </div>

      <table class="table">
        <thead>
          <tr>
            <th>序  號</th>
            <th>使用者</th>
            <th>密  碼</th>  
          </tr>
        </thead>
        <tbody>
<?php

        foreach ($result_post->fetchAll() as $row) {
?>
          <tr>
            <th scope="row"><?= $row['id'] ?></th>
            <th scope="row"><?= $row['user'] ?></th>
            <th scope="row"><?= $row['password'] ?></th>
          </tr>
<?php
        }
?>
        </tbody>
      </table>
    </div> <!-- /container -->
    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>
