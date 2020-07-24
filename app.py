import json
import pymongo
import operator

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

#   Creates database 'Data Tracker' and collection 'products'.
mydb = myclient["Data_Tracker"]
product_col = mydb["product_col"]

def display(collection):
    try:
        name = mydb[collection]
        for i in name.find():
            print(i)
    except:
        pass

#   Imports data from a JSON file revcieved from SQL database.
with open("data.json", "r") as line:
    data = json.load(line)
    for i in data: product_col.update(i, i, upsert=True)

print(f"[*] Database:\n\n")
display("product_col")

#   Creates collection for top three products.
top_products_col = mydb["top_three_products"]

#   The var 'top_items' selects and returns the first objects from the database.
#   In line 23 we add the three objects to the collection top_three_products
top_items = product_col.find().limit(3)

try:
    for i in top_items: top_products_col.update(i, i, upsert=True)
except:
    pass

print(f"\n\n[*] Top Three Products:\n\n")
for i in product_col.find().limit(3): print(i)
#   Sorts all the data by their product type in descending order.
product_col.find().sort("Type", -1)
print(f"\n\n[*] Descending Data: \n\n")
display("product_col")


#   Deletes two products from my top three products.
top_products_col.delete_many({"Type":"cooldrink"})
print(f"\n\n[*] Deleted Two Objs:\n\n")
display('top_three_products')


#   Updates 1 product and its brands.
item_brand = {"Type": "chips", "Brand/product": "Lays"}
new_brand = {"id": 1, "Type": "cooldrink","Brand/product": "Coke Zero", "Price per unit":7.5, "Stock":124, "Total stock price":930}

mydb.product_col.update(item_brand, new_brand, upsert=True)
print("\n\n[*] Updated Product:\n\n")
for i in product_col.find({"Brand/product": "Sprite"}): print(i) 

#   Search for five brands.
brand_list = ['Simba', 'Monster', 'BarOne', 'Doritos', 'Fanta']

print("[*] Items Searched\n")

item_types = ["chips", "cooldrink", "chocolate", "pies", "cupcakes", "veggies", "fruit", "energy_drink", "sauce"]
items = {}

for i in item_types:
    a = product_col.find({'Type': {'$regex': f'{i}.*'}})
    items[i] = a.count()

data = sorted(items.items(), key=operator.itemgetter(1))

i = 0
while i < 5:
   b = data[i][0]
   c = product_col.find({"Type":b})
   for item in c: print(item)
   i+= 1

myclient.close()