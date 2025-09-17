---CARD---
meta: kind=table table=clients
[TABLE]
name: clients
business_name: Клиенты
purpose: Справочник клиентов (1 строка = 1 клиент)
grain: 1 строка = уникальный клиент
primary_key: client_id
temporal_fields: dob (string 'YYYY-MM-DD')
pii: fullname, dob
tags: catalog, ref, has_pii
usage_hints:
  - PII не выводить сырым текстом; агрегации или маски.


---CARD---
meta: kind=column table=clients name=client_id
[COLUMN]
table: clients
name: client_id
type: integer
business_meaning: Уникальный идентификатор клиента (технический ключ)
constraints: primary_key, not null
tags: [key, id, joinable, non_pii]
usage_hints:
  - Использовать в JOIN и COUNT(DISTINCT).


---CARD---
meta: kind=column table=clients name=fullname pii=true
[COLUMN]
table: clients
name: fullname
type: varchar
business_meaning: Полное имя клиента (ФИО)
pii: true
tags: [pii, name, dimension]
usage_hints:
  - По умолчанию скрывать/маскировать.


---CARD---
meta: kind=column table=clients name=dob pii=true
[COLUMN]
table: clients
name: dob
type: string (ISO 'YYYY-MM-DD')
business_meaning: Дата рождения клиента (текст)
pii: true
tags: [pii, date_text, time_key, needs_cast]
cast_examples:
  postgres: dob::date
  bigquery: DATE(dob)
  snowflake: TO_DATE(dob)