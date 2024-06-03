<?php

namespace App\Model;

use App\DAO\UserManager;

class Model
{

    protected UserManager $userManager;

    public function __construct()
    {
        $this->userManager = new UserManager();
    }
}
