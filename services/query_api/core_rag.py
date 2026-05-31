from google import genai
from google.genai import types
from shared.config import settings

def build_prompt(system_prompt: str, context_chunk: list[dict], user_query: str) -> str:
    
    """
    Builds a prompt for the language model by combining the system prompt, context chunks, and user query.
    
    Args:
        system_prompt (str): The system prompt providing instructions to the model.
        context_chunk (list[dict]): A list of context chunks, where each chunk is a dictionary containing 'chunk_text'.
        user_query (str): The user's query for which the answer is to be generated.
    
    Returns:
        str: The combined prompt to be sent to the language model.
    """

    context_text = "\n\n".join([f"Source {i}: {chunk['chunk_text']}" for i,chunk in enumerate(context_chunk, start=1)])

    prompt = f"{system_prompt}\n\nContext:\n{context_text}\n\nUser Query: {user_query}\n\nAnswer based only on the context above. If the answer is not in the context, say so.\n\nAnswer:"

    return prompt

def execute_inference(prompt: str, temperature: float, max_tokens: int, top_p: float = 0.95) -> str:

    """
    Executes inference using the Google Gemini API with the given prompt and generation configuration.

    Args:
        prompt (str): The prompt to be sent to the language model.
        temperature (float): The temperature setting for the generation, controlling randomness.
        max_tokens (int): The maximum number of tokens to generate in the response.
        top_p (float, optional): The nucleus sampling parameter to control diversity. Defaults to 0.95.
    
    Returns:
        str: The generated response from the language model.
    """
    
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    try:
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt,
            config = types.GenerateContentConfig(
                temperature = temperature,
                max_output_tokens = max_tokens,
                top_p = top_p
            )    
        )

        return response.text

    except Exception as e:
        print(f"Inference error: {e}")
        return "I was unable to generate a response. Please try again."