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

        if (isset($data['firstname']) && isset($data['lastname'])  && isset($data['email']) && isset($data['password'])) {

            try {
                $jwt = $this->userService->createUser($data);

                if ($jwt) {

                    http_response_code(200);
                    echo json_encode(['token' => $jwt]);
                    die();
                } else {

                    echo json_encode(["success" => false, "message" => "Failed to create user"]);
                    die();
                }
            } catch (\Exception $e) {
                http_response_code(400);

                echo json_encode(["success" => false, "message" => $e->getMessage()]);
                die();
            }
        } else {
            $missingFields = [];
            if (!isset($data['firstname'])) {
                $missingFields[] = "firstname";
            }
            if (!isset($data['lastname'])) {
                $missingFields[] = "lastname";
            }
            if (!isset($data['email'])) {
                $missingFields[] = "email";
            }
            if (!isset($data['password'])) {
                $missingFields[] = "password";
            }
            http_response_code(400);
            echo json_encode(["success" => false, "message" => "Missing data. Required fields: " . implode(", ", $missingFields)]);
            die();
        }
    }

    public function login()
    {
        $data = json_decode(file_get_contents('php://input'), true);
        // die(var_dump($this->getIpAddress()));

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
            die();
        } catch (\Exception $e) {
            http_response_code(500);
            echo json_encode(['success' => false, 'message' => $e->getMessage()]);
        }
    }

    function getUserInfo()
    {

        $this->userService->getUserInfo();
        die();
    }

    function confirmOtp()
    {
        $data = json_decode(file_get_contents('php://input'), true);


        if (isset($data['otp'])) {
            $this->userService->confirmeOtp($data['otp']);
            die();
        } else {
            http_response_code(400);
            echo json_encode(["success" => false, "message" => "Missing data. Required field : otp"]);
            die();
        }
    }
}
