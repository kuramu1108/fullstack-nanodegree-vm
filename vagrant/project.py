from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# JSON API endpoint route
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
	return jsonify(MenuItem=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def restaurantMenuItemJSON(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id)
	item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
	return jsonify(MenuItem=item.serialize)

@app.route('/')

@app.route('/restaurants/<int:restaurant_id>/')
def listMenuItems(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	
	return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash("new menu item created")
		return redirect(url_for('listMenuItems', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			item.name = request.form['name']
		if request.form['description']:
			item.description = request.form['description']
		if request.form['price']:
			item.price = request.form['price']
		if request.form['course']:
			item.course = request.form['course']
		session.add(item)
		session.commit()
		flash("menu item editted")
		return redirect(url_for('listMenuItems', restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html', item=item)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		flash("menu item deleted")
		return redirect(url_for('listMenuItems', restaurant_id=restaurant_id))
	else:
		return render_template('deletemenuitem.html', item=item)
		
if __name__ == '__main__':
	app.secret_key = 'something'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)