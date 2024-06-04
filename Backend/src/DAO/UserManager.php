<?php

namespace App\DAO;

use App\Model\User;

class UserManager extends DataManager
{
    public function create(User $user, string $password): User
    {
        if ($this->emailExists($user->getEmail())) {
            throw new \Exception('Email already exists.');
        }


        $sql = "INSERT INTO users (firstname, lastName, email,password) VALUES (:firstname, :lastName, :email,:password)";
        $stmt = $this->prepare($sql);

        $firstname = $user->getFirstname();
        $lastName = $user->getLastName();
        $email = $user->getEmail();
        $hashedPassword = password_hash($password, PASSWORD_BCRYPT);


        $stmt->bindParam(':firstname', $firstname);
        $stmt->bindParam(':lastName', $lastName);
        $stmt->bindParam(':email', $email);
        $stmt->bindParam(':password', $hashedPassword);


        try {
            $stmt->execute();

            return $this->getUserByEmail($email);
        } catch (\PDOException $e) {
            http_response_code(500);
            throw new \Exception("Erreur interne au serveur");
            return false;
        }
    }

    public function setOtpValidated(int $userId): bool
    {
        $sql = "UPDATE users SET is_otp_validated = TRUE WHERE id = :id";
        $stmt = $this->prepare($sql);
        $stmt->bindParam(':id', $userId);

        try {
            return $stmt->execute();
        } catch (\PDOException $e) {
            http_response_code(500);
            throw new \Exception("Erreur interne au serveur");
            return false;
        }
    }


    private function emailExists(string $email): bool
    {
        $sql = "SELECT COUNT(*) FROM users WHERE email = :email";
        $stmt = $this->prepare($sql);
        $stmt->bindParam(':email', $email);
        $stmt->execute();
        $result = $stmt->fetchColumn();
        return $result > 0;
    }

    // private function phoneNumberExists(int $phoneNumber): bool
    // {
    //     $sql = "SELECT COUNT(*) FROM users WHERE phoneNumber = :phoneNumber";
    //     $stmt = $this->prepare($sql);
    //     $stmt->bindParam(':phoneNumber', $phoneNumber, \PDO::PARAM_INT);
    //     $stmt->execute();
    //     $result = $stmt->fetchColumn();
    //     return $result > 0;
    // }
    public function getUserByEmail(string $email): User
    {
        $sql = "SELECT * FROM users WHERE email = :email";
        $stmt = $this->prepare($sql);
        $stmt->bindParam(':email', $email, \PDO::PARAM_INT);
        $stmt->execute();
        $userData = $stmt->fetch(\PDO::FETCH_ASSOC);

        if ($userData) {
            // Créer un objet User à partir des données récupérées de la base de données
            $user = new User(
                $userData['firstname'],
                $userData['lastName'],
                $userData['email'],
                $userData['is_otp_validated'],
                $userData['password'],
                $userData['id'],
            );

            return $user;
        } else {
            throw new \Exception("Utilisateur introuvable!!");
        }
    }
}
