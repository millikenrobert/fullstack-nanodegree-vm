import os
import sys

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Restaurant, MenuItem

##insert at the end
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)

session = DBSession()

myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

session.query(Restaurant).all()

cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made will natural ingredients and fresh mozza", course = "Entree", price = "$8.99",  restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()

items = session.query(Restaurant).all()
for item in items:
	print item.name


veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')

for veggieBurger in veggieBurgers:
	print veggieBurger.id
	print veggieBurger.price
	print veggieBurger.restaurant.name
	print "\n"


urbanVeggieBurgers = session.query(MenuItem).filter_by(id = 10).one()

urbanVeggieBurgers.price = '$2.99'
session.add(urbanVeggieBurgers)
session.commit()



for veggieBurger in veggieBurgers:
	veggieBurger.price = '$2.99'
	session.add(urbanVeggieBurgers)
	session.commit()


spinichIceCream = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
session.delete(spinichIceCream)
session.commit()
