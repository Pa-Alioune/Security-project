<?php

namespace App\Dto;

use App\Model\User;

class UserDto
{
    public int $id;
    public string $firstname;
    public string $lastName;
    public string $email;

    public static function toUserDto(User $user): UserDto
    {
        $userDto = new UserDto();
        $userDto->firstname = $user->getFirstname();
        $userDto->lastName = $user->getLastName();
        $userDto->email = $user->getEmail();
        $userDto->id = $user->getId();
        return $userDto;
    }
}
