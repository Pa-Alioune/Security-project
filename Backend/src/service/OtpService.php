<?php

namespace App\Service;

class OtpService
{

    public function generateOtp(int $length = 6): string
    {
        $otp = '';
        for ($i = 0; $i < $length; $i++) {
            $otp .= mt_rand(0, 9);
        }
        return $otp;
    }

    public function getOtpExpiration()
    {
        $expiration = new \DateTime();
        $expiration->add(new \DateInterval('PT5M')); // Add 5 minutes
        return $expiration->getTimestamp();
    }
}
