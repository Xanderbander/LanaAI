import openai
import os

class OpenAIIntegration:
    def __init__(self, api_key):
        openai.api_key = api_key
    
    def generate_text(self, prompt):
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        if len(response.choices) > 0:
            return response.choices[0].text
        else:
            return ""

    def train_model(self, model_id, text_data):
        openai.Model.create(model_id, training_data=text_data)
        
    def generate_crypto_trading_decision(self, market_data):
        prompt = "Given the following market data, make a decision on whether to buy or sell:\n\n"
        prompt += market_data + "\n"
        prompt += "Decision:"
        decision = self.generate_text(prompt)
        return decision.strip()

if __name__ == "__main__":
    api_key = os.environ["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"]
    openai_integration = OpenAIIntegration(api_key)
    
    # Generate text example
    prompt = "The price of Bitcoin is currently $50,000. What will the price of Bitcoin be in 1 hour?"
    response = openai_integration.generate_text(prompt)
    print(response)

    # Train model example
    model_id = "my-custom-model"
    text_data = [
        "The price of Bitcoin is currently $50,000. I think the price will go up in the next hour.",
        "The price of Bitcoin is currently $50,000. I think the price will go down in the next hour."
    ]
    openai_integration.train_model(model_id, text_data)
    
    # Generate crypto trading decision example
    market_data = "Bitcoin price: $50,000\nEthereum price: $2,000\nMarket cap: $1.5 trillion\nTrading volume: $100 billion"
    decision = openai_integration.generate_crypto_trading_decision(market_data)
    print("Decision:", decision)
