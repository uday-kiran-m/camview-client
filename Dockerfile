#DOCKER_BUILDKIT=1
FROM ubuntu
COPY . /app
RUN apt update && apt upgrade -y
WORKDIR /app
RUN apt install python3 -y
RUN apt install python3-pip -y
# RUN apt install python3-opencv -y 6
# RUN pip install -r requirements.txt

EXPOSE 8000

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
