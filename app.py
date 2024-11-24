from flask import Flask
from routes.user_input_routes import user_input_blueprint
from routes.recipe_routes import recipe_blueprint
from routes.meal_plan_routes import meal_plan_blueprint

app = Flask(__name__)

# Register blueprints
app.register_blueprint(user_input_blueprint, url_prefix="/api/input")
app.register_blueprint(recipe_blueprint, url_prefix="/api/recipes")
app.register_blueprint(meal_plan_blueprint, url_prefix="/api/meal_plan")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)  # Adjust for VM deployment
