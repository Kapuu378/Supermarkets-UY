# **Supermarkets-UY is a webscrapping project.**
Scrapes various Uruguayan supermarkets in order to get price data daily.

## Features

- ✅ Uses requests module to parse Vtex open API's.
- ✅ Formats data in a simple accessible way.
- ✅ Uses SqlAlchemy and SQLite3 to store the data.


## **Setup**
```
git clone git@github.com:Kapuu378/Supermarkets-UY.git
cd Supermarkets-UY
pip install -r requirements.txt
```

## **Quick start**
After setting it up you can run any of the Supermarket webscrappers in the proyect. E.g. 
``` python3 sample/devoto.py```

## **DATABASE TABLE STRUCTURE**
When you run this script it will automatically create a .db file in the root directory of the proyect. There will be only two tables:

**Products**
| ID (int) | PROD_ID (int) | PROD_NAME (varchar) | BRAND (varchar) | LK_TEXT (varchar) | SMK_NAME (varchar) |
|---------|--------|----------|----------|----------|----------|
|1|999999|Aceite|Marca 1| aceite-girasol-m3dn|Devoto|
|2|999998|Arroz|Marca 2| arroz-f4dn|Devoto|
|...|...|...|...|...|

**Prices**
| ID (int) | UNIT_P(int) |FULL_P (int) | FULL_P_ND (int) | DATE(varchar)|PROD_FK (int)|
|---------|--------|----------|----------|----------|----------|
|1|190|190|200|2025-12-26|23|
|2|190|190|200|2025-12-26|24|
|...|...|...|...|...|...|

This table structure prevents duplication of data and reduces it's size.
Joining the two tables results in:
<img src="https://i.imgur.com/XBSKXQ9.png">

**Note:** All the scrapers will push their data to this DB file.