from flask import Flask
from routes.user_routes import user_blueprint
from routes.recipe_routes import recipe_blueprint
from routes.meal_plan_routes import meal_plan_blueprint
from routes.recipe_details_routes import recipe_details_blueprint  # Adjusted import

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(recipe_blueprint, url_prefix="/recipes")
app.register_blueprint(meal_plan_blueprint, url_prefix="/meal_plan")
app.register_blueprint(recipe_details_blueprint, url_prefix="/recipe_details_route")  # Adjusted registration

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
