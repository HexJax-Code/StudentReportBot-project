"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2025-11-25 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # students
    op.create_table(
        'students',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.String(length=64), nullable=False),
        sa.Column('full_name', sa.String(length=256), nullable=False),
        sa.Column('phone', sa.String(length=64), nullable=False),
        sa.Column('guardian_name', sa.String(length=256), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index(op.f('ix_students_student_id'), 'students', ['student_id'], unique=True)

    # reports
    op.create_table(
        'reports',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('students.id', ondelete='CASCADE'), nullable=False),
        sa.Column('report_url', sa.String(length=1024), nullable=False),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )

    # send_jobs
    op.create_table(
        'send_jobs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('report_id', sa.Integer(), sa.ForeignKey('reports.id', ondelete='CASCADE'), nullable=False),
        sa.Column('phone', sa.String(length=64), nullable=False),
        sa.Column('attempt_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('last_error', sa.Text(), nullable=True),
        sa.Column('scheduled_for', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )

def downgrade():
    op.drop_table('send_jobs')
    op.drop_table('reports')
    op.drop_table('students')
