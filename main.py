import os
from typing import Annotated

import dotenv
import strawberry
from fastapi import Depends, FastAPI, Header, HTTPException
from strawberry.fastapi import GraphQLRouter

from pet_hotel.mutation import Mutation
from pet_hotel.query import Query

dotenv.load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


async def get_token_header(access_token: Annotated[str, Header()]):
    if access_token != ACCESS_TOKEN:
        raise HTTPException(status_code=400, detail="Access-Token header invalid")


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

app.include_router(
    graphql_app, prefix="/graphql", dependencies=[Depends(get_token_header)]
)
