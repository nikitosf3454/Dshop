from flask import Flask, render_template, request, redirect, url_for, abort, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Used for session security
from models import Drone, Motor, Vote, Rating
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drone_shop.db'  # Use SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy()  # Create SQLAlchemy instance
db.init_app(app)   # Bind app to db instance
migrate = Migrate(app, db)
# Sample data for drones
drones = [
    {
        "id": 1,
        "name": "Axisflying Manta 5 SE",
        "frame": "Axisflying Manta 5 SE frame",
        "wheelbase_size": "223mm",
        "weight": "362g (Analog) / 391g (Vista)",
        "top_plate_thickness": "2mm",
        "center_plate_thickness": "3mm",
        "bottom_plate_thickness": "3mm",
        "arm_thickness": "5.5mm",
        "flight_controller": "Axisflying Argus ECO FC F405",
        "image_url": "https://www.studiosport.fr/upload/image/drone-manta5-se-dji-o3-6s---axisflying-p-image-267534-grande.jpg",
        "price": 299,
        "description": "High-performance drone with robust features.",
        "votes": 0,
    },
    {
        "id": 2,
        "name": "DJI FPV Combo",
        "frame": "DJI FPV Frame",
        "wheelbase_size": "245mm",
        "weight": "795g",
        "top_plate_thickness": "3mm",
        "center_plate_thickness": "4mm",
        "bottom_plate_thickness": "4mm",
        "arm_thickness": "6mm",
        "flight_controller": "DJI Flight Controller",
        "image_url": "https://www.flyingeye.fr/wp-content/uploads/2021/03/DJI-FPV-Combo-MA3.jpg",
        "price": 1299,
        "description": "Immersive flight experience with incredible stability.",
        "votes": 0,
    },
    {
        "id": 3,
        "name": "iFlight Nazgul5 V2",
        "frame": "iFlight Nazgul Frame",
        "wheelbase_size": "210mm",
        "weight": "360g",
        "top_plate_thickness": "2mm",
        "center_plate_thickness": "2.5mm",
        "bottom_plate_thickness": "3mm",
        "arm_thickness": "5mm",
        "flight_controller": "iFlight SucceX-E F7",
        "image_url": "https://www.lacameraembarquee.fr/59805-large_default/drone-iflight-nazgul5-v3-dji-o3-6s-hd.jpg",
        "price": 249,
        "description": "Compact and powerful drone for freestyle pilots.",
        "votes": 0,
    },
    {
        "id": 4,
        "name": "GEPRC CineLog 35",
        "frame": "GEPRC CineLog Frame",
        "wheelbase_size": "150mm",
        "weight": "310g",
        "top_plate_thickness": "1.5mm",
        "center_plate_thickness": "2mm",
        "bottom_plate_thickness": "2.5mm",
        "arm_thickness": "4mm",
        "flight_controller": "GEPRC GEP F4-35A",
        "image_url": "https://www.drone-fpv-racer.com/56610-large_default/cinelog35-v2-6s-dji-o3-hd-bnf-crossfire-gps-geprc.jpg",
        "price": 399,
        "description": "Smooth cinematic performance for FPV filming.",
        "votes": 0,
    },
    {
        "id": 5,
        "name": "BetaFPV Pavo30",
        "frame": "BetaFPV Pavo30 Frame",
        "wheelbase_size": "120mm",
        "weight": "284g",
        "top_plate_thickness": "1.5mm",
        "center_plate_thickness": "2mm",
        "bottom_plate_thickness": "2mm",
        "arm_thickness": "3.5mm",
        "flight_controller": "BetaFPV F4 20A AIO",
        "image_url": "https://www.helicomicro.com/wp-content/uploads/2021/04/betafpv-pavo30-00.jpg",
        "price": 349,
        "description": "Compact cinewhoop drone for indoor and outdoor cinematic flights.",
        "votes": 0,
    },
    {
        "id": 6,
        "name": "EMAX Tinyhawk 2",
        "frame": "EMAX Tinyhawk 2 Frame",
        "wheelbase_size": "75mm",
        "weight": "54g",
        "top_plate_thickness": "1mm",
        "center_plate_thickness": "1.5mm",
        "bottom_plate_thickness": "2mm",
        "arm_thickness": "2mm",
        "flight_controller": "EMAX F3 AIO",
        "price": 129,
        "description": "Great beginner drone for indoor and outdoor flying.",
        "image_url": "https://www.helicomicro.com/wp-content/uploads/2020/03/emax-tinyhawk-2-race-00.jpg",
        "votes": 0,
    },
    {
        "id": 7,
        "name": "Autel Robotics EVO II",
        "frame": "Autel EVO II Frame",
        "wheelbase_size": "210mm",
        "weight": "1150g",
        "top_plate_thickness": "3mm",
        "center_plate_thickness": "4mm",
        "bottom_plate_thickness": "4mm",
        "arm_thickness": "5mm",
        "flight_controller": "Autel EVO II AIO",
        "price": 1499,
        "description": "High-performance drone with a 6K camera.",
        "image_url": "https://www.drone-store.fr/img/evo2-test5.png",
        "votes": 0,
    },
    {
        "id": 8,
        "name": "Holybro Kopis 2 HD",
        "frame": "Holybro Kopis 2 Frame",
        "wheelbase_size": "220mm",
        "weight": "470g",
        "top_plate_thickness": "2mm",
        "center_plate_thickness": "3mm",
        "bottom_plate_thickness": "3mm",
        "arm_thickness": "4mm",
        "flight_controller": "Holybro Kakute F7",
        "price": 499,
        "description": "HD FPV racing drone with carbon fiber frame.",
        "image_url": "https://www.helicomicro.com/wp-content/uploads/2019/11/kopis-2-hdv-fpv-racing-drone-air-unit-not-included-p-image-214185-grande.jpg",
        "votes": 0,
    },
    {
        "id": 9,
        "name": "iFlight Nazgul5 V2",
        "frame": "iFlight Nazgul5 V2 Frame",
        "wheelbase_size": "220mm",
        "weight": "440g",
        "top_plate_thickness": "2mm",
        "center_plate_thickness": "2mm",
        "bottom_plate_thickness": "2mm",
        "arm_thickness": "4mm",
        "flight_controller": "iFlight SucceX F7",
        "price": 419,
        "description": "High-end drone for racing and freestyle flights.",
        "image_url": "https://ae01.alicdn.com/kf/S89b7a3cdcacf4690bc58ec4db2dd5487q/IFlight-Nazgul5-V3-BLITZ-F7-BLHELIS-45A-1-6W-VTX-RaceCam-R1-XING-E-PRO-2207.jpg",
        "votes": 0,
    }
]

