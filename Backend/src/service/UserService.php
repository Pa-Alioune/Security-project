<?php

namespace App\Service;

use App\Model\User;
use Firebase\JWT\JWT;

class UserService
{
    // private User $user;
    private TokenService $tokenService;
    public function __construct()
    {
        $this->tokenService = new TokenService();
    }

    public function createUser($data)
    {
        $firstname = $data['firstname'];
        $lastname = $data['lastname'];
        $phoneNumber = $data['phoneNumber'];
        $email = $data['email'];
        $password = $data["password"];
        $user = new User($firstname, $lastname, $phoneNumber, $email);
        return $user->create($user, $password);
    }

    function login(string $email, string $password): string
    {
        $user = $this->getUserByEmail($email);

        if (!$user || !password_verify($password, $user->getPassword()) || $user->getEmail() !== $email) {
            http_response_code(401);
            echo json_encode(['success' => false, 'message' => 'Invalid credentials']);
            exit();
        }

        return  $this->tokenService->generateToken($user);
    }

    public function getUserByEmail(string $email): User
    {

        return User::findByEmail($email);
    }
}
