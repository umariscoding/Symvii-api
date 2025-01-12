from fastapi import APIRouter, HTTPException
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/ai-doctor", tags=["AI Doctor"])
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@router.post("")
async def get_ai_consultation(consultation_data: dict):
    """
    Get AI doctor consultation based on user input
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical AI assistant providing consultations."
                },
                {
                    "role": "user",
                    "content": f"""Given these patient details:
Symptoms: {consultation_data.get('symptom')}
Sex: {consultation_data.get('sex')}
Age: {consultation_data.get('age')}
Country visited: {consultation_data.get('country')}

Provide a concise summary of the potential medical issue and recommended actions. If the condition appears complex, provide a more detailed explanation. Use simple language and avoid medical jargon. use words like 'you' and 'your'. Never return result in form of bullets or points or list. always return result in paragraph format."""
                }
            ]
        )

        response_text = completion.choices[0].message.content

        return {
            "message": "Consultation generated successfully",
            "data": {
                "consultation": response_text,
                "original_input": {
                    "symptom": consultation_data.get("symptom"),
                    "sex": consultation_data.get("sex"),
                    "age": consultation_data.get("age"),
                    "country": consultation_data.get("country")
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 