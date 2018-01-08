from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Fake Restaurants


def getRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return restaurant


def getMenuItems(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return items


def getItem(menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return item


# show restaurants
@app.route('/restaurant/')
@app.route('/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurant.html', restaurants=restaurants)

# add new restaurant


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():

    if request.method == 'POST':
        newRestaurantAdded = Restaurant(name=request.form['name'])
        session.add(newRestaurantAdded)
        session.commit()
        flash("New Restaurant Created")

        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


# edit restaurant


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = getRestaurant(restaurant_id)

    if request.method == 'POST':
        editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        flash("Restaurant Successfully Edited")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editRestaurant.html', restaurant=editedRestaurant)


# delete restaurant


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant = getRestaurant(restaurant_id)
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        flash("Restaurant Successfully Deleted")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant=deletedRestaurant)


# show menu
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):

    return render_template('menu.html', restaurant=getRestaurant(restaurant_id), items=getMenuItems(restaurant_id))

# new menu itemss


@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):

    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        flash("New Menu Item Created")
        session.commit()

        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)


# edit menu item


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editItem = getItem(menu_id)
    if request.method == 'POST':
        editItem.name = request.form['name']
        session.add(editItem)
        session.commit()
        flash("Menu Item Successfully Edited")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', item=editItem, restaurant_id=restaurant_id)

# delete menu item


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = getItem(menu_id)
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("Menu Item Successfully Deleted")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', deletedItem=deletedItem)


@app.route('/restaurant/JSON')
def restaurantJSON():
    restaurants = session.query(Restaurant)
    return jsonify(Restaurant=[r.serialize for r in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuJSONID(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(id=menu_id)
    return jsonify(MenuItems=[i.serialize for i in items])


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
