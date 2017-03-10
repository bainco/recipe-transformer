categories_list = [
	'Appetizer',
	'appetizer',
	'Snack', 
	'snack', 
	'BBQ', 
	'Dessert'
	'dessert',
	'Breakfast' 
	'breakfast',
	'Lunch', 
	'lunch',
	'Dinner', 
	'dinner',
	'Drinks', 
	'drinks',
	'Healthy', 
	'healthy',
	'Holiday', 
	'holiday',
	'Pasta',
	'pasta',
	'Seafood',
	'seafood',
	'Meat',
	'meat',
	'Poultry',
	'poultry',
	'Soup',
	'soup',
	'Stew'
	'stew',
	'Chili',
	'chili',
	'Beef',
	'beef',
	'Chicken',
	'chicken',
	'Pork',
	'pork',
	'Salmon',
	'salmon',
	'Bread',
	'bread',
	'Cake',
	'cake',
	'Salmon'
	'salmon',
	'Smoothie'
	'smoothie',
	'Vegan'
	'vegan',
	'Vegetarian',
	'vegetarian',
	'Asian',
	'Indian',
	'Italian',
	'Mexican',
	'Southern',
	'Christmas',
	'Easter',
	'Seasonal',
	'seasonal']

def classify(title, description):
	'''Classify takes in two strings and returns a list of the types of cuisines
	a recipe can be categorized as.'''
	type_of_cuisine = []
	title_and_description = title + " " + description
	for word in title_and_description.split():
		if word in categories_list:
			type_of_cuisine.append(word)
	print type_of_cuisine
	return type_of_cuisine

classify("Baked Buffalo Chicken Dip","You can't keep showing up at these Super Bowl parties with a bag of chips every year. So, if you're ready to go from snack scrub to appetizer all-star, then give this great baked dip a try.")
