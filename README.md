1 - bo'lib .env nomli faylni loyiha ichiga tashlab qo'yish kerak

Keyin quyidagi kodlarni ketma-ket yozib chiqiladi (bu buyruqlar konsolda proyekt ichidan yoziladi)

1) python -m venv .venv

2) pip install -r requirements.txt

3) .venv/Scripts/activate

4) py manage.py makemigrations

5) py manage.py migrate

6) py manage.py runserver

3 keyin 6 buyruqlar har safar serverni yoqish uchun ishlatiladi.
Agar gitdan pull qilinsa 3, 4, 5, 6 buyruqlar ketma-ket yoziladi.