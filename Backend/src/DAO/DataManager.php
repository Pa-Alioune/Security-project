<?php

namespace App\DAO;


class DataManager
{
    protected function getPdo(): \PDO
    {
        return new \PDO('mysql:host=localhost;dbname=securePwd;charset=utf8', 'root', "");
    }

    public function prepare(string $sql): \PDOStatement
    {
        return $this->getPdo()->prepare($sql);
    }
}
