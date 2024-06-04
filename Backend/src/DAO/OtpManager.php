<?php

namespace App\DAO;

use App\Service\OtpService;

class OtpManager extends DataManager
{

    private OtpService $otpService;
    public function __construct()
    {
        $this->otpService = new OtpService();
    }
    public function create(int $id): string
    {

        $otp = $this->otpService->generateOtp();
        $expiration = $this->otpService->getOtpExpiration();
        $sql = "INSERT INTO otps (user_id, otp, expires_at)  VALUES (:user_id, :otp, :expires_at)";
        $stmt = $this->prepare($sql);
        $stmt->bindParam(':user_id', $id);
        $stmt->bindParam(':otp', $otp);
        $stmt->bindParam(':expires_at', $expiration);

        try {
            $stmt->execute();
            return $otp;
        } catch (\PDOException $e) {
            http_response_code(500);
            throw new \Exception("Erreur interne au serveur");
            return false;
        }
    }
    public function isOtpValidated(int $userId, string $otp): bool
    {
        $sql = "SELECT otp, expires_at FROM otps WHERE user_id = :user_id AND otp = :otp ORDER BY created_at DESC LIMIT 1";
        $stmt = $this->prepare($sql);
        $stmt->bindParam(':user_id', $userId, \PDO::PARAM_INT);
        $stmt->bindParam(':otp', $otp, \PDO::PARAM_STR);

        try {
            $stmt->execute();
            $row = $stmt->fetch(\PDO::FETCH_ASSOC);
            if ($row) {

                return time() < $row['expires_at'];
            }
            return false;
        } catch (\PDOException $e) {
            http_response_code(500);
            throw new \Exception("Erreur interne au serveur");
        }
    }
}
