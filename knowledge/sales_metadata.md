---CARD---
meta: kind=column table=sales name=sale_id
[COLUMN]
table: sales
name: sale_id
type: integer
business_meaning: Уникальный идентификатор продажи (технический ключ)
constraints: primary_key, not null
tags: [key, id, joinable]
usage_hints:
  - Использовать в JOIN и COUNT(DISTINCT).

---CARD---
meta: kind=column table=sales name=client_id
[COLUMN]
table: sales
name: client_id
type: integer
business_meaning: Идентификатор клиента, связанного с продажей
constraints: not null
usage_hints:
  - Использовать для связи с таблицей клиентов.

---CARD---
meta: kind=column table=sales name=product_id
[COLUMN]
table: sales
name: product_id
type: integer
business_meaning: Идентификатор продукта, проданного в транзакции
constraints: not null
usage_hints:
  - Использовать для связи с таблицей продуктов.

---CARD---
meta: kind=column table=sales name=quantity
[COLUMN]
table: sales
name: quantity
type: integer
business_meaning: Количество проданного товара
usage_hints:
  - Использовать для анализа объема продаж.

---CARD---
meta: kind=column table=sales name=sale_dt
[COLUMN]
table: sales
name: sale_dt
type: string (ISO 'YYYY-MM-DD')
business_meaning: Дата продажи (текст)
tags: [date_text, time_key, needs_cast]
cast_examples:
  postgres: sale_dt::date
  bigquery: DATE(sale_dt)
  snowflake: TO_DATE(sale_dt)
usage_hints:
  - Использовать для временных фильтров и агрегаций.

---CARD---
meta: kind=column table=sales name=total_cost
[COLUMN]
table: sales
name: total_cost
type: integer
business_meaning: Итоговая сумма по продаже
usage_hints:
  - Использовать для анализа выручки и прибыли.


