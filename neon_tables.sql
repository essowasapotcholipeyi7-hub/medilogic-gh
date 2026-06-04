-- ========== CRÉATION DES TABLES NEON POUR MEDILOGIC-GHP ==========

-- 1. TABLE PATIENTS
CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    structure_id INTEGER NOT NULL,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    telephone VARCHAR(20),
    adresse TEXT,
    date_naissance DATE,
    type_assurance VARCHAR(50),
    taux_prise_charge INTEGER DEFAULT 0,
    numero_assure VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 2. TABLE ACTES
CREATE TABLE IF NOT EXISTS actes (
    id SERIAL PRIMARY KEY,
    structure_id INTEGER NOT NULL,
    code VARCHAR(20),
    nom VARCHAR(200) NOT NULL,
    prix DECIMAL(10,2) NOT NULL,
    description TEXT,
    categorie VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. TABLE PRODUITS
CREATE TABLE IF NOT EXISTS produits (
    id SERIAL PRIMARY KEY,
    structure_id INTEGER NOT NULL,
    code VARCHAR(20),
    nom VARCHAR(200) NOT NULL,
    prix_vente DECIMAL(10,2) NOT NULL,
    quantite_stock INTEGER DEFAULT 0,
    seuil_alerte INTEGER DEFAULT 10,
    categorie VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 4. TABLE VENTES
CREATE TABLE IF NOT EXISTS ventes (
    id SERIAL PRIMARY KEY,
    structure_id INTEGER NOT NULL,
    patient_id INTEGER,
    type VARCHAR(20),
    montant_total DECIMAL(10,2),
    date_vente TIMESTAMP DEFAULT NOW()
);

-- 5. TABLE CONSULTATIONS
CREATE TABLE IF NOT EXISTS consultations (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    structure_id INTEGER NOT NULL,
    date_consultation DATE,
    medecin VARCHAR(100),
    motif TEXT,
    diagnostic TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 6. TABLE PRESCRIPTIONS
CREATE TABLE IF NOT EXISTS prescriptions (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    structure_id INTEGER NOT NULL,
    date_prescription DATE,
    traitement TEXT,
    posologie TEXT,
    duree TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 7. TABLE RENDEZ-VOUS
CREATE TABLE IF NOT EXISTS rendez_vous (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    structure_id INTEGER NOT NULL,
    date_rdv DATE,
    heure_rdv TIME,
    motif VARCHAR(100),
    statut VARCHAR(20) DEFAULT 'programme',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 8. TABLE USERS (utilisateurs de la structure)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    structure_id INTEGER NOT NULL,
    nom VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    mot_de_passe VARCHAR(255),
    role VARCHAR(20) DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Vérification
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';