import random
from faker import Faker

fake = Faker("es_ES")

def generate_seed(num_products=10, num_policies=50, coverages_per_policy=(1, 3), output_file="seed.sql"):
    """
    Genera un archivo seed.sql con datos fake para las tablas:
    product, policy y policy_coverage.
    """

    # Prepara archivo
    with open(output_file, "w", encoding="utf-8") as f:

        # --------------------
        # Tabla product
        # --------------------
        f.write("-- Insertar productos\n")
        for i in range(1, num_products + 1):
            code = f"PRD{i:03d}"
            name = fake.word().capitalize() + " " + fake.word().capitalize()
            description = fake.sentence()
            product_type = random.choice(["LIFE", "AUTO", "HOME", "HEALTH"])
            base_premium = round(random.uniform(50, 500), 2)

            f.write(
                f"INSERT INTO product (code, name, description, product_type, base_premium) "
                f"VALUES ('{code}', '{name}', '{description}', '{product_type}', {base_premium});\n"
            )

        f.write("\n")

        # --------------------
        # Tabla policy
        # --------------------
        f.write("-- Insertar pólizas\n")
        for i in range(1, num_policies + 1):
            policy_number = f"POL-{i:06d}"
            customer_id = random.randint(1, 1000)  # referencia lógica a microservicio Customer
            product_id = random.randint(1, num_products)
            agent_id = random.randint(1, 50)  # referencia lógica a microservicio Agent
            start_date = fake.date_between(start_date="-2y", end_date="today")
            end_date = fake.date_between(start_date=start_date, end_date="+1y")
            sum_insured = round(random.uniform(10000, 100000), 2)
            premium = round(sum_insured * random.uniform(0.01, 0.05), 2)
            status = random.choice(["ACTIVE", "CANCELLED", "EXPIRED"])

            f.write(
                f"INSERT INTO policy (policy_number, customer_id, product_id, agent_id, start_date, end_date, sum_insured, premium, status) "
                f"VALUES ('{policy_number}', {customer_id}, {product_id}, {agent_id}, '{start_date}', '{end_date}', {sum_insured}, {premium}, '{status}');\n"
            )

        f.write("\n")

        # --------------------
        # Tabla policy_coverage
        # --------------------
        f.write("-- Insertar coberturas\n")
        coverage_id = 1
        for policy_id in range(1, num_policies + 1):
            for _ in range(random.randint(*coverages_per_policy)):
                coverage_code = f"COV-{coverage_id:04d}"
                coverage_name = "Cobertura " + fake.word().capitalize()
                coverage_limit = round(random.uniform(5000, 50000), 2)
                deductible = round(random.uniform(0, 1000), 2)

                f.write(
                    f"INSERT INTO policy_coverage (policy_id, coverage_code, coverage_name, coverage_limit, deductible) "
                    f"VALUES ({policy_id}, '{coverage_code}', '{coverage_name}', {coverage_limit}, {deductible});\n"
                )
                coverage_id += 1

        print(f"✅ Archivo {output_file} generado con {num_products} productos, {num_policies} pólizas y coberturas asociadas.")


if __name__ == "__main__":
    # Puedes cambiar los parámetros aquí:
    generate_seed(num_products=50, num_policies=20000, coverages_per_policy=(1, 3))