# List of FPV Motors with Characteristics
fpv_motors = [
    {
        "motor_id": 1,
        "motor_name": "T-Motor F40 Pro IV",
        "kv_rating": 2400,
        "stator_size": "2306",
        "motor_weight": "29.5g",
        "max_thrust": "1650g",
        "voltage": "3S-6S",
        "motor_price": 27.99,
        "motor_description": "High-performance motor designed for racing and freestyle drones.",
        "motor_image_url": "https://store.hexadrone.fr/8026-large_default/moteur-f40-pro-iv-1950-kv-t-motor.jpg",
        "votes": 0,
    },
    {
        "motor_id": 2,
        "motor_name": "iFlight XING-E Pro 2207",
        "kv_rating": 1800,
        "stator_size": "2207",
        "motor_weight": "32g",
        "max_thrust": "1650g",
        "voltage": "4S-6S",
        "motor_price": 24.99,
        "motor_description": "Durable and reliable motor for freestyle and racing.",
        "motor_image_url": "https://www.lacameraembarquee.fr/78513-large_default/moteur-iflight-xing-e-pro-2207-1800kv.jpg",
        "votes": 0,
    },
    {
        "motor_id": 3,
        "motor_name": "EMAX ECO II 2306",
        "kv_rating": 1900,
        "stator_size": "2306",
        "motor_weight": "29g",
        "max_thrust": "1450g",
        "voltage": "4S-6S",
        "motor_price": 14.99,
        "motor_description": "Budget-friendly motor with excellent efficiency and performance.",
        "motor_image_url": "https://n-factory.de/media/image/product/5037/lg/emax-eco-ii-series-2306-1900kv-motor.jpg",
        "votes": 0,
    },
    {
        "motor_id": 4,
        "motor_name": "BrotherHobby Avenger V3 2507",
        "kv_rating": 1750,
        "stator_size": "2507",
        "motor_weight": "37g",
        "max_thrust": "2000g",
        "voltage": "6S",
        "motor_price": 32.99,
        "motor_description": "Premium motor for long-range and cinematic builds.",
        "motor_image_url": "https://www.studiosport.fr/upload/image/moteur-avenger-v2-2507-1850-kv---brother-hobby-p-image-233585-moyenne.jpg",
        "votes": 0,
    },
    {
        "motor_id": 5,
        "motor_name": "RCINPower GTS V3 2207",
        "kv_rating": 1950,
        "stator_size": "2207",
        "motor_weight": "31.5g",
        "max_thrust": "1680g",
        "voltage": "4S-6S",
        "motor_price": 29.99,
        "motor_description": "Versatile motor for high-performance FPV builds.",
        "motor_image_url": "https://www.kiwiquads.co.nz/wp-content/uploads/RCINPower-GTS-V3-1804-2450KV-345.jpg",
        "votes": 0,
    }
]




