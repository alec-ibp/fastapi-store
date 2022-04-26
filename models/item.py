import sqlalchemy

from db.init_db import metadata
from models.enums import ItemState

item = sqlalchemy.Table(
    "items",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("title", sqlalchemy.String(120), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("photo_url", sqlalchemy.String(320), nullable=False),
    sqlalchemy.Column("amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime,
                      server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("status", sqlalchemy.Enum(ItemState),
                      server_default=ItemState.pendding.name),
    sqlalchemy.Column("seller_id", sqlalchemy.ForeignKey(
        "users.id"), nullable=False)
)
