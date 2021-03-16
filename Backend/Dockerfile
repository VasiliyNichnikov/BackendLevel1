FROM python:3.8
ENV PYTHONUNBUFFERED 1
MAINTAINER Vasiliy Nichnikov 'v.nichnikov@gmail.com'
COPY . /app.py
COPY . /api.py
COPY . /generate_key_user.py
COPY . /DataBase/__all_models.py
COPY . /DataBase/db_session.py
COPY . /DataBase/product.py
COPY . /DataBase/user.py
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]