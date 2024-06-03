<?php

namespace App\Controller;

use App\Dto\UserDto;
use App\Model\User;
use App\Service\UserService;

class UserController
{

    private UserService $userService;
    public function __construct()
    {
        $this->userService = new UserService();
    }

    public function create()
    {
        $data = json_decode(file_get_contents('php://input'), true);

        if (isset($data['firstname']) && isset($data['lastname']) && isset($data['phoneNumber']) && isset($data['email']) && isset($data['password'])) {

            try {
                $user = $this->userService->createUser($data);

                if ($user) {
                    echo json_encode(UserDto::toUserDto($user));
                    exit();
                } else {
                    echo json_encode(["success" => false, "message" => "Failed to create user"]);
                    exit();
                }
            } catch (\Exception $e) {
                echo json_encode(["success" => false, "message" => $e->getMessage()]);
            }
        } else {
            $missingFields = [];
            if (!isset($data['firstname'])) {
                $missingFields[] = "firstname";
            }
            if (!isset($data['lastname'])) {
                $missingFields[] = "lastname";
            }
            if (!isset($data['phoneNumber'])) {
                $missingFields[] = "phoneNumber";
            }
            if (!isset($data['email'])) {
                $missingFields[] = "email";
            }
            if (!isset($data['password'])) {
                $missingFields[] = "password";
            }
            $secretKey = $_ENV['JWT_SECRET'];
            http_response_code(400);
            echo json_encode(["success" => false, "message" => "Missing data. Required fields: " . implode(", ", $missingFields)]);
            exit();
        }
    }

    public function login()
    {
        $data = json_decode(file_get_contents('php://input'), true);

        $email = $data['email'] ?? null;
        $password = $data['password'] ?? null;

        if (!$email || !$password) {
            http_response_code(400);
            echo json_encode(['success' => false, 'message' => 'Missing email or password']);
            return;
        }

        try {
            $jwt = $this->userService->login($email, $password);

            echo json_encode(['token' => $jwt]);
            exit();
        } catch (\Exception $e) {
            http_response_code(500);
            echo json_encode(['success' => false, 'message' => $e->getMessage()]);
        }
    }

    function getUserInfo()
    {

        $this->userService->getUserInfo();
        exit();
    }
}
