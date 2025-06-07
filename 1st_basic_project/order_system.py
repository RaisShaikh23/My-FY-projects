print("----------MENU--------")
menu = {
    1:{"Dish":"Panir" , "price":70},
    2:{"Dish":"Chicken" , "price":170},
    3:{"Dish":"Mix-Veg" , "price":100},
    4:{"Dish":"Daal" , "price":110},
    5:{"Dish":"Rice" , "price":50},
    6:{"Dish": "Pasta", "price": 120},
    7:{"Dish": "chicken Biryani", "price": 180},
    8:{"Dish": "egg fried rice", "price": 140},
    9:{"Dish": "panner pulav", "price": 100},
    10:{"Dish": "chicken tandori", "price": 200},
    11:{"Dish": "chicken nuggets", "price": 190},
    12:{"Dish": "Butter chicken", "price": 210},
    13:{"Dish": "salsa rice", "price": 120},
    14:{"Dish": "panner Butter masala", "price": 220},
    15:{"Dish": "manchurian", "price": 100},
    16:{"Dish": "Chilly fry", "price": 104},
    17:{"Dish": "Dry Chilly", "price": 108},
    18:{"Dish": "Makhan", "price": 106},
}
import pandas as pd
# Show Menu
menu_df = pd.DataFrame(menu)
print(menu_df.T)

# Cart For selected Dishes
cart = []

while True:
    try:
        user = int(input("\n~Enter The Number From Menu.\n~Enter 0 for Total Meal.\nPlz Enter Your Meal No :- "))
        if user==0:
            break
        meal = menu_df[user]
        cart.append(meal)
    except ValueError:
        print("Enter The Number From Menu Plz !")
    except:
        print(f"No.{user} Not In A Menu Card try Again !")
        
# Generating Bill
k = pd.DataFrame(cart)

cart1 = k.groupby("Dish")["price"].sum()
import time as tm
td = tm.ctime()
print("")
print("")
print("-----------Added To Cart-----------\n",cart1)
print()
print(f"-----------Total Bill--------------\nBill : ₹ {cart1.sum()}")
print()
print(f"----------------------------------\n{td}")
print()
print(f"----------------------------------\n*Thank U For Your Order*\n\nPlz Visit Again !")