-- Script d'initialisation minimal (extensions seulement)
-- Évite les conflits avec Alembic et les modèles Python

-- Extensions utiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Note: Le seeding et la création de tables sont gérés par Alembic
DO $$
BEGIN
    RAISE NOTICE 'Extensions PostgreSQL initialisées (uuid-ossp, pg_trgm).';
    RAISE NOTICE 'Les tables et données de démonstration seront créées via Alembic.';
END $$;
