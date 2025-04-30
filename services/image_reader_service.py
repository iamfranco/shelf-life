from io import BytesIO
from typing import List
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

import os
from dotenv import load_dotenv

from models.food_item import FoodItem
load_dotenv()

def analyze_image(image: BytesIO) -> List[FoodItem]:
  image.seek(0)

  ocr_endpoint = os.getenv("OCR_ENDPOINT")
  ocr_key = os.getenv("OCR_KEY")

  document_intelligence_client = DocumentIntelligenceClient(
    endpoint=ocr_endpoint,
    credential=AzureKeyCredential(ocr_key)
  )

  poller = document_intelligence_client.begin_analyze_document(
    model_id="prebuilt-receipt",
    body=image
  )

  receipts = poller.result()
  receipt_documents = receipts.documents

  if receipt_documents is None or len(receipt_documents) == 0:
    return []

  receipt_items = receipt_documents[0].fields['Items'].value_array

  food_items = [
    FoodItem(
      name=item.value_object['Description'].value_string,
      quantity=item.value_object['Quantity'].value_number,
      price=item.value_object['Price'].value_currency.amount,
      currency=item.value_object['Price'].value_currency.currency_code
    )
    for item in receipt_items
  ]

  return food_items