
from flask import Flask, request, render_template
import openai

app = Flask(__name__)

# Replace this with your OpenAI API key
openai.api_key = "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"

def generate_description(product_name, keywords):
    # Construct the prompt for OpenAI
    prompt = f"""
    Write a compelling product description for {product_name},
    incorporating these keywords: {', '.join(keywords)}.
    The description should be engaging, informative, and highlight the product's key features.
    Focus on benefits and value to the customer.
    Product Description:
    """
    
    try:
        # Call OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error generating description: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    description = None
    error = None
    
    if request.method == 'POST':
        try:
            product_name = request.form['product_name']
            # Split keywords and remove any extra whitespace
            keywords = [k.strip() for k in request.form['keywords'].split(',')]
            
            if product_name and keywords:
                description = generate_description(product_name, keywords)
            else:
                error = "Please provide both product name and keywords."
                
        except Exception as e:
            error = f"An error occurred: {str(e)}"
    
    return render_template('index.html', description=description, error=error)

if __name__ == '__main__':
    app.run(debug=True)