FROM python

COPY main.py /main.py

RUN apt update

RUN pip install "fastapi[standard]"

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0"]
