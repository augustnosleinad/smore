from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
)

task = Table('task', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('task_name', String(length=64)),
    Column('timestamp', DateTime),
    Column('duration', Integer),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].create()
    post_meta.tables['task'].columns['timestamp'].create()
    post_meta.tables['task'].columns['user_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].drop()
    post_meta.tables['task'].columns['timestamp'].drop()
    post_meta.tables['task'].columns['user_id'].drop()
