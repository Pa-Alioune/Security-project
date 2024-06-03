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

        if ($this->phoneNumberExists($user->getPhoneNumber())) {
            throw new \Exception('Phone number already exists.');
        }
        $sql = "INSERT INTO users (firstname, lastName, phoneNumber, email,password) VALUES (:firstname, :lastName, :phoneNumber, :email,:password)";
        $stmt = $this->prepare($sql);

        $firstname = $user->getFirstname();
        $lastName = $user->getLastName();
        $phoneNumber = $user->getPhoneNumber();
        $email = $user->getEmail();
        $hashedPassword = password_hash($password, PASSWORD_BCRYPT);


        $stmt->bindParam(':firstname', $firstname);
        $stmt->bindParam(':lastName', $lastName);
        $stmt->bindParam(':phoneNumber', $phoneNumber, \PDO::PARAM_INT);
        $stmt->bindParam(':email', $email);
        $stmt->bindParam(':password', $hashedPassword);


        try {
            $stmt->execute();

            return $this->getUserByEmail($phoneNumber);
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

    private function phoneNumberExists(int $phoneNumber): bool
    {
        $sql = "SELECT COUNT(*) FROM users WHERE phoneNumber = :phoneNumber";
        $stmt = $this->prepare($sql);
        $stmt->bindParam(':phoneNumber', $phoneNumber, \PDO::PARAM_INT);
        $stmt->execute();
        $result = $stmt->fetchColumn();
        return $result > 0;
    }
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
                $userData['phoneNumber'],
                $userData['email'],
                $userData['password'],
                $userData['id'],
            );
            return $user;
        } else {
            throw new \Exception("Utilisateur introuvable!!");
        }
    }
}
