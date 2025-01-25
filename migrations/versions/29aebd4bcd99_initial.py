"""init_dev

Revision ID: 29aebd4bcd99
Revises: 
Create Date: 2025-01-24 10:52:05.462266

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '29aebd4bcd99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.Column('disabled', sa.Boolean(), nullable=False, default=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('users')
