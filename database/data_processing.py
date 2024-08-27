import re

class FoodItem:
    def __init__(self, name, quantity, safety, ymin, xmin, ymax, xmax):
        self.name = name.strip()
        self.quantity = int(quantity)
        self.safety = int(safety)
        self.ymin = int(ymin)
        self.xmin = int(xmin)
        self.ymax = int(ymax)
        self.xmax = int(xmax)

    def __repr__(self):
        return f"FoodItem(name={self.name}, quantity={self.quantity}, safety={self.safety}, ymin={self.ymin}, xmin={self.xmin}, ymax={self.ymax}, xmax={self.xmax})"

def create_food_list(text):
    # example food item string: 
    # sauce, 1, 0, [183 94 403 217] (means [ymin xmin ymax xmax])
    # meat patty, 1, 0, [522 469 582 641]
    food_list = []
    for line in text.split("\n"):
        attrs = line.split(",")
        if len(attrs) == 4:
            try:
                # Remove brackets and split coordinates
                coordinates = re.sub(r'[\[\]]', '', attrs[3]).split()
                if len(coordinates) == 4:
                    food_item = FoodItem(
                        name=attrs[0],
                        quantity=attrs[1],
                        safety=attrs[2],
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
