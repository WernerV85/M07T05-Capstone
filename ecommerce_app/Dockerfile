FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		pkg-config \
		default-libmysqlclient-dev \
		build-essential \
	&& rm -rf /var/lib/apt/lists/*

COPY requirement.txt /app/
RUN pip install --no-cache-dir -r requirement.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]