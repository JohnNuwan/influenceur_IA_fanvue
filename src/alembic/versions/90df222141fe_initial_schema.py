"""initial schema

Revision ID: 90df222141fe
Revises: 
Create Date: 2025-08-09 08:19:32.972648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90df222141fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Remarque: on utilise des ENUM non-natifs (native_enum=False) pour éviter les conflits CREATE TYPE

    # users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column('username', sa.String(length=100), nullable=False, unique=True, index=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255)),
        sa.Column('role', sa.Enum('admin', 'manager', 'influenceuse', 'support', name='userrole', native_enum=False), nullable=False, server_default='influenceuse'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('avatar_url', sa.String(length=500)),
        sa.Column('bio', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.Column('last_login', sa.DateTime(timezone=True)),
    )
    # Indexes pour users déjà gérés par index=True/unique=True sur les colonnes à la création de la table

    # influenceuses
    op.create_table(
        'influenceuses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('stage_name', sa.String(length=255), nullable=False),
        sa.Column('bio', sa.Text()),
        sa.Column('avatar_url', sa.String(length=500)),
        sa.Column('cover_image_url', sa.String(length=500)),
        sa.Column('followers_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('following_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('posts_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('content_categories', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('content_style', sa.String(length=100)),
        sa.Column('subscription_price', sa.Float(), nullable=False, server_default='0'),
        sa.Column('tips_enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('custom_content_enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('is_featured', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('auto_posting_enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('chatbot_enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('analytics_enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.Column('last_activity', sa.DateTime(timezone=True)),
    )
    # Index par défaut sur id déjà existant

    # content
    op.create_table(
        'content',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('influenceuse_id', sa.Integer(), sa.ForeignKey('influenceuses.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255)),
        sa.Column('description', sa.Text()),
        sa.Column('content_type', sa.Enum('image', 'video', 'text', 'audio', name='contenttype', native_enum=False), nullable=False),
        sa.Column('status', sa.Enum('draft', 'generated', 'published', 'archived', 'failed', name='contentstatus', native_enum=False), nullable=False, server_default='draft'),
        sa.Column('file_url', sa.String(length=500)),
        sa.Column('file_size', sa.Integer()),
        sa.Column('file_format', sa.String(length=50)),
        sa.Column('thumbnail_url', sa.String(length=500)),
        sa.Column('prompt', sa.Text()),
        sa.Column('ai_model', sa.String(length=100)),
        sa.Column('generation_params', sa.JSON()),
        sa.Column('generation_time', sa.Integer()),
        sa.Column('categories', sa.JSON(), server_default='[]'),
        sa.Column('tags', sa.JSON(), server_default='[]'),
        sa.Column('width', sa.Integer()),
        sa.Column('height', sa.Integer()),
        sa.Column('duration', sa.Integer()),
        sa.Column('is_public', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('is_featured', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('published_at', sa.DateTime(timezone=True)),
        sa.Column('views_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('likes_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('shares_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )
    # Index par défaut sur id déjà existant

    # conversations
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('influenceuse_id', sa.Integer(), sa.ForeignKey('influenceuses.id', ondelete='CASCADE'), nullable=False),
        sa.Column('platform', sa.String(length=100)),
        sa.Column('platform_conversation_id', sa.String(length=255)),
        sa.Column('status', sa.Enum('active', 'paused', 'closed', 'archived', name='conversationstatus', native_enum=False), nullable=False, server_default='active'),
        sa.Column('chatbot_enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('auto_reply_enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('ollama_model', sa.String(length=100), nullable=False, server_default='llama2:7b'),
        sa.Column('conversation_history', sa.JSON(), server_default='[]'),
        sa.Column('last_message_at', sa.DateTime(timezone=True)),
        sa.Column('message_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('response_time_avg', sa.Integer()),
        sa.Column('satisfaction_score', sa.Integer()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )
    # Index par défaut sur id déjà existant

    # messages
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('conversation_id', sa.Integer(), sa.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('message_type', sa.String(length=50)),
        sa.Column('sender_type', sa.String(length=50)),
        sa.Column('platform_message_id', sa.String(length=255)),
        sa.Column('platform_timestamp', sa.DateTime(timezone=True)),
        sa.Column('is_ai_generated', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('ai_model', sa.String(length=100)),
        sa.Column('ai_confidence', sa.Integer()),
        sa.Column('metadata_json', sa.JSON()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )
    op.create_index('ix_messages_id', 'messages', ['id'])


def downgrade() -> None:
    op.drop_index('ix_messages_id', table_name='messages')
    op.drop_table('messages')
    op.drop_index('ix_conversations_id', table_name='conversations')
    op.drop_table('conversations')
    op.drop_index('ix_content_id', table_name='content')
    op.drop_table('content')
    op.drop_index('ix_influenceuses_id', table_name='influenceuses')
    op.drop_table('influenceuses')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')

    # Aucun type ENUM natif à supprimer (native_enum=False)


