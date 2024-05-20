from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Product
from schemas import ProductCreate, ProductUpdate, ProductSort


# Function to add a new product
def create_product(db: Session, product_data: ProductCreate):
    new_product = Product(**product_data.model_dump())
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except:
        raise HTTPException(status_code=400, detail='Could not add product')


# Fetch all products
def get_products(db: Session, sort_by: ProductSort):
    '''
        This will sort the product results based on name or price in ascending or
        descending manner based on the input provided.
    '''
    query = db.query(Product).filter(Product.version != 0)
    if sort_by == ProductSort.Name_A_to_Z:
        query = query.order_by(Product.name.asc())
    elif sort_by == ProductSort.Name_Z_to_A:
        query = query.order_by(Product.name.desc())
    elif sort_by == ProductSort.Price_Low_to_High:
        query = query.order_by(Product.price.asc())
    else:
        query = query.order_by(Product.price.desc())
    
    return query.all()


# Fetch a specific product
def get_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id, Product.version != 0).one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Update the information of a specific product
def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    product = db.query(Product).filter(
        Product.id == product_id, Product.version != 0).with_for_update().one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.version != product_data.version:
        raise HTTPException(
            status_code=409, detail="Product has been modified by another user")

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.version += 1

    db.commit()
    db.refresh(product)
    return product


# Function to delete a specific product
def delete_product(db: Session, product_id: int):
    '''
        This function is for deleting a specific product but does not literally
        delete the product from the database.

        If we actually delete a product, the order information will get affected but it is something
        which has to be stored for eternity. For this purpose a product is marked as deleted when its
        version is set to 0. From here on out, only products other than version = 0 will be treated as
        live products. 
    '''
    product = db.query(Product).filter(Product.id == product_id, Product.version != 0).one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.version = 0
    db.commit()
    return 'Product deleted successfully'
