from sqlalchemy import String, Integer, Column, ForeignKey
from Users.UserModel import User

from base import Base

class ProviderCategories(Base):
    __tablename__ = "provider_categories"
    category_id = Column("category_id",Integer,primary_key =True,autoincrement=True)
    user_id = Column("user_id",Integer,ForeignKey(User.user_id),nullable=False)
    main_categories = Column("main_categories",String(255),nullable=False)
    sub_categories = Column("sub_categories",String(255),nullable=False)
    subcategories_description = Column("subcategories_description",String(255),nullable=False)
    subcategory_image = Column("subcategory_image",String(255),nullable=True)
    number_of_visits = Column("number_of_visits", Integer, nullable=True)

# users = relationship("Users", uselist=False, back_populates="users")
