---CARD---
meta: kind=table table=products pii=false
[TABLE]
name: products
business_name: Товары (канцелярия)
purpose: Справочник товарных позиций (SKU) с розничной ценой и категорией
grain: 1 строка = 1 товар (SKU)
primary_key: product_id
pii: нет
sample_columns: product_id, name, category, price
notes:
  - Категории (по примеру): Письменные принадлежности; Бумажная продукция; Офисные аксессуары; Хранение и организация; Чертёжные и художественные принадлежности.
  - Цена хранится числом; валюта не указана (уточняется в бизнес-справочнике).
tags: [catalog, non_pii]


---CARD---
meta: kind=column table=products name=product_id pii=false
[COLUMN]
table: products
name: product_id
type: integer
business_meaning: Уникальный идентификатор товара (SKU)
constraints: primary_key, not null
examples: 1, 10, 25
tags: [key, id, joinable, non_pii]
usage_hints:
  - Использовать в JOIN с фактами продаж (например, sales.product_id).
  - Подходит для COUNT(DISTINCT product_id).


---CARD---
meta: kind=column table=products name=name pii=false
[COLUMN]
table: products
name: name
type: varchar
business_meaning: Наименование товара (человеко-читаемое)
examples: "Ручка шариковая", "Бумага для принтера", "Органайзер настольный"
tags: [dimension, label, non_pii]
usage_hints:
  - Поиск по подстроке/ILIKE; учитывать формы слов на русском.
  - В отчётах комбинировать с category.


---CARD---
meta: kind=column table=products name=category pii=false
[COLUMN]
table: products
name: category
type: varchar
business_meaning: Классификационная категория товара
examples:
  - "Письменные принадлежности"
  - "Бумажная продукция"
  - "Офисные аксессуары"
  - "Хранение и организация"
  - "Чертёжные и художественные принадлежности"
tags: [dimension, taxonomy, non_pii]
usage_hints:
  - Использовать в GROUP BY и фильтрах.
  - При необходимости вынести в отдельный справочник категорий.


---CARD---
meta: kind=column table=products name=price pii=false
[COLUMN]
table: products
name: price
type: integer   # используйте numeric(10,2), если появятся дробные цены
business_meaning: Розничная цена за единицу товара (валюта не указана)
value_profile:
  min: 10
  p50: 70
  p95: 300
  max: 400
  mean_approx: 106.2
examples: 25, 90, 400
tags: [measure, money, currency_unknown, non_pii]
usage_hints:
  - Атрибут позиции, НЕ суммируйте price по строкам как выручку.
  - Для выручки используйте qty * price в фактах продаж.
  - Для фильтров — обычные числовые условия (>=, BETWEEN).
