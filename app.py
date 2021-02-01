import os
import config
import requests
import json

from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    session,
    g,
    jsonify,
    make_response,
)
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from forms import UserAddForm, LoginForm, EditUserForm, AddFavoriteForm, SearchForm
from models import db, connect_db, User, Favorite

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgres:///closest"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "it's a secret")
HERE_API_KEY = config.here_api_key
GOOGLE_API_KEY = config.google_api_key

# toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


##############################################################################
# Signup routes:


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("signup.html", form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Handle logout of user."""

    session.clear()
    flash("You have logged out successfully!", "success")
    return redirect("/login")


##############################################################################
# Search/Results routes:


@app.route("/", methods=["GET", "POST"])
def home_page():
    form = SearchForm()

    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/login")

    if form.validate_on_submit():

        address = form.address.data

        search = str(address)

        print(
            f"made it to form validation and... address: {address}...search: {search}"
        )

        return redirect(f"/results/{search}")

    return render_template("home.html", form=form)


@app.route("/google_search/<string:latlng>", methods=["GET", "POST"])
def google_search(latlng):
    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/login")

    # print(latlng)

    comma_location = latlng.find(",")
    # print(comma_location)

    latitude = latlng[0:comma_location]

    longitude = latlng[comma_location+1:]

    # print(f"latitude: {latitude} longitude: {longitude}")

    google_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={GOOGLE_API_KEY}"
    google_resp = requests.get(google_url)
    google_resp_to_dict = json.loads(google_resp.text)
    # print(google_resp_to_dict)

    formatted_address = google_resp_to_dict["results"][0]["formatted_address"]
    print(formatted_address)

    return redirect(f"/results/{formatted_address}")


@app.route("/results/<string:search>", methods=["GET", "POST"])
def show_results(search):

    # print(f"search: {search}")
    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/login")

    geocode_URL = f"https://geocode.search.hereapi.com/v1/geocode?q={search}&apiKey={HERE_API_KEY}"
    geocode_resp1 = requests.get(geocode_URL)
    # print(geocode_resp1.text)

    resp_to_dict = json.loads(geocode_resp1.text)
    # print(resp_to_dict)
    search_lat_long = resp_to_dict["items"][0]["position"]
    # print(lat_long)
    here_search_latitude = search_lat_long["lat"]
    here_search_longitude = search_lat_long["lng"]
    # print(f"lat: {here_search_latitude} and long: {here_search_longitude}")

    public_transit_URL = f"https://transit.hereapi.com/v8/stations?in={here_search_latitude},{here_search_longitude};r=50000&return=transport,address&maxPlaces=50&apiKey={HERE_API_KEY}"
    transit_resp2 = requests.get(public_transit_URL)
    # print(transit_resp2.text)
    stations_dict = json.loads(transit_resp2.text)
    print(stations_dict)
    if "notices" in stations_dict:
        print("Made it into redirect loop")
        sad_message = (
            f"Maybe try living somewhere closer to civilization, {g.user.username}"
        )
        return render_template("no_results.html", sad_message=sad_message)

    closest_station_name = stations_dict["stations"][0]["place"]["name"]
    closest_station_name_og = closest_station_name
    closest_station_name = closest_station_name.replace("&", "%26")
    closest_station_transport = stations_dict["stations"][0]["transports"][0]["mode"]
    combined_address_search = (
        f"{closest_station_name} {closest_station_transport} station"
    )
    # print(combined_address_search)

    closest_station_address = stations_dict["stations"][0]["place"]["address"]
    address_string = str(
        closest_station_address["houseNumber"]
        + " "
        + closest_station_address["street"]
        + " "
        + closest_station_address["city"]
        + " "
        + closest_station_address["postalCode"]
    )
    # print(f"address string: {address_string}")

    google_map_URL = f"https://www.google.com/maps/embed/v1/place?key={GOOGLE_API_KEY}&q={combined_address_search}&center={here_search_latitude},{here_search_longitude}"
    # print(google_map_URL)

    table_array = []

    stations_array = stations_dict["stations"]
    print(stations_array)
    length = len(stations_array)
    # print(f"length of stations array: {length}")
    for x in range(len(stations_array)):
        # print(stations_array[x]["place"]["address"])
        row_array = []
        row_array.append(stations_array[x]["place"]["name"])
        try:
            row_array.append(
                str(
                    stations_array[x]["place"]["address"]["houseNumber"]
                    + " "
                    + stations_array[x]["place"]["address"]["street"]
                    + " "
                    + stations_array[x]["place"]["address"]["city"]
                    + " "
                    + stations_array[x]["place"]["address"]["postalCode"]
                )
            )
        except KeyError:
            row_array.append("Exact Address Not Found")

        row_array.append(stations_array[x]["transports"][0]["headsign"])
        row_array.append(stations_array[x]["transports"][0]["mode"])

        table_array.append(row_array)

    # print(table_array)

    return render_template(
        "results.html",
        google_map_URL=google_map_URL,
        closest_station_name_og=closest_station_name_og,
        table_array=table_array,
    )


##############################################################################
# User routes:


@app.route("/users/<int:user_id>/")
def show_profile(user_id):
    """Show User Profile Information"""

    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/login")

    user = User.query.get_or_404(user_id)

    return render_template("user_profile.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def edit_profile(user_id):
    """Edit User Profile Information """

    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/login")

    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.phone_number = form.phone_number.data
        user.image_url = form.image_url.data
        password = g.user.password

        user_auth = User.authenticate(form.username.data, form.password.data)

        if user_auth:
            try:
                db.session.commit()
                return redirect(f"/users/{g.user.id}")
            except SQLAlchemyError as e:
                print(str(e))
                db.session.rollback()
                raise
                return redirect(f"/users/{g.user.id}")
        else:
            flash("Incorrect Username/Password.", "danger")
            return redirect(f"/users/{g.user.id}/")

    return render_template("edit_profile.html", form=form, user=user)


@app.route("/favorites/show")
def favorites_show():
    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/login")

    favorites = Favorite.query.filter(Favorite.user_id == g.user.id).all()

    return render_template("favorites.html", favorites=favorites)


@app.route("/favorites/add", methods=["POST"])
def favorite_add():
    data = request.json

    user = User.query.get(g.user.id)

    # print(data)

    name = data["name"]
    address = data["address"]
    map_image_url = data["map_image_url"]

    check_dupes = Favorite.query.filter(
        Favorite.user_id == g.user.id, Favorite.map_image_url == map_image_url
    ).count()

    if check_dupes > 0:
        return make_response("Already a Favorite!", 200)

    new_favorite = Favorite(
        title=name, address=address, map_image_url=map_image_url, user_id=user.id
    )
    db.session.add(new_favorite)
    db.session.commit()

    return make_response("Add Worked", 200)


@app.route("/favorites/<int:favorite_id>/delete", methods=["POST"])
def favorite_delete(favorite_id):

    if not g.user:
        flash("Access unauthorized", "danger")
        return redirect("/login")

    favorite = Favorite.query.get(favorite_id)

    db.session.delete(favorite)
    db.session.commit()

    return redirect("/favorites/show")
