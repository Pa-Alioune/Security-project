<?php

namespace App\Model;

use App\DAO\UserManager;

class User extends Model
{
    private int $id;
    private string $firstname;
    private string $lastName;
    private string $email;
    private string $password;
    private bool $isOtpValidated;


    public function __construct(
        string $firstname,
        string $lastName,
        string $email,
        bool $isOtpValidated = null,
        string $password = null,
        int $id = null,

    ) {
        parent::__construct();
        $this->firstname = $firstname;
        $this->lastName = $lastName;
        $this->email = $email;
        if ($id !== null) {
            $this->id = $id;
        }
        if ($password !== null) {

            $this->password = $password;
        }
        if ($isOtpValidated !== null) {
            $this->isOtpValidated = $isOtpValidated;
        }
    }

    public function create(User $user, string $password): User
    {
        return $this->userManager->create($user, $password);
    }
    public static function findByEmail(string $email): User
    {
        $userManager = new UserManager();
        return $userManager->getUserByEmail($email);
    }
    public  function confirm(): bool
    {
        return $this->userManager->setOtpValidated($this->getId());
    }

    // Autres méthodes getter et setter...

    /**
     * Get the value of id
     */
    public function getId()
    {
        return $this->id;
    }

    /**
     * Set the value of id
     *
     * @return  self
     */
    public function setId($id)
    {
        $this->id = $id;

        return $this;
    }

    /**
     * Get the value of firstname
     */
    public function getFirstname()
    {
        return $this->firstname;
    }

    /**
     * Set the value of firstname
     *
     * @return  self
     */
    public function setFirstname($firstname)
    {
        $this->firstname = $firstname;

        return $this;
    }

    /**
     * Get the value of lastName
     */
    public function getLastName()
    {
        return $this->lastName;
    }

    /**
     * Set the value of lastName
     *
     * @return  self
     */
    public function setLastName($lastName)
    {
        $this->lastName = $lastName;

        return $this;
    }

    /**
     * Get the value of email
     */
    public function getEmail()
    {
        return $this->email;
    }

    /**
     * Set the value of email
     *
     * @return  self
     */
    public function setEmail($email)
    {
        $this->email = $email;

        return $this;
    }



    /**
     * Get the value of password
     */
    public function getPassword()
    {
        return $this->password;
    }

    /**
     * Get the value of isOtpValidated
     */
    public function getIsOtpValidated()
    {
        return $this->isOtpValidated;
    }

    /**
     * Set the value of isOtpValidated
     *
     * @return  self
     */
    public function setIsOtpValidated($isOtpValidated)
    {
        $this->isOtpValidated = $isOtpValidated;

        return $this;
    }
}
