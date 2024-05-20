from fastapi import HTTPException
from sqlalchemy.orm import Session
from orders.models import Order, OrderItem, Product
from orders.schemas import OrderCreate, OrderStatus, OrderFilter, OrderSort


enum_table_name_mapping = {
    'TotalPrice': Order.total_price,
    'OrderStatus': Order.order_status
}

# Function to create order_items and order based on the user input of orders.
def create_order(db: Session, user_id: int, order_data: OrderCreate):
    '''
        This will check the products in the orders against the products currently in the system 
        which are not marked deleted by the version number as 0. If any deleted products are provided
        in the input then all those products flagged accordingly.
    '''
    mapping = [order.model_dump() for order in order_data.order_items]
    product_quantity = {prod_quan['product_id']: prod_quan['quantity'] for prod_quan in mapping}
    product_ids = set(product_quantity)
    product_prices = dict(db.query(Product.id, Product.price).where(Product.id.in_(product_ids), Product.version != 0).all())

    existing_product_ids = product_prices.keys()
    given_product_ids = product_quantity.keys()

    diff = set(existing_product_ids) ^ set(given_product_ids)
    if diff:
        if len(diff) == 1:
            word = ' with id '
        else:
            word = 's with ids '
        raise HTTPException(status_code=404, detail="Order contains deleted product" + word + ', '.join(map(str, diff)) + '. Remove and try again')

    total_price = sum([product_price * product_quantity[product_id] for product_id, product_price in product_prices.items()])
    order = Order(user_id=user_id, total_price=total_price)
    db.add(order)
    db.commit()
    db.refresh(order)

    order_items = []
    for item_data in order_data.order_items:
        if item_data.product_id in product_prices:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                price=product_prices[item_data.product_id]
            )
            db.add(order_item)
            order_items.append(order_item)

    db.commit()

    order.order_items = order_items
    return order


# Function to get all orders for a user
def get_orders(db: Session, user_id: int, filter_by: OrderFilter, sort_by: OrderSort):
    '''
        This will return all orders for a given user. Filter functionality based on the order status
        and sorting functionality based on either prices or order status has been provided.
    '''
    query = db.query(Order).filter(Order.user_id == user_id)
    if filter_by != OrderFilter.All:
        query = query.filter(Order.order_status == filter_by)
    query = query.order_by(enum_table_name_mapping[sort_by])
    return query.all()


# Returns a specific order for a specific user
def get_order(db: Session, order_id: int, user_id: int):
    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == user_id)
        .one_or_none()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# To update order status as and when required for a particular order of a user
def update_order_status(db: Session, order_id: int, user_id: int, order_status: OrderStatus):
    '''
        Functionality to update the order status of a particular order of a user.
        Once an order status milestone has been reached, order status in the future cannot be updated 
        to a milestone before it in the order status heirarchy.
        This will ensure that any unnecessary updates are not possible and data integrity is maintained.
    '''
    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == user_id)
        .one_or_none()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order_status_heirarchy = OrderStatus._member_names_
    order_status_heirarchy = order_status_heirarchy[order_status_heirarchy.index(order.order_status) + 1:]

    if order_status not in order_status_heirarchy:
        raise HTTPException(status_code=422, detail="Order status cannot be changed to a previously updated status")
    
    order.order_status = order_status
    db.commit()
    return order
