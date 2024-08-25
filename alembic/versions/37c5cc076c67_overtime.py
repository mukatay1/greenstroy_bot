"""overtime

Revision ID: 37c5cc076c67
Revises: 4dabd8bea9ee
Create Date: 2024-08-25 12:13:42.059959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '37c5cc076c67'
down_revision: Union[str, None] = '4dabd8bea9ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_attendances_id', table_name='attendances')
    op.drop_table('attendances')
    op.drop_index('ix_employees_fio', table_name='employees')
    op.drop_index('ix_employees_full_name', table_name='employees')
    op.drop_index('ix_employees_id', table_name='employees')
    op.drop_index('ix_employees_telegram_id', table_name='employees')
    op.drop_table('employees')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employees',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('employees_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('telegram_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('fio', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('full_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('city', postgresql.ENUM('ALMATY', 'ASTANA', name='city'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='employees_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_employees_telegram_id', 'employees', ['telegram_id'], unique=True)
    op.create_index('ix_employees_id', 'employees', ['id'], unique=False)
    op.create_index('ix_employees_full_name', 'employees', ['full_name'], unique=False)
    op.create_index('ix_employees_fio', 'employees', ['fio'], unique=False)
    op.create_table('attendances',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('employee_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('arrival_time', postgresql.TIME(), autoincrement=False, nullable=True),
    sa.Column('departure_time', postgresql.TIME(), autoincrement=False, nullable=True),
    sa.Column('late', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('departure_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('departure_reason', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('supervisor', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('departure_time_actual', postgresql.TIME(), autoincrement=False, nullable=True),
    sa.Column('return_time', postgresql.TIME(), autoincrement=False, nullable=True),
    sa.Column('check', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('skip_status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], name='attendances_employee_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='attendances_pkey')
    )
    op.create_index('ix_attendances_id', 'attendances', ['id'], unique=False)
    # ### end Alembic commands ###
