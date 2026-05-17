from sqlalchemy import Column, Integer, String, Text

from database.db import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)

    content = Column(Text)

    file_type = Column(String)

    source_name = Column(String)