FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TOKEN_CODE=OVRL
ENV TOKEN_ISSUER=GBZH36ATUXJZKFRMQTAAW42MWNM34SOA4N6E7DQ62V3G5NVITC3QOVRL

EXPOSE 5000

CMD ["python", "main.py"]
