from flask import Flask, render_template, redirect, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
# from flask_wtf import FlaskForm
from forms import AddPetForm, EditPetForm
from models import db, Pet, connect_db


app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretpassword'

connect_db(app)
toolbar = DebugToolbarExtension(app)

@app.route('/')
def index():
    '''Renders homepage(index) and shows both available and not available pets'''
    available_pets = Pet.query.filter_by(available=True).all()

    no_longer_available_pets = Pet.query.filter_by(available=False).all()

    return render_template(
        'index.html',
        available_pets=available_pets,
        no_longer_available_pets=no_longer_available_pets
    )


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    '''renders the form for adding a pet and processes the submission'''
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        # Create a new pet object and add it to the database
        new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(new_pet)
        db.session.commit()

        #flash a success message
        flash('Pet added successfully!', 'success')

        return redirect(url_for('index'))

    return render_template('add_pet.html', form=form)


@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def pet_details(pet_id):
    '''renders pet details and the edit form for the given pet ID'''
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        form.populate_obj(pet)
        db.session.commit()

        flash('Pet updated successfully!', 'success')

        return redirect(url_for('index'))

    return render_template('pet_details.html', pet=pet, form=form)

if __name__ == '__main__':
    # Create the database tables before running the app
    db.create_all()
    app.run(debug=True)