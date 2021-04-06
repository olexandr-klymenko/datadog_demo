from faker import Faker
import requests

if __name__ == "__main__":
    fake = Faker()
    for _ in range(20):
        name = fake.name()
        birthdate = fake.date_between(start_date='-40y', end_date='-25y')
        print(name, birthdate)

# TODO: finish data generation
