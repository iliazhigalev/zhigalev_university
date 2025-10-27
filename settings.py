from envparse import Env

env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default= "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
)


TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default= "postgresql+asyncpg://postgres_test:postgres_test@localhost:5433/postgres_test"
)
