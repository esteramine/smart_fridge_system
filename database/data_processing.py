import re

from .food_expiration import get_expiration_date

class FoodItem:
    def __init__(self, name, quantity, danger, category, ymin, xmin, ymax, xmax, expiration_date=None, user_defined=False, in_fridge=True, doc_id=None):
        self.doc_id = doc_id
        self.name = name.strip()
        self.quantity = int(quantity)
        self.danger = int(danger)
        self.category = category.strip()
        self.ymin = int(ymin)
        self.xmin = int(xmin)
        self.ymax = int(ymax)
        self.xmax = int(xmax)
        self.expiration_date = expiration_date if expiration_date else get_expiration_date(self.category)
        self.user_defined = user_defined
        self.in_fridge = in_fridge

    @staticmethod
    def from_dict(source, doc_id=None):
        return FoodItem(
            name=source.get('name', ''),
            quantity=source.get('quantity', 0),
            danger=source.get('danger', 0),
            category=source.get('category', ""),
            ymin=source.get('ymin', 0),
            xmin=source.get('xmin', 0),
            ymax=source.get('ymax', 0),
            xmax=source.get('xmax', 0),
            expiration_date=source.get('expiration_date', ""),
            user_defined = source.get('user_defined', False),
            in_fridge = source.get('in_fridge', False),
            doc_id=doc_id
        )

    def to_dict(self):
        return {
            "name": self.name,
            "quantity": self.quantity,
            "danger": self.danger,
            "category": self.category,
            "expiration_date": self.expiration_date,
            "user_defined": self.user_defined,
            "in_fridge": self.in_fridge,
            "ymin": self.ymin,
            "xmin": self.xmin,
            "ymax": self.ymax,
            "xmax": self.xmax,
        }

    def __repr__(self):
        return f"FoodItem(doc_id={self.doc_id}, name={self.name}, quantity={self.quantity}, danger={self.danger}, category={self.category}, expiration_date={self.expiration_date}, user_defined={self.user_defined}, in_fridge={self.in_fridge}, ymin={self.ymin}, xmin={self.xmin}, ymax={self.ymax}, xmax={self.xmax})"

def create_food_list(text):
    # example food item string: 
    # eggs, 6, 0, whole_eggs, [314 271 394 530] (means [ymin xmin ymax xmax])
    # meat patties, 1, 0, cooked_meat_and_poultry, [512 477 587 638]
    food_list = []
    for line in text.split("\n"):
        attrs = line.split(",")
        if len(attrs) == 5:
            try:
                # Remove brackets and split coordinates
                coordinates = re.sub(r'[\[\]]', '', attrs[4]).split()
                if len(coordinates) == 4:
                    food_item = FoodItem(
                        name=attrs[0],
                        quantity=attrs[1],
                        danger=attrs[2],
                        category=attrs[3],
                        ymin=coordinates[0],
                        xmin=coordinates[1],
                        ymax=coordinates[2],
                        xmax=coordinates[3],
                    )
                    food_list.append(food_item)
            except ValueError:
                print(f"Skipping invalid line: {line}")
        else:
            print(f"Skipping line with incorrect format: {line}")

    return food_list
