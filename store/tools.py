from .models import Product, Order
from .serializers import ProductSerializer


def search_products(args):
    keyword = args.get("q", "")
    products = Product.objects.filter(name__icontains=keyword)
    return ProductSerializer(products, many=True).data


def check_stock(args):
    product_id = args.get("id")
    product = Product.objects.filter(id=product_id).first()

    if not product:
        return {"error": "Product not found"}

    return {"product": product.name, "stock": product.stock}


def recommend_products(args):
    products = Product.objects.all()[:5]
    return ProductSerializer(products, many=True).data


def track_order(args):
    order_id = args.get("order_id")

    order = Order.objects.filter(id=order_id).first()

    if not order:
        return {"error": "Order not found"}

    return {
        "order_id": order.id,
        "customer": order.customer_name,
        "product": order.product.name,
        "quantity": order.quantity,
        "status": order.status,
        "message": f"Your order #{order.id} is {order.status.lower()}.",
    }


from .models import Product, Order


def place_order(args):
    product_id = args.get("product_id")
    customer_name = args.get("customer_name")
    quantity = int(args.get("quantity", 1))

    product = Product.objects.filter(id=product_id).first()

    if not product:
        return {"message": "Product not found"}

    if product.stock < quantity:
        return {"message": "Insufficient stock"}

    order = Order.objects.create(
        customer_name=customer_name, product=product, quantity=quantity, status="Placed"
    )

    product.stock -= quantity
    product.save()

    return {
        "order_id": order.id,
        "message": f"Order placed successfully for {product.name}.",
    }


def cancel_order(args):
    order_id = args.get("order_id")

    order = Order.objects.filter(id=order_id).first()

    if not order:
        return {"message": "Order not found"}

    if order.status == "Cancelled":
        return {"message": "Order already cancelled"}

    if order.status == "Delivered":
        return {"message": "Delivered order cannot be cancelled"}

    product = order.product
    product.stock += order.quantity
    product.save()

    order.status = "Cancelled"
    order.save()

    return {
        "order_id": order.id,
        "message": f"Order #{order.id} cancelled successfully.",
    }
