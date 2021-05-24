<?php

define('BOT_USERNAME', 'inkestak_bot'); 

ini_set('display_errors', 1);
require_once __DIR__ . '/vendor/autoload.php';
function getTelegramUserData() {
  if (isset($_COOKIE['tg_user'])) {
    $auth_data_json = urldecode($_COOKIE['tg_user']);
    $auth_data = json_decode($auth_data_json, true);
    return $auth_data;
  }
  return false;
}
if(isset($_GET['postID']))
{
	$postID=$_GET['postID'];
}else{
	$postID="1";
}
if (isset($_GET['logout'])) {
  setcookie('tg_user', '');
  header('Location: index.php?postID='.$postID);
}

    $manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");
    $collection = new MongoDB\Collection($manager, "QR_DATA", "QUESTIONS");
	$postData = $collection->findOne(['postID' => $postID]);
    $collection = new MongoDB\Collection($manager, "QR_DATA", "COMMENTS");

if (isset($_POST['isComment'])) {
  $document = array( 
      "first_name" => $_POST['first_name'],
      "last_name" => $_POST['last_name'],
      "photo_url" => $_POST['photo_url'],
      "comment" => $_POST['comment'],
	  "postID" => $postID
   );
   $collection->insertOne($document);
}

$tg_user = getTelegramUserData();
if ($tg_user !== false) {
  
  if (isset($tg_user['first_name'])) {
	  $first_name = htmlspecialchars($tg_user['first_name']);
  }else{
	  $first_name = "";
  }
  if (isset($tg_user['last_name'])) {
	  $last_name = htmlspecialchars($tg_user['last_name']);
  }else{
	  $last_name = "";
  }
  if (isset($tg_user['username'])) {
    $username = htmlspecialchars($tg_user['username']);
  }else{
	  $username = "";
  }
  if (isset($tg_user['photo_url'])) {
    $photo_url = htmlspecialchars($tg_user['photo_url']);
  }else{
	  $photo_url = "img/unknown.png";
  }
} else {
  $bot_username = BOT_USERNAME;
}

	$cursor = $collection->find(['postID' => $postID]);
?>
<!doctype html>
                        <html>
                            <head>
                                <meta charset='utf-8'>
                                <meta name='viewport' content='width=device-width, initial-scale=1'>
                                <title>QR-Bot</title>
                                <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-alpha1/dist/css/bootstrap.min.css' rel='stylesheet'>
                                <link href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css' rel='stylesheet'>
                                <style>@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800&display=swap");

body {
    background-color: #eee;
    font-family: "Poppins", sans-serif;
    font-weight: 300
}

.card {
    border: none
}

.ellipsis {
    color: #a09c9c
}

hr {
    color: #a09c9c;
    margin-top: 4px;
    margin-bottom: 8px
}

.muted-color {
    color: #a09c9c;
    font-size: 13px
}

.ellipsis i {
    margin-top: 3px;
    cursor: pointer
}

.icons i {
    font-size: 25px
}

.icons .fa-heart {
    color: red
}

.icons .fa-smile-o {
    color: yellow;
    font-size: 29px
}

.rounded-image {
    border-radius: 50% !important;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50px;
    width: 50px
}

.name {
    font-weight: 600
}

.comment-text {
    font-size: 12px
}

.status small {
    margin-right: 10px;
    color: blue
}

.form-control {
    border-radius: 26px
}

.comment-input {
    position: relative
}

.fonts {
    position: absolute;
    right: 13px;
    top: 8px;
    color: #a09c9c
}

.form-control:focus {
    color: #495057;
    background-color: #fff;
    border-color: #8bbafe;
    outline: 0;
    box-shadow: none
}</style>
                                <script type='text/javascript' src=''></script>
                                <script type='text/javascript' src='https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-alpha1/dist/js/bootstrap.bundle.min.js'></script>
                                <script type='text/javascript'></script>
                            </head>
                            <body oncontextmenu='return false' class='snippet-body'>
                            <div class="container mt-5 mb-5">
    <div class="row d-flex align-items-center justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="d-flex justify-content-between p-2 px-3">
                    <div class="d-flex flex-row align-items-center"> <img src="img/logo.jpg" width="50" class="rounded-circle">
                        <div class="d-flex flex-column ml-2"> <span class="font-weight-bold">Javi QR</span> <small class="text-primary">Administrator</small> </div>
                    </div>
                </div> 
				<img src="img/logo.jpg" class="img-fluid">
                <div class="p-2">
                    <p class="text-justify"><h1><?php echo $postData['question-eng']; ?></h1></p>
                    <hr>
					<p class="text-justify"><b>Comments:</b></p>
                    <div class="comments">
					<?php 
					foreach ($cursor as $document) { ?>
						<div class="d-flex flex-row mb-2"> <img src="<?php echo $document['photo_url']; ?>" width="40" class="rounded-image">
                            <div class="d-flex flex-column ml-2"> <span class="name"><?php echo $document['first_name']." ".$document['last_name']; ?></span> <small class="comment-text"><?php echo $document['comment']; ?></small>
                            </div>
                        </div>
                    <hr>
					<?php }
						if(isset($_COOKIE['tg_user'])){	?>
                        <div class="d-flex flex-row mb-2"> <img src="<?php echo $photo_url; ?>" width="40" class="rounded-image">
                            <div class="d-flex flex-column ml-2"> <span class="name"><?php echo $first_name." ".$last_name; ?>   <a href="?logout=1&postID=<?php echo $postID; ?>">Logout</a></span> <small class="comment-text">Write a comment below...</small>
                            </div>	
                        </div>
						<form action="/bot/index.php?postID=<?php echo $postID; ?>" method="post">
							<div class="comment-input"> 
								<input type="text" name="comment" class="form-control">
								<input type="hidden" name="isComment" class="form-control" value="true">
								<input type="hidden" name="first_name" class="form-control" value="<?php echo $first_name; ?>">
								<input type="hidden" name="last_name" class="form-control" value="<?php echo $last_name; ?>">
								<input type="hidden" name="postID" class="form-control" value="<?php echo $postID; ?>">
								<input type="hidden" name="photo_url" class="form-control" value="<?php echo $photo_url; ?>">
							</div>
						</form>
						<?php }else{ ?>
						<script async src="https://telegram.org/js/telegram-widget.js?14" data-telegram-login="inkestak_bot" data-size="large" data-auth-url="login_main.php?postID=<?php echo $postID; ?>" data-request-access="write"></script>
						<?php } ?></div>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
<?php

?>
