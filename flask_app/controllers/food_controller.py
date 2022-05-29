from operator import methodcaller
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.food_model import Food
from flask_app.models.balance_model import Balance
import datetime

temp_foods = []


@app.route('/pantry')
def pantry():
    if 'user_id' not in session:
        flash('You must Log in or Register to use the Virtual Pantry.')
        return redirect('/')
    user = User.get_one({ 'id' : session['user_id']})
    all_foods = Food.get_all_foods({'user_id':session['user_id']})
    balance = Balance.get_balance({'user_id':session['user_id']})
    return render_template('pantry.html',all_foods=all_foods, user = user, balance=balance)

@app.route('/reset_balance/<int:id>')
def reset_balance(id):
    if 'user_id' not in session:
        flash('You must Log in or Register to use the Virtual Pantry.')
        return redirect('/')
    Balance.reset_balance({'user_id': id})
    return redirect('/pantry')

@app.route('/get_foods', methods=['POST'])
def get_foods():
    return redirect('/pantry')

@app.route('/add_food')
def add_food():
    if 'user_id' not in session:
        flash('You must Log in or Register to use the Virtual Pantry.')
        return redirect('/')
    foods = Food.get_temp_foods({'user_id':session['user_id']})
    return render_template('add_food.html', foods = foods)

@app.route('/add_new_food', methods=['POST'])
def add_new_food():
    print(request.form)
    if not Food.validate_new_food(request.form):
        return redirect('/add_food')
    Food.add_new_food(request.form)
    return redirect('/add_food')

@app.route('/edit_food/<int:id>')
def edit_food(id):
    if 'user_id' not in session:
        flash('You must Log in or Register to use the Virtual Pantry.')
        return redirect('/')
    one_food = Food.get_one_food({'id': id})
    return render_template('edit_entry.html', one_food = one_food)

@app.route('/submit_one_food/<int:id>', methods=['POST'])
def submit_one_food(id):
    if not Food.validate_new_food(request.form):
        return redirect(f'/edit_food/{id}')
    Food.edit_food(request.form)
    return redirect('/add_food')

@app.route('/delete_food/<int:id>')
def delete_food(id):
    if 'user_id' not in session:
        flash('You must Log in or Register to use the Virtual Pantry.')
        return redirect('/')  
    Food.delete_food({'id': id})
    return redirect('/add_food')

@app.route('/submit_food_list')
def submit_food_list():
    if 'user_id' not in session:
        flash('You must Log in or Register to use the Virtual Pantry.')
        return redirect('/')  
    Food.confirm_food_list({'user_id':session['user_id']})    
    return redirect('/pantry')

@app.route('/edit_pantry_food/<int:id>')
def edit_pantry_food(id):
    if 'user_id' not in session:
        flash('You must Log in or Register to use the Virtual Pantry.')
        return redirect('/')  
    one_food = Food.get_one_food({'id': id})
    return render_template('edit_food.html', one_food=one_food)

@app.route('/submit_pantry_food/<int:id>', methods=['POST'])
def submit_pantry_food(id):
    if not Food.validate_new_food(request.form):
        return redirect(f'/edit_pantry_food/{id}')
    Food.edit_pantry_food(request.form)
    return redirect('/pantry')

@app.route('/eat_food/<int:id>')
def eat_food(id):
    if 'user_id' not in session:
        flash('You must Log in or Register to use the Virtual Pantry.')
        return redirect('/')      
    item = Food.get_one_food({'id':id})
    if item.quant == 1:
        Food.delete_food({'id':id})
        return redirect('/pantry')
    total = item.quant
    return render_template('eat_food.html',total=total, item=item)
    
@app.route('/eat_all/<int:id>')
def eat_all(id):
    if 'user_id' not in session:
        flash('You must Log in or Register to use the Virtual Pantry.')
        return redirect('/') 
    Food.delete_food({'id':id})
    return redirect('/pantry')

@app.route('/eat_some/<int:id>', methods=['POST'])
def eat_some(id):
    print(request.form)
    user = User.get_one({'id':session['user_id']})
    price = int(request.form['price'])
    quant = int(request.form['quant'])
    eaten = int(request.form['num'])
    unit_price = price/quant
    left = quant-eaten
    prev = Balance.get_balance({'user_id': user.id })
    if int(request.form['num']) > 0:
        waste = unit_price * left
        waste += int(prev.balance)
        data = {
        'user_id':session['user_id'],
        'balance' : round(waste, 2)
        }
        print(data)
        Balance.add_waste(data)
        Food.delete_food({'id':id})
        return redirect('/pantry')
    if int(request.form['perc']) > 0:
        perc = int(request.form['perc'])
        waste = price * perc / 100 
        waste += int(prev.balance)
        data = {
            'user_id':session['user_id'],
            'balance' : round(waste, 2)
        }
        print(data)
        Balance.add_waste(data)
        Food.delete_food({'id':id})
        return redirect('/pantry')
    else:
        return redirect(f'/eat_food/{id}')


@app.route('/throw_out/<int:id>')
def throw_out(id):
    if 'user_id' not in session:
        flash('You must Log in or Register to use the Virtual Pantry.')
        return redirect('/') 
    food = Food.get_one_food({'id':id}) 
    prev = Balance.get_balance({'user_id':session['user_id']})
    balance = int(food.price) + int(prev.balance)
    data = {
        'user_id':session['user_id'],
        'balance': balance
    }
    Balance.add_waste(data)
    Food.delete_food({'id': id})
    return redirect('/pantry')