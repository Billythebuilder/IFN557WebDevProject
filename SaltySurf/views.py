from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Brand, Surfboard, Order
from datetime import datetime
from .forms import CheckoutForm
from . import db

main_bp = Blueprint('main', __name__)

# Homepage
@main_bp.route('/')
def index():
    brands = db.session.scalars(db.select(Brand).order_by(Brand.id))
    return render_template('index.html', brands=brands)

# View all surfboards
@main_bp.route('/surfboard/<int:brandid>')
def brandsurfboard(brandid):
    surfboard = db.session.scalars(db.select(Surfboard).where(Surfboard.brand_id==brandid))
    return render_template('brandsurfboard.html', surfboard=surfboard)

# Referred to as "Basket" to the user
@main_bp.route('/order', methods=['POST','GET'])
def order():
    surfboard_id = request.values.get('surfboard_id')
    print(f'Values: {surfboard_id}')
    # retrieve order if there is one
    if 'order_id'in session.keys():
        order = db.session.scalar(db.select(Order).where(Order.id==session['order_id']))
        # order will be None if order_id stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status = False, firstname='', surname='', email='', phone='', address='', totalcost=0, date=datetime.now())
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None
    
    # calcultate totalprice
    total_price = 0
    if order is not None:
        for surfboard in order.surfboard:
            total_price = total_price + surfboard.price
    
    # Are we adding an item?
    if surfboard_id is not None and order is not None:
        surfboard = db.session.scalar(db.select(Surfboard).where(Surfboard.id==surfboard_id))
        try:
            order.surfboard.append(surfboard)
            for surfboard in order.surfboard:
                total_price += surfboard.price
            order.total_cost = total_price
            db.session.commit()
        except:
            flash('There was an issue adding the item to your basket', category='danger')
        return redirect(url_for('main.order'))
    return render_template('order.html', order=order, total_price=total_price)

@main_bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id = request.form['id']
    print(f'Surfboard to delete ID is: {id}')
    if 'order_id' in session:
        order = db.session.scalar(db.select(Order).where(Order.id==session['order_id']))
        if not order:
            flash("There's no order to delete!")
            return redirect(request.referrer)
        print(order.surfboard)
        surfboard_to_delete = db.session.scalar(db.select(Surfboard).where(Surfboard.id==id))
        print(f'Deleting: {surfboard_to_delete.name}')
        try:
            surfboard_to_delete.qty = 0
            order.surfboard.remove(surfboard_to_delete)
            db.session.commit()
        except:
            print('Something went wrong when trying to delete the order')
        
    return redirect(url_for('main.order'))

# Empty basket
@main_bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        order = db.session.scalar(db.select(Order).where(Order.id==session['order_id']))
        for surfboard in surfboard.surfboard:
            order.surfboard.remove(surfboard)
        session.pop('order_id')
        db.session.commit()
        flash('Basket emptied!')
    else:
        flash("There's no order to delete!")
        return redirect(request.referrer)
    return redirect(url_for('main.index'))

# Complete the order
@main_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = db.session.scalar(db.select(Order).where(Order.id==session['order_id']))
        if not order.surfboard:
            flash('You need to add a surfboard to your basket first!')
            return(redirect(request.referrer))
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.address = form.address.data
            order.phone = form.phone.data
            totalcost = 0
            for surfboard in order.surfboard:
                totalcost = totalcost + surfboard.price
            order.totalcost = totalcost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you for your order! Tracking details were sent to the email address provided!')
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form=form)

# Search functionality
@main_bp.route("/search", methods=['GET','POST'])
def search():
    search = request.args.get('search')
    search = '%{}%'.format(search)
    surfboards = Surfboard.query.filter(Surfboard.description.like(search)).all()
    return render_template('brandsurfboard.html', surfboard=surfboards)