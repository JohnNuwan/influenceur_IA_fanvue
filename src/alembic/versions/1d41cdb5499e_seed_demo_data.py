"""seed demo data

Revision ID: 1d41cdb5499e
Revises: 90df222141fe
Create Date: 2025-08-09 12:17:50.059592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d41cdb5499e'
down_revision = '90df222141fe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    # Utilisateur admin démo (id auto)
    sql_user = sa.text(
        """
        INSERT INTO users (email, username, hashed_password, is_active, is_verified, role)
        SELECT :email, :username, :hashed_password, TRUE, TRUE, :role
        WHERE NOT EXISTS (
            SELECT 1 FROM users WHERE email = :email
        );
        """
    )
    bind.execute(
        sql_user,
        {
            "email": "admin@influenceur-ia.com",
            "username": "admin",
            "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.gS.6.m",
            "role": "admin",
        },
    )

    # Influenceuse demo (liée à admin)
    sql_influenceuse = sa.text(
        """
        WITH u AS (
            SELECT id FROM users WHERE email = 'admin@influenceur-ia.com'
        )
        INSERT INTO influenceuses (
            user_id, stage_name, bio, followers_count, posts_count, is_active
        )
        SELECT u.id, 'Demo Influenceuse', 'Profil démo', 1000, 1, true FROM u
        WHERE NOT EXISTS (
            SELECT 1 FROM influenceuses i WHERE i.user_id = u.id
        );
        """
    )
    bind.execute(sql_influenceuse)

    # Contenu démo
    sql_content = sa.text(
        """
        WITH i AS (
            SELECT id FROM influenceuses ORDER BY id LIMIT 1
        )
        INSERT INTO content (
            influenceuse_id, title, description, content_type, status, is_public
        )
        SELECT i.id, 'Bienvenue', 'Contenu de démo', 'text', 'published', true FROM i
        WHERE NOT EXISTS (
            SELECT 1 FROM content c WHERE c.title = 'Bienvenue'
        );
        """
    )
    bind.execute(sql_content)


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM content WHERE title = 'Bienvenue'"))
    op.execute(sa.text("DELETE FROM influenceuses WHERE stage_name = 'Demo Influenceuse'"))
    op.execute(sa.text("DELETE FROM users WHERE email = 'admin@influenceur-ia.com'"))


