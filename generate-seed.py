import random
from faker import Faker
import os

# ruta relativa: ./init/seed.sql
output_path = os.path.join("init", "seed.sql")

fake = Faker("es_ES")

def batch_insert(table, columns, rows, f, batch_size=500):
    """
    Escribe inserciones agrupadas en lotes.
    """
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i+batch_size]
        values = ",\n".join(batch)
        f.write(f"INSERT INTO {table} ({', '.join(columns)}) VALUES\n{values};\n\n")


def append_seed(num_policies=50, coverages_per_policy=(1, 3), beneficiaries_per_policy=(0, 2), output_file=output_path):
    """
    Agrega inserts de policy, policy_coverage y beneficiary al final de seed.sql
    (sin tocar los productos que ya están en el archivo).
    """

    with open(output_file, "w", encoding="utf-8") as f:  # 👈 append, no overwrite

        # --------------------
        # Tabla policy
        # --------------------
        f.write("-- Insertar pólizas\n")
        policy_rows = []
        for i in range(1, num_policies + 1):
            policy_number = f"POL-{i:06d}"
            customer_id = random.randint(1, 4000)
            product_code = f"'PRD{random.randint(1, 15):03d}'"  # 👈 suponiendo 15 productos ya en seed.sql
            agent_id = f"'AGT{random.randint(1, 50):03d}'"
            start_date = fake.date_between(start_date="-2y", end_date="today")
            end_date = fake.date_between(start_date=start_date, end_date="+1y")
            sum_insured = round(random.uniform(10000, 100000), 2)
            premium = round(sum_insured * random.uniform(0.01, 0.05), 2)
            status = random.choice(["ACTIVE", "CANCELLED", "EXPIRED"])

            policy_rows.append(
                f"('{policy_number}', {customer_id}, {product_code}, {agent_id}, '{start_date}', '{end_date}', {sum_insured}, {premium}, '{status}')"
            )
        batch_insert(
            "policy",
            ["policy_number", "customer_id", "product_id", "agent_id", "start_date", "end_date", "sum_insured", "premium", "status"],
            policy_rows,
            f,
        )

        # --------------------
        # Tabla policy_coverage
        # --------------------
        f.write("-- Insertar coberturas\n")
        coverage_rows = []
        coverage_id = 1
        for policy_id in range(1, num_policies + 1):
            for _ in range(random.randint(*coverages_per_policy)):
                coverage_code = f"COV-{coverage_id:04d}"
                coverage_name = "Cobertura " + fake.word().capitalize()
                coverage_limit = round(random.uniform(5000, 50000), 2)
                deductible = round(random.uniform(0, 1000), 2)

                coverage_rows.append(
                    f"({policy_id}, '{coverage_code}', '{coverage_name}', {coverage_limit}, {deductible})"
                )
                coverage_id += 1
        batch_insert(
            "policy_coverage",
            ["policy_id", "coverage_code", "coverage_name", "coverage_limit", "deductible"],
            coverage_rows,
            f,
        )

        # --------------------
        # Tabla beneficiary
        # --------------------
        f.write("-- Insertar beneficiarios\n")
        beneficiary_rows = []
        beneficiary_id = 1
        for policy_id in range(1, num_policies + 1):
            for _ in range(random.randint(*beneficiaries_per_policy)):
                client_id = random.randint(1, 4000)  # ref lógica a otro microservicio
                full_name = fake.name().replace("'", "''")
                relationship = random.choice(["HIJO", "HIJA", "CONYUGE", "PADRE", "MADRE", "HERMANO", "HERMANA", "ABUELO", "ABUELA"])
                percentage = round(random.uniform(10, 100), 2)
                contact_info = fake.phone_number().replace("'", "''")

                beneficiary_rows.append(
                    f"({policy_id}, {client_id}, '{full_name}', '{relationship}', {percentage}, '{contact_info}')"
                )
                beneficiary_id += 1
        if beneficiary_rows:
            batch_insert(
                "beneficiary",
                ["policy_id", "client_id", "full_name", "relationship", "percentage", "contact_info"],
                beneficiary_rows,
                f,
            )

    print(f"✅ Datos de policies, coverages y beneficiaries agregados en {output_file}.")


if __name__ == "__main__":
    # Ajusta parámetros aquí:
    append_seed(num_policies=20000, coverages_per_policy=(1, 3), beneficiaries_per_policy=(0, 2))