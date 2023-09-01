"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template,  redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "keyz"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.app_context().push()
connect_db(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create')
def new_cupcake():
    """New cupcake form"""
    return render_template('create-form.html')

@app.route('/update')
def edit_cupcake():
    """Update cupcake form"""
    return render_template('edit-form.html')

@app.route('/api/cupcakes')
def list_cupcakes():
    """Shows cupcake api"""
    all_cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcake/<int:id>')
def get_cupcake(id):
    """Shows specific cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.to_dict())


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Handles new cupcake form"""
    flavor = request.form["flavor"]
    size = request.form["size"]
    rating = request.form["rating"]
    image = request.form["image"] if request.form["image"] else None
    
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()
    reponse_json = jsonify(cupcake=new_cupcake.to_dict())
    # return (reponse_json, 201)
    return redirect('/')

# @app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
# def update_cupcake(cupcake_id):
#     """Updates cupcake"""

#     data = request.json()

#     cupcake = Cupcake.query.get_or_404(cupcake_id)

#     cupcake.flavor = data['flavor']
#     cupcake.rating = data['rating']
#     cupcake.size = data['size']
#     cupcake.image = data['image']

#     db.session.add(cupcake)
#     db.session.commit()

#     return jsonify(cupcake=cupcake.to_dict())
    
@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Delete cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")