# Database models
class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Assuming user_id is provided
    items = db.relationship('CartItem', backref='cart', lazy=True)

class CartItem(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


class User(db.Model):
    __tablename__ = 'users'  # Explicitly defining the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


# Initialize the database
with app.app_context():
    db.create_all()



@app.route('/add_to_cart/<string:product_type>/<int:product_id>', methods=['GET'])
def add_to_cart(product_type, product_id):
    # Find the product by id based on its type
    product = None
    if product_type == 'drone':
        product = next((item for item in drones if item['id'] == product_id), None)
    elif product_type == 'motor':
        product = next((item for item in fpv_motors if item['motor_id'] == product_id), None)

    if product:
        # Initialize the cart in the session if it doesn't exist
        if 'cart' not in session:
            session['cart'] = []

        # Check if the product is already in the cart
        found = False
        for item in session['cart']:
            if item['id'] == product_id and item['type'] == product_type:
                found = True
                break

        # Add product to cart if it's not already there
        if not found:
            # Add product to cart if it's not already there
            if product_type == 'drone':
                session['cart'].append({
                    'type': 'drone',  # Type for differentiation
                    'id': product['id'],
                    'name': product['name'],
                    'price': product['price'],
                    'image_url': product['image_url'],
                    'frame': product['frame'],  # Specific to drones
                    'wheelbase_size': product['wheelbase_size'],  # Specific to drones
                    'description': product['description'],  # Specific to drones
                    'flight_controller': product['flight_controller'],  # Specific to drones
                })
            elif product_type == 'motor':
                session['cart'].append({
                    'type': 'motor',  # Type for differentiation
                    'id': product['motor_id'],
                    'name': product['motor_name'],
                    'price': product['motor_price'],
                    'image_url': product['motor_image_url'],
                    'kv': product['kv_rating'],  # Specific to motors
                    'weight': product['motor_weight'],  # Specific to motors
                    'description': product['motor_description'],  # Specific to motors
                })

        # Mark the session as modified to ensure the data is saved
        session.modified = True

    # Redirect to the cart page after adding the product
    return redirect(url_for('view_cart'))



@app.route('/view_cart')
def view_cart():
    # If the cart is empty, inform the user
    if 'cart' not in session or len(session['cart']) == 0:
        return "Your cart is empty."

    # Calculate the total price for the cart
    total_price = sum(item['price'] for item in session['cart'])

    return render_template('view_cart.html', cart=session['cart'], total_price=total_price)


# Remove product from cart
@app.route('/remove_from_cart/<int:product_id>', methods=['GET'])
def remove_from_cart(product_id):
    # Check if the cart exists in the session
    if 'cart' in session:
        # Remove the item with the given product_id
        session['cart'] = [item for item in session['cart'] if item['id'] != product_id]
        # Mark the session as modified to save the changes
        session.modified = True

    # Redirect to the cart page after removing the item
    return redirect(url_for('view_cart'))


# Home page (view drones)
@app.route('/')  # Changing the endpoint name here to avoid conflict
def index():
    return render_template('index.html', drones=drones)

# Quick view page for a drone
@app.route('/quick_view/drone/<int:drone_id>', endpoint='quick_view_drone')
def quick_view_drone(drone_id):
    drone = next((item for item in drones if item['id'] == drone_id), None)
    if not drone:
        abort(404, description="Drone not found")
    return render_template('drone_view.html', drone=drone)

# Detailed view page for a drone
@app.route('/drone/<int:drone_id>', methods=['GET'], endpoint='view_drone')
def view_drone(drone_id):
    drone = next((item for item in drones if item['id'] == drone_id), None)
    if not drone:
        abort(404, description="Drone not found")
    return render_template('drone_view.html', drone=drone)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Check if the cart exists in the session
    if 'cart' not in session or len(session['cart']) == 0:
        return redirect(url_for('index'))  # Redirect to the homepage if the cart is empty

    # Get the cart and calculate the total price
    cart = session['cart']
    total_price = sum(item['price'] for item in cart)

    # Handle form submission for payment
    if request.method == 'POST':
        full_name = request.form['full_name']
        address = request.form['address']
        email = request.form['email']
        payment_method = request.form['payment_method']
        card_number = request.form['card_number']
        expiration_date = request.form['expiration_date']
        cvv = request.form['cvv']

        # You would normally process the payment here using a payment gateway (e.g., Stripe, PayPal, etc.)

        # After successful payment, redirect to confirmation page with details
        return render_template('payment_confirmation.html', full_name=full_name,
                               address=address, email=email, payment_method=payment_method,
                               card_number=card_number, expiration_date=expiration_date, cvv=cvv)

    # Render checkout page with the cart and total price if it's a GET request
    return render_template('checkout.html', cart=cart, total_price=total_price)



@app.route('/checkout-confirmation', methods=['POST'])
def checkout_confirmation():
    cart = session['cart']
    # Get the form data
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    email = request.form['email']
    address = request.form['address']
    city = request.form['city']
    country = request.form['country']
    items = cart  # Items that were purchased (this can be dynamic based on cart)

    # Here you could process the payment, send emails, save to database, etc.

    # Render the confirmation page with order details
    return render_template('checkout-confirmation.html', first_name=first_name, last_name=last_name,
                           email=email, address=address, city=city, country=country, items=items, total_price=sum(item['price'] for item in items))




@app.route('/buy_now/<int:product_id>', defaults={'product_type': 'drone'}, methods=['GET'])
@app.route('/buy_now/<string:product_type>/<int:product_id>', methods=['GET'])
def buy_now(product_type, product_id):
    # Find the product by id based on its type
    product = None
    if product_type == 'drone':
        product = next((item for item in drones if item['id'] == product_id), None)
    elif product_type == 'motor':
        product = next((item for item in fpv_motors if item['motor_id'] == product_id), None)

    if product:
        # Initialize the cart if it doesn't exist
        if 'cart' not in session:
            session['cart'] = []

        # Add the product to the cart (since Buy Now is like Add to Cart, but immediate checkout)
        session['cart'] = [{
            'type': product_type,
            'id': product['id'] if product_type == 'drone' else product['motor_id'],
            'name': product['name'] if product_type == 'drone' else product['motor_name'],
            'price': product['price'] if product_type == 'drone' else product['motor_price'],
            'image_url': product['image_url'] if product_type == 'drone' else product['motor_image_url']
        }]
        session.modified = True

        # Redirect to the checkout page
        return redirect(url_for('checkout'))

    else:
        # If the product doesn't exist
        abort(404, description="Product not found")



@app.route('/process_payment', methods=['GET'])
def process_payment():
    # Assuming payment is successful (in a real case, you would interact with a payment gateway)

    # Clear the cart from the session after successful payment
    session.pop('cart', None)
    session.modified = True

    # Redirect to the order confirmation page
    return redirect(url_for('payment_confirmation'))

@app.route('/payment_confirmation', methods=['GET'])
def payment_confirmation():
    # Display a simple order confirmation message
    return render_template('payment_confirmation.html')

#=========================================================================


# Home page for motors
@app.route('/motors', methods=['GET'], endpoint='motors')
def motors():
    return render_template('motors.html', motors=fpv_motors)


# Quick view page for a motor
@app.route('/quick_view/motor/<int:motor_id>', endpoint='quick_view_motor')
def quick_view_motor(motor_id):
    motor = next((item for item in fpv_motors if item['motor_id'] == motor_id), None)
    if not motor:
        abort(404, description="Motor not found")
    return render_template('motor_view.html', motor=motor)

# Motor detail page
@app.route('/motors/<int:motor_id>', methods=['GET'], endpoint='view_motor')
def view_motor(motor_id):
    motor = next((item for item in fpv_motors if item['motor_id'] == motor_id), None)
    if not motor:
        abort(404, description="Motor not found")
    return render_template('motor_view.html', motor=motor)


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')  # Assuming you name your "About Us" page 'about_us.html'

#==================================================


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return "Email already exists. Please log in."

        # Create a new user
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Store user_id in session
        session['user_id'] = new_user.id
        return redirect(url_for('profile'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Query the user by email and password
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('login.html')


@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    return render_template('profile.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

#============================================================================


@app.route('/vote/drone/<int:drone_id>', methods=['POST'])
def submit_drone_vote(drone_id):
    data = request.form
    rating = int(data.get('rating'))
    comment = data.get('comment', '')
    email = data.get('email')

    # Check if drone exists
    drone = Drone.query.get_or_404(drone_id)

    # Save vote
    vote = Vote(user_email=email, rating=rating, comment=comment, drone_id=drone_id)
    db.session.add(vote)
    db.session.commit()

    return jsonify({'message': 'Vote submitted successfully!'}), 201


@app.route('/votes/drone/<int:drone_id>', methods=['GET'])
def get_drone_votes(drone_id):
    votes = Vote.query.filter_by(drone_id=drone_id).all()
    return jsonify([
        {
            'user_email': vote.user_email,
            'rating': vote.rating,
            'comment': vote.comment,
            'created_at': vote.created_at.isoformat()
        }
        for vote in votes
    ])



@app.route('/vote/motor/<int:motor_id>', methods=['POST'])
def vote_motor(motor_id):
    motor = next((item for item in fpv_motors if item['motor_id'] == motor_id), None)
    if not motor:
        abort(404, description="Motor not found")
    motor['votes'] += 1
    return jsonify({"success": True, "votes": motor['votes']})



@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    # Get the rating value from the form
    rating = request.form.get('rating')  # This retrieves the rating from the POST request

    if rating is None:
        return "Please select a rating.", 400  # Handle no rating selection

    try:
        rating = int(rating)  # Convert rating to integer
    except ValueError:
        return "Invalid rating value.", 400

    # Create a new Rating instance and save to the database
    new_rating = Rating(stars=rating, comment="This is a sample comment")
    with app.app_context():  # Ensure this runs within the app context
        db.session.add(new_rating)
        db.session.commit()

    return "Rating saved successfully!"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)