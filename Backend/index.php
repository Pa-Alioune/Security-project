<?php

use App\Controller\ErreurController;
use App\Controller\UserController;

require "./vendor/autoload.php";

$dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
$dotenv->load();


$cotrollerPath = __DIR__ . DIRECTORY_SEPARATOR . "Controller" . DIRECTORY_SEPARATOR;

$UserController = new UserController();
$erreur = new ErreurController();

$action = $_GET["action"] ?? "erreur";


if ($action === "register") {
    $UserController->create();
}
if ($action === "login") {
    $UserController->login();
}
if ($action === "userinfo") {
    $UserController->getUserInfo();
} else {
    $erreur->notFound();
}
