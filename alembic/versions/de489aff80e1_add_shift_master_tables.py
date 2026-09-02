"""add shift master tables

Revision ID: de489aff80e1
Revises: 9b57d84ef539
Create Date: 2026-09-01 13:30:24.583049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de489aff80e1'
down_revision: Union[str, Sequence[str], None] = '9b57d84ef539'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Buat tabel master shift harian
    op.create_table('ttamshiftdaily',
        sa.Column('shiftdailycode', sa.String(length=50), nullable=False),
        sa.Column('starttime', sa.DateTime(), nullable=True),
        sa.Column('endtime', sa.DateTime(), nullable=True),
        sa.Column('productivehours', sa.Integer(), nullable=False),
        sa.Column('daytype', sa.String(length=5), nullable=False),
        sa.Column('remark', sa.String(length=255), nullable=True),
        sa.Column('color', sa.String(length=60), nullable=True),
        sa.Column('is_active', sa.SmallInteger(), nullable=False),
        sa.Column('created_by', sa.String(length=50), nullable=False),
        sa.Column('created_date', sa.DateTime(), nullable=False),
        sa.Column('modified_by', sa.String(length=50), nullable=False),
        sa.Column('modified_date', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('shiftdailycode')
    )
    
    # 2. Buat tabel mapping shift karyawan
    op.create_table('ttadempshif',
        sa.Column('shiftcode', sa.String(length=50), nullable=False),
        sa.Column('emp_id', sa.Integer(), nullable=False),
        sa.Column('shiftdailycode', sa.String(length=50), nullable=False),
        sa.Column('created_by', sa.String(length=50), nullable=False),
        sa.Column('created_date', sa.DateTime(), nullable=False),
        sa.Column('modified_by', sa.String(length=50), nullable=False),
        sa.Column('modified_date', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['emp_id'], ['employees.id'], ),
        sa.ForeignKeyConstraint(['shiftdailycode'], ['ttamshiftdaily.shiftdailycode'], ),
        sa.PrimaryKeyConstraint('shiftcode', 'emp_id')
    )
    op.create_index(op.f('ix_ttadempshif_emp_id'), 'ttadempshif', ['emp_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Hapus dalam urutan terbalik dari pembuatan (child dulu baru parent)
    op.drop_index(op.f('ix_ttadempshif_emp_id'), table_name='ttadempshif')
    op.drop_table('ttadempshif')
    op.drop_table('ttamshiftdaily')