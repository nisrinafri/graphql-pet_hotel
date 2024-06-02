from datetime import date
from typing import List, Optional

import strawberry

from pet_hotel.db import get_db_connection


def get_pets_for_owner(root: "Owner"):
    assert root.id != 0

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, species, age, owner_id FROM pets WHERE owner_id = %(owner_id)s",
        {"owner_id": root.id},
    )
    rows = cur.fetchall()

    pets = [
        Pet(id=row[0], name=row[1], species=row[2], age=row[3], owner_id=row[4])
        for row in rows
    ]

    cur.close()
    conn.close()

    return pets


def get_pet_for_booking(root: "Booking"):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, species, age, owner_id FROM pets WHERE id = %(pet_id)s",
        {"pet_id": root.pet_id},
    )
    row = cur.fetchone()

    pet = (
        Pet(id=row[0], name=row[1], species=row[2], age=row[3], owner_id=row[4])
        if row
        else None
    )

    cur.close()
    conn.close()

    return pet


def get_owner_for_booking(root: "Booking"):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT o.id, o.fullname, o.phone, o.email, o.address 
        FROM owners o
        JOIN pets p ON o.id = p.owner_id
        WHERE p.id = %(pet_id)s
        """,
        {"pet_id": root.pet_id},
    )
    row = cur.fetchone()

    owner = (
        Owner(id=row[0], fullname=row[1], phone=row[2], email=row[3], address=row[4])
        if row
        else None
    )

    cur.close()
    conn.close()

    return owner


@strawberry.type
class Owner:
    id: int
    fullname: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    pets: List["Pet"] = strawberry.field(resolver=get_pets_for_owner)


@strawberry.type
class Pet:
    id: int
    name: str
    species: str
    age: int
    owner_id: int


@strawberry.type
class Booking:
    id: int
    pet_id: int
    check_in_date: date
    check_out_date: Optional[date] = None
    pet: Optional[Pet] = strawberry.field(resolver=get_pet_for_booking)
    owner: Optional[Owner] = strawberry.field(resolver=get_owner_for_booking)
