<?php

namespace App\Controller;

class ErreurController
{

    public function notFound()
    {
        http_response_code(404);
        echo json_encode(["erreur" => true, "message" => "url not found"]);
    }
}
