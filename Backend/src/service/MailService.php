<?php

namespace App\Service;

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

class MailService
{
    public function sendEmail(string $receiverEmail, string $otp)
    {
        $mail = new PHPMailer(true); // Enable exceptions for error handling

        try {
            // Configure SMTP
            $mail->isSMTP();
            $mail->Host = $_ENV['mail.host'];
            $mail->SMTPAuth = true;
            $mail->Username = $_ENV['mail.username'];
            $mail->Password = $_ENV['mail.password'];
            $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
            $mail->Port = $_ENV['mail.port'];

            $mail->setFrom($_ENV['mail.sendEmail'], 'Dev dic3 sécurité');
            $mail->addAddress($receiverEmail);

            $mail->Subject = 'Votre Code de Confirmation OTP';
            $mail->isHTML(true);

            $mail->Body = '
                <!DOCTYPE html>
                <html lang="fr">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Confirmation de Code OTP</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f5f5f5;
                            margin: 0;
                            padding: 0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                        }
                        .container {
                            background-color: #ffffff;
                            border-radius: 10px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            padding: 20px;
                            max-width: 400px;
                            text-align: center;
                        }
                        .container h1 {
                            color: #333333;
                            margin-bottom: 20px;
                        }
                        .otp {
                            font-size: 24px;
                            font-weight: bold;
                            letter-spacing: 2px;
                            margin: 20px 0;
                            padding: 10px;
                            border: 2px dashed #4CAF50;
                            border-radius: 5px;
                            background-color: #e8f5e9;
                            color: #4CAF50;
                        }
                        .message {
                            color: #666666;
                            margin-bottom: 20px;
                        }
                        .footer {
                            margin-top: 20px;
                            font-size: 12px;
                            color: #999999;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Votre Code de Confirmation</h1>
                        <p class="message">Utilisez le code ci-dessous pour confirmer votre adresse email.</p>
                        <div class="otp">' . htmlspecialchars($otp) . '</div>
                        <p class="message">Ce code expirera dans 5 minutes.</p>
                        <div class="footer">Si vous n\'avez pas demandé ce code, veuillez ignorer cet email.</div>
                    </div>
                </body>
                </html>
            ';
            $mail->AltBody = 'Votre code de confirmation est ' . $otp . '. Ce code expirera dans 30 minutes.';

            // Send the message
            $mail->send();
        } catch (Exception $e) {
            throw new \Exception("Mailer Error: {$mail->ErrorInfo}");
        }
    }
}
