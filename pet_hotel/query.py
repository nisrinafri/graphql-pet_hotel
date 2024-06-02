from typing import List

import strawberry

from pet_hotel.db import get_db_connection
from pet_hotel.models import Booking, Owner, Pet
from pet_hotel.mutation import Mutation


@strawberry.type
class Query:
    @strawberry.field
    def owners(self) -> List[Owner]:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, fullname, phone, email, address FROM owners")
        rows = cur.fetchall()

        owners = [
            Owner(
                id=row[0], fullname=row[1], phone=row[2], email=row[3], address=row[4]
            )
            for row in rows
        ]

        cur.close()
        conn.close()

        return owners

    @strawberry.field
    def pets(self) -> List[Pet]:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name, species, age, owner_id FROM pets")
        rows = cur.fetchall()

        pets = [
            Pet(id=row[0], name=row[1], species=row[2], age=row[3], owner_id=row[4])
            for row in rows
        ]

        cur.close()
        conn.close()

        return pets

    @strawberry.field
    def bookings(self) -> List[Booking]:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, pet_id, check_in_date, check_out_date FROM bookings")
        rows = cur.fetchall()

        bookings = [
            Booking(
                id=row[0], pet_id=row[1], check_in_date=row[2], check_out_date=row[3]
            )
            for row in rows
        ]

        cur.close()
        conn.close()

        return bookings

    @strawberry.field
    def pets_by_species(self, species: str) -> List[Pet]:
        if species == "":
            raise ValueError("Invalid species variable")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, name, species, age, owner_id FROM pets WHERE species = %(species)s",
            {"species": species},
        )
        rows = cur.fetchall()

        pets = [
            Pet(id=row[0], name=row[1], species=row[2], age=row[3], owner_id=row[4])
            for row in rows
        ]

        cur.close()
        conn.close()

        return pets


schema = strawberry.Schema(query=Query, mutation=Mutation)
