from flask import Flask
from routes.user_routes import user_blueprint
from routes.recipe_routes import recipe_blueprint
from routes.meal_plan_routes import meal_plan_blueprint

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(recipe_blueprint, url_prefix="/recipes")
app.register_blueprint(meal_plan_blueprint, url_prefix="/meal_plan")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
