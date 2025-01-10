import datetime
from typing import Annotated
from sqlalchemy import text
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON
from backend.database.database import Base


int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True, index=True)]
unique_str = Annotated[str, mapped_column(unique=True, index=True)]
optional_str = Annotated[str, mapped_column(default='')]
created_at = Annotated[
    datetime.datetime,
    mapped_column(server_default=text('CURRENT_TIMESTAMP'))
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text('CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP')
    )
]


class BaseModel(Base):
    __abstract__ = True

    # Default fields
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class User(BaseModel):
    __tablename__ = 'user'

    # Auth info
    email: Mapped[unique_str]
    hashed_password: Mapped[str]


class ProductType(Enum):
    # Instruments
    electric_guitar = 'electric-guitar'
    acoustic_guitar = 'acoustic-guitar'
    drum = 'drum'
    digital_piano = 'digital-piano'
    acoustic_piano = 'acoustic-piano'

    # Devices
    microphone = 'microphone'
    headphone = 'headphone'
    sound_system = 'sound-system'
    sound_card = 'sound-card'
    combo_amplifier = 'combo-amplifier'

    # Accessories
    mediator = 'mediator'
    string = 'string'
    drumstick = 'drumstick'
    cover = 'cover'
    chair = 'chair'


class Product(BaseModel):
    __tablename__ = 'product'

    # Main fields
    title: Mapped[unique_str]
    product_type: Mapped[ProductType]
    price: Mapped[int]
    description: Mapped[optional_str]
    image_url: Mapped[optional_str]
    quantity: Mapped[int] = mapped_column(nullable=True)
    characteristics: Mapped[dict] = mapped_column(type_=JSON, nullable=True)
