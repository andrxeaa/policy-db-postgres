CREATE TABLE product (
  id SERIAL PRIMARY KEY,
  code VARCHAR(50) NOT NULL UNIQUE,       -- Identificador alfanumérico (ej: PRD001)
  name VARCHAR(255) NOT NULL,
  description TEXT,
  product_type VARCHAR(50),
  base_premium NUMERIC(12,2) DEFAULT 0
);

CREATE TABLE policy (
  id SERIAL PRIMARY KEY,
  policy_number VARCHAR(100) NOT NULL UNIQUE,
  customer_id INTEGER NOT NULL,  -- referencia lógica a microservicio Customer
  product_id VARCHAR(50) NOT NULL REFERENCES product(code) ON DELETE RESTRICT, -- ahora apunta a 'code'
  agent_id VARCHAR(50),          -- referencia lógica a microservicio Agent
  start_date DATE,
  end_date DATE,
  sum_insured NUMERIC(14,2),
  premium NUMERIC(12,2),
  status VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_policy_customer_id ON policy(customer_id);
CREATE INDEX idx_policy_product_id ON policy(product_id);

CREATE TABLE policy_coverage (
  id SERIAL PRIMARY KEY,
  policy_id INTEGER NOT NULL REFERENCES policy(id) ON DELETE CASCADE,
  coverage_code VARCHAR(100),
  coverage_name VARCHAR(255),
  coverage_limit NUMERIC(14,2),
  deductible NUMERIC(12,2)
);

CREATE INDEX idx_policycoverage_policy_id ON policy_coverage(policy_id);

CREATE TABLE beneficiary (
    id BIGSERIAL PRIMARY KEY,
    policy_id BIGINT NOT NULL,
    client_id BIGINT NOT NULL,            -- referencia lógica al microservicio de clientes
    full_name VARCHAR(255) NOT NULL,      -- nombre del beneficiario
    relationship VARCHAR(50) NOT NULL,    -- Ej: hijo, cónyuge, padre
    percentage NUMERIC(5,2),              -- opcional: % de la suma asegurada
    contact_info TEXT,                    -- opcional: datos de contacto
    
    CONSTRAINT fk_beneficiary_policy FOREIGN KEY (policy_id) REFERENCES policy(id) ON DELETE CASCADE
);

CREATE INDEX idx_beneficiary_policy_id ON beneficiary(policy_id);
