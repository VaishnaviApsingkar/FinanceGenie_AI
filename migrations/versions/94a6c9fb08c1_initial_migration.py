"""Initial migration

Revision ID: 94a6c9fb08c1
Revises: 3dc08707d629
Create Date: 2024-12-26 19:42:06.181311

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '94a6c9fb08c1'
down_revision = '3dc08707d629'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chase_transactions')
    op.drop_table('axis_transactions')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('axis_transactions',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('bank_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('transaction_date', sa.DATE(), nullable=False),
    sa.Column('amount', mysql.FLOAT(), nullable=False),
    sa.Column('transaction_id', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('type', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('transaction_name', mysql.VARCHAR(length=255), nullable=False),
    sa.ForeignKeyConstraint(['bank_id'], ['bank_account.id'], name='axis_transactions_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('chase_transactions',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('bank_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('transaction_date', sa.DATE(), nullable=False),
    sa.Column('amount', mysql.FLOAT(), nullable=False),
    sa.Column('transaction_id', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('type', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('transaction_name', mysql.VARCHAR(length=255), nullable=False),
    sa.ForeignKeyConstraint(['bank_id'], ['bank_account.id'], name='chase_transactions_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
