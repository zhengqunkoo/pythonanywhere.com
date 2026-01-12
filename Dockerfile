FROM python:3.13-alpine
LABEL maintainer="zhengqun.koo@gmail.com"
COPY . /
WORKDIR /
RUN pip install -r requirements.txt
#EXPOSE 80
ENTRYPOINT ["python"]
CMD ["main.py"]