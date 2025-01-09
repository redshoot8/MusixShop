import datetime
from typing import Annotated
from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
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


class M2MUserManga(BaseModel):
    __tablename__ = 'm2m_user_manga'

    id_user: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    id_manga: Mapped[int] = mapped_column(ForeignKey('manga.id'), nullable=False)
    last_read_chapter: Mapped[int] = mapped_column(ForeignKey('manga_chapter.id'), nullable=False)


class M2MMangaGenre(BaseModel):
    __tablename__ = 'm2m_manga_genre'

    id_manga: Mapped[int] = mapped_column(ForeignKey('manga.id'), nullable=False)
    id_genre: Mapped[int] = mapped_column(ForeignKey('genre.id'), nullable=False)


class User(BaseModel):
    __tablename__ = 'user'

    # Auth info
    username: Mapped[unique_str]
    hashed_password: Mapped[str]

    # Main fields
    description: Mapped[optional_str]


class Manga(BaseModel):
    __tablename__ = 'manga'

    # Main fields
    title: Mapped[unique_str]
    description: Mapped[optional_str]


class MangaChapter(BaseModel):
    __tablename__ = 'manga_chapter'

    # Main fields
    id_manga: Mapped[int] = mapped_column(ForeignKey('manga.id'), nullable=False)
    number: Mapped[int]
    title: Mapped[str]


class MangaPage(BaseModel):
    __tablename__ = 'manga_page'

    # Main fields
    id_chapter: Mapped[int] = mapped_column(ForeignKey('manga_chapter.id'), nullable=False)
    number: Mapped[int]
    image: Mapped[unique_str]


class Genre(BaseModel):
    __tablename__ = 'genre'

    # Main fields
    name: Mapped[unique_str]
