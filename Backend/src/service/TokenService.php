<?php

namespace App\Service;

use App\Model\User;
use Firebase\JWT\JWT;
use Firebase\JWT\Key;
use Exception;

class TokenService
{
    private string $secretKey;
    private string $domaine;


    public function __construct()
    {
        $this->secretKey = $_ENV['JWT_SECRET'];
        $this->domaine = $_ENV['DOMAINE_NAME'];
    }

    public function generateToken(User $user): string
    {
        $payload = [
            'iss' => $this->domaine,
            'iat' => time(),
            'exp' => time() + 3600, // 1 heure d'expiration
            'data' => [
                'id' => $user->getId(),
                'email' => $user->getEmail(),
            ],
        ];
        return JWT::encode($payload, $this->secretKey, 'HS256');
    }

    public function verifyToken(string $token): object
    {
        try {
            return JWT::decode($token, new Key($this->secretKey, 'HS256'));
        } catch (Exception $e) {
            throw new Exception("Invalid token: " . $e->getMessage());
        }
    }
}
