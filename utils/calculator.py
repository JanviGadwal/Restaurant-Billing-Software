def calculate_total(items, gst=True, discount=0):
    subtotal = sum(item['price'] * item['qty'] for item in items)

    gst_amt = sum(item['price'] * item['qty'] * (item['gst'] / 100) for item in items) if gst else 0

    discount_amt = (subtotal * discount) / 100

    total = subtotal + gst_amt - discount_amt

    return subtotal, gst_amt, discount_amt, total