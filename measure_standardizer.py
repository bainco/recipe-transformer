types_of_measurement_list = ['teaspoon', 'cup', 'pound', 'dash', 'pinch',  'pint', 'quart', 'gallon', ' oz', 'liter', 'gram', 'ml', 'ounce', 'stick', 'can', 'jar', 'lb', 'package']

CONVERSION_FACTOR = {
    'teaspoon': float(0.167),
    'cup': 8,
    'pound': 16 ,
    'dash': float(0.333),
    'pinch': float(0.333),
    'pint': 16,
    'quart': 32,
    'gallon': 128,
    'oz': 1,
    'liter': float(33.814),
    'gram': float(0.03),
    'ml': float(0.0338),
    'ounce': 1,
    'stick': 2,
    'can': 8,
}

def standardize_measurement(quant, measurement):
    return (float(quant) * CONVERSION_FACTOR[measurement])
