import pandas as pd
import numpy as np
import random

#Задание 1.1
recipes = pd.read_csv('data/recipes_sample.csv')
reviews = pd.read_csv('data/reviews_sample.csv')

#Задание 1.2
print("Таблица recipes:")
print(f"Кол-во строк: {len(recipes)}")
print(f"Кол-во столбцов: {len(recipes.columns)}")
print(f"Тип данных столбцов:\n {recipes.dtypes}")

print("\nТаблица reviews:")
print(f"Кол-во строк: {len(reviews)}")
print(f"Кол-во столбцов: {len(reviews.columns)}")
print(f"Тип данных столбцов:\n {reviews.dtypes}")

#Задание 1.3
print('\nТаблица recipes: ')
for col in recipes.columns:
    print(col, ': ', recipes[col].isna().sum(), ' пропущенных значений') 
print('Доля строк с пропусками:', round(recipes.isna().sum().sum()/len(recipes)*100, 2), '%')

print('\nТаблица reviews: ')
for col in reviews.columns:
    print(col, ': ', reviews[col].isna().sum(), ' пропущенных значений')  
print('Доля строк с пропусками:', round(reviews.isna().sum().sum()/len(reviews)*100, 2), '%') 

#Задание 1.4
print('\nТаблица recipes:')
for col in recipes.select_dtypes(include=[np.number]):
    if col == 'minutes' or col == 'n_steps' or col == 'n_ingredients':
        print(col, ': среднее =', round(recipes[col].mean(), 2))

print('\nТаблица reviews:')  
for col in reviews.select_dtypes(include=[np.number]):
    if col == 'rating':
        print(col, ': среднее =', round(reviews[col].mean(), 2)) 

#Задание 1.5
recipes_name = recipes['name'].tolist()
random_recipes = random.sample(recipes_name, 10)
serias = pd.Series(random_recipes)
print('\n', "Вывод серии рандомных 10 названий рецептов: ")
print(serias)

#Задание 1.6
val = 0
for i in range(len(reviews)):
    reviews.at[i, 'Unnamed: 0'] = val
    val += 1
print('\n', "Вывод первых пяти строк с измененным index: ")
print(reviews[:5])

#Задание 1.7
filter_recipes = recipes[(recipes['minutes'] <= 20) & (recipes['n_ingredients'] <= 5)]
print('\n', "Вывод отфильтрованного DataFrame, где время не больше 20, а кол-во ингридиентов не больше 5: ")
print(filter_recipes[['name', 'minutes', 'n_ingredients']])

#Задание 2.1
recipes['submitted'] = pd.to_datetime(recipes['submitted'])
print("\nВывод столбца submittes в формате datetime")
print(recipes['submitted'])

#Задание 2.2
t_filter_recipes = recipes[recipes['submitted'] > '2010-01-01']
print("\nВывод отфильтрованного DataFrame, где год не позже 2010: ")
print(t_filter_recipes[['name', 'submitted']])

#Задание 3.1
recipes['description_length'] = recipes['description'].str.len()
print("\nВывод значений стобца description_length: \n", recipes['description_length'])

#Задание 3.2
recipes['name'] = recipes['name'].str.title()
print("\nВывод названия рецептов: \n", recipes['name'])

#Задание 3.3 
recipes['name_word_count'] = recipes['name'].str.split().str.len()
print("\nВывод столбца name_word_count: \n", recipes['name_word_count'])

#Задание 4.1
grouped = recipes.groupby('contributor_id')
counts = grouped.name.count() 
sorted_counts = counts.sort_values(ascending=False)
print('\nВывод участника который добавил большее кол-во рецептов: \n', sorted_counts.head(1))

#Задание 4.2
rating_val = 0
ans_rating_val = reviews['rating'].mean()
print("\nСредний рейтинг: ", ans_rating_val)
grouped = reviews.groupby('recipe_id')
reviewed_recipes = grouped.groups.keys()  
no_reviews = recipes[recipes['id'].isin(reviewed_recipes)]
print('\nКол-во рецептов без отзывов равно: ', len(no_reviews))

#Задание 4.3
reviews['date'] = pd.to_datetime(reviews['date'])
reviews_by_year = reviews.groupby('date').count()
print('\nКоличество рецептов с разбивкой по годам создания: ', len(reviews_by_year))

#Задание 5.1
reviews = reviews.rename(columns={'Unnamed: 0' : 'id'})
merged = pd.merge(recipes, reviews, on='id')
grouped = merged.groupby(['id', 'name']).agg({'user_id': 'count', 'rating': 'mean'})
filtered = grouped[grouped['user_id'] > 0]
print(filtered.head(5))

#Задание 5.2
merged = pd.merge(recipes, reviews, on='id', how='left')
grouped = merged.groupby(['id', 'name']).agg({'user_id': 'count'})
grouped = grouped.rename(columns={'user_id': 'review_count'})
result = pd.DataFrame({'recipe_id': grouped.index.get_level_values(0),
                    'name': grouped.index.get_level_values(1),
                    'review_count': grouped['review_count']})
result['review_count'] = result['review_count'].fillna(0)
print(result.head(5))

#Задание 5.3
df = pd.merge(recipes, reviews, on='id')
df['year'] = pd.to_datetime(df['date']).dt.year
mean_ratings = df.groupby('year')['rating'].mean()
min_year = mean_ratings.idxmin()
print(min_year)

#Задание 6.1
recipes = recipes.sort_values('name_word_count', ascending=False)
recipes.to_csv('recipes_with_word_count.csv', index=False)

#Задание 6.2
writer = pd.ExcelWriter('output.xlsx')
filtered.to_excel(writer, sheet_name='Рецепты с оценками', index=True)
result.to_excel(writer, sheet_name='Количество отзывов по рецептам', index=False)
writer._save()
