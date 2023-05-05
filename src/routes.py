import src.models.foods as food_model

routes = []

def send_food():
    foods = food_model.Foods.query.all()

    return foods

def send_home():
    return "Food API"


routes.append(
    {
        "rule": "/",
        "view_func": send_home,
        "options": {
            "methods": ["GET"]
        }
    }
)

routes.append(
    {
        "rule": "/foods",
        "view_func": send_food,
        "options": {
            "methods": ["GET"]
        }
    }
)