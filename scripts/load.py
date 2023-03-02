from server.models import Inventory, ProductType, Store
from server.products import products

def run():
    Inventory.objects.all().delete()
    for product in products:
        pro = Inventory(
            name = product['product_name'],
            productType = ProductType.objects.get(id=2),
            store = Store.objects.get(id=1),
            quantity = product['quantity'],
            purchaseDate = product['expiry_date'],
            costPrice = product['buying_price'],
            sellingPrice = product['selling_price']
        )

        pro.save()