from datetime import date
from typing import Optional

import strawberry

from pet_hotel.db import get_db_connection
from pet_hotel.models import Booking, Owner, Pet


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_owner(
        self,
        fullname: str,
        phone: str,
        email: Optional[str] = None,
        address: Optional[str] = None,
    ) -> Owner:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO owners (fullname, phone, email, address) VALUES (%s, %s, %s, %s) RETURNING id",
            (fullname, phone, email, address),
        )
        owner_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return Owner(
            id=owner_id, fullname=fullname, phone=phone, email=email, address=address
        )

    @strawberry.mutation
    def create_pet(self, name: str, species: str, age: int, owner_id: int) -> Pet:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO pets (name, species, age, owner_id) VALUES (%s, %s, %s, %s) RETURNING id",
            (name, species, age, owner_id),
        )
        pet_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return Pet(id=pet_id, name=name, species=species, age=age, owner_id=owner_id)

    @strawberry.mutation
    def create_booking(
        self, pet_id: int, check_in_date: date, check_out_date: Optional[date] = None
    ) -> Booking:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO bookings (pet_id, check_in_date, check_out_date) VALUES (%s, %s, %s) RETURNING id",
            (pet_id, check_in_date, check_out_date),
        )
        booking_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return Booking(
            id=booking_id,
            pet_id=pet_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
        )

    @strawberry.mutation
    def delete_booking(self, booking_id: int) -> bool:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM bookings WHERE id = %s RETURNING id", (booking_id,))
        deleted_id = cur.fetchone()
        conn.commit()

        cur.close()
        conn.close()

        return deleted_id is not None

    @strawberry.mutation
    def update_booking(
        self,
        booking_id: int,
        pet_id: Optional[int] = None,
        check_in_date: Optional[date] = None,
        check_out_date: Optional[date] = None,
    ) -> Optional[Booking]:
        conn = get_db_connection()
        cur = conn.cursor()

        # Build the SQL query dynamically based on which fields are provided
        fields = []
        values = []

        if pet_id is not None:
            fields.append("pet_id = %s")
            values.append(pet_id)

        if check_in_date is not None:
            fields.append("check_in_date = %s")
            values.append(check_in_date)

        if check_out_date is not None:
            fields.append("check_out_date = %s")
            values.append(check_out_date)

        if not fields:
            # No fields to update
            return None

        values.append(booking_id)
        sql_query = f"UPDATE bookings SET {', '.join(fields)} WHERE id = %s RETURNING id, pet_id, check_in_date, check_out_date"

        cur.execute(sql_query, values)
        updated_booking = cur.fetchone()
        conn.commit()

        cur.close()
        conn.close()

        if updated_booking:
            return Booking(
                id=updated_booking[0],
                pet_id=updated_booking[1],
                check_in_date=updated_booking[2],
                check_out_date=updated_booking[3],
            )
        else:
            return None
