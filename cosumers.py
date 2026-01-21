import json
from fastapi import FastAPI, HTTPException

def create_delivery(state , event):
    data = json.loads(event.data)
    return {
        "id" : event.delivery_id,
        "budget" : int(data["budget"]),
        "notes" : data["notes"],
        "status" : "ready"
    }
def start_delivery(state , event):
       
    if(state["status"] !='ready' ):
          raise HTTPException(status_code=400 , detail="Delivery is already started")
    return state | {
         "status" : "active"
    }
def pickup_products(state , event):
    data = json.loads(event.data)
    current_budget = int(state["budget"])
    pickup_cost = int(data['purchase_price'])
    total_cost = pickup_cost * int(data['quantity'])
    if current_budget < total_cost:
        raise HTTPException(status_code=400 , detail="Not have enough budget")
     
    new_budget =  current_budget - total_cost
    if new_budget < 0:
        raise HTTPException(status_code=400 , detail="Not have enough budget")
    return state | {
        "budget" : new_budget,
        "purchase_price" : int(data['purchase_price']),
        "quantity" : int(data['quantity']),
        "status" : "collected"
    }
def delivery_product(state , event):
    if state.get("status") != "collected":
        raise HTTPException(400, "Products must be picked up before delivery")
    data = json.loads(event.data)
    print(event)
    new_budget = state["budget"] + int(data["sell_price"]) *int(data["quantity"])
    new_quantity = state["quantity"] - int(data['quantity'])
    if new_quantity < 0:
        raise HTTPException(status_code=400 , detail="Not have enough quantity")
    return state | {
        
        "budget" : new_budget,
        "sell_price" : int(data["sell_price"]),
        "quantity" : new_quantity,
        "status" : "completed"
    }
def increase_budget(state , event):
    data = json.loads(event.data)
    state['budget'] += int(data['budget'])
    return state
CONSUMERS = {
    "CREATE_DELIVERY" : create_delivery,
    "START_DELIVERY" : start_delivery,
    "Pick_up" :  pickup_products,
    "DELIVERED_PRODUCTS" : delivery_product,
    "INCREASE_BUDGET" :  increase_budget
}
# we can change start delivery to consumers

