from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
worklog = Table('worklog', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('task_id', Integer),
    Column('timestamp', DateTime),
    Column('duration', Integer),
)

task = Table('task', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('task_name', String),
    Column('timestamp', DateTime),
    Column('duration', Integer),
    Column('user_id', Integer),
)

task = Table('task', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('task_name', String(length=64)),
    Column('creation_date', DateTime),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['worklog'].create()
    pre_meta.tables['task'].columns['duration'].drop()
    pre_meta.tables['task'].columns['timestamp'].drop()
    post_meta.tables['task'].columns['creation_date'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['worklog'].drop()
    pre_meta.tables['task'].columns['duration'].create()
    pre_meta.tables['task'].columns['timestamp'].create()
    post_meta.tables['task'].columns['creation_date'].drop()
