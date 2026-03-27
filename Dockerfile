FROM python:3.11-slim	
WORKDIR /app
COPY ..
RUN pip install --no-cashe-dir -r requirements.txt
CMD ["python", "run.py"]