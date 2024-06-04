<?php

namespace App\Service;

use App\DAO\OtpManager;
use App\Dto\UserDto;
use App\Model\User;
use Firebase\JWT\JWT;

class UserService
{
    // private User $user;
    private TokenService $tokenService;
    private OtpManager $otpManager;
    private MailService $mailService;
    public function __construct()
    {
        $this->tokenService = new TokenService();
        $this->mailService = new MailService();
        $this->otpManager = new OtpManager();
    }

    public function createUser($data)
    {
        $firstname = $data['firstname'];
        $lastname = $data['lastname'];
        $email = $data['email'];
        $password = $data["password"];

        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            http_response_code(400);
            echo json_encode(["success" => false, "message" => "Adresse email invalide"]);
            die();
        }

        // Validation du mot de passe
        if (
            strlen($password) < 8 ||
            !preg_match('/[A-Z]/', $password) ||
            !preg_match('/[a-z]/', $password) ||
            !preg_match('/[0-9]/', $password) ||
            !preg_match('/[!@#$%^&*(),.?":{}|<>]/', $password)
        ) {
            http_response_code(400);
            echo json_encode(["success" => false, "message" => "Le mot de passe doit contenir au moins 8 caractères et inclure des lettres majuscules, minuscules, des chiffres et des symboles"]);
            die();
        }
        $user = new User($firstname, $lastname, $email);
        $user = $user->create($user, $password);
        $otp =  $this->otpManager->create($user->getId());
        $this->mailService->sendEmail($user->getEmail(), $otp);
        return  $this->tokenService->generateToken($user);
    }

    function login(string $email, string $password): string
    {
        $user = $this->getUserByEmail($email);

        if (!$user || !password_verify($password, $user->getPassword()) || $user->getEmail() !== $email) {
            http_response_code(401);
            echo json_encode(['success' => false, 'message' => 'Invalid credentials']);
            die();
        }

        return  $this->tokenService->generateToken($user);
    }

    public function getUserByEmail(string $email): User
    {

        return User::findByEmail($email);
    }

    protected function authenticate()
    {
        $headers = apache_request_headers();
        $authHeader = $headers['Authorization'] ?? '';

        if (preg_match('/Bearer\s(\S+)/', $authHeader, $matches)) {
            $jwt = $matches[1];

            try {
                $decoded = $this->tokenService->verifyToken($jwt);
                $id = $decoded->data->id;
                $email = $decoded->data->email;

                $user = $this->getUserByEmail($email);
                if ($user->getId() === $id && $user->getEmail() === $email) {
                    return $user;
                }
            } catch (\Exception $e) {
                http_response_code(401);
                echo json_encode(['success' => false, 'message' => 'Unauthorized']);
                exit();
            }
        }
        http_response_code(401);
        echo json_encode(['success' => false, 'message' => 'Unauthorized']);
        exit();
    }


    public function getUserInfo()
    {
        $user = $this->authenticate();
        $user = $this->verifyOtp();


        echo json_encode(UserDto::toUserDto($user));
        die();
    }
    public function confirmeOtp(string $otp)
    {
        $user = $this->authenticate();

        if ($this->otpManager->isOtpValidated($user->getId(), $otp)) {

            $user->confirm();
            http_response_code(200);
            die();
        }
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'OTP incorrect']);
        die();
    }
    public function verifyOtp(): User
    {
        $user = $this->authenticate();
        // Vérifiez si l'OTP a été validé
        if ($user->getIsOtpValidated()) {
            return $user;
        }
        http_response_code(401);
        echo json_encode(['success' => false, 'message' => 'OTP not validated']);
        die();
    }
}
