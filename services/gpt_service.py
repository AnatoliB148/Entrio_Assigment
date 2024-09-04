from openai import OpenAI
import services.logging_service as log

client = OpenAI(api_key='sk-svcacct-aW8rtIKf3COJybbprFk83s_54541536tF9EzS28iY8r0NveSA-5sNUh-29RvgKiM_VonvGBIurePKSwBT3BlbkFJmlaLaRHpjTDROYTm8hujnvfBWu-TDjBy-wW00aOCBt7pXMIsOPxVR9bQg_iz_1beNT8RZvOgcMHoA2IA')

def run_chat(system_prompt, user_prompt):
    log.info("Function - run_chat - Started")
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": str(user_prompt)}
        ],
        temperature=1
    )
    log.info("Function - run_chat - Done")
    # Extract and parse the response into a dictionary
    return response.choices[0].message.content
