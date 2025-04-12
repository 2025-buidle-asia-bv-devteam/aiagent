# 🌟 Eau d'Intelligence: The Master Perfumer AI Agent

<div align="center">
  <img src="https://img.shields.io/badge/Powered%20by-OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="Powered by OpenAI" />
  <img src="https://img.shields.io/badge/Built%20with-Eliza-008080?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiwxLjVBMTAuNSwxMC41LDAsMSwwLDIyLjUsMTIsMTAuNTEsMTAuNTEsMCwwLDAsMTIsMS41Wk0yMCwxMS42M2gtM2E3Ljc2LDcuNzYsMCwwLDAtMS41MS00LjY1TDE4LDQuODRBOC40NSw4LjQ1LDAsMCwxLDIwLDExLjYzWk0xMywxMS42M1YzLjc2YTcuNzgsNy43OCwwLDAsMSw0LjM1LDMuMTksOC4zNSw4LjM1LDAsMCwxLDEuMjcsNC42OFptLTIsMFYzLjc2QTcuNzgsNy43OCwwLDAsMCw2LjY1LDYuOTVhOC4zNSw4LjM1LDAsMCwwLTEuMjcsNC42OFptLTgsMFY0LjgzYTguMzQsOC4zNCwwLDAsMSwzLjM0LDIuMTVBNy43Niw3Ljc2LDAsMCwwLDcsMTEuNjNaTTQsMTIuMzdINy4wNWE3Ljc2LDcuNzYsMCwwLDAsMS41MSw0LjY1TDYsMTkuMTdBOC40NSw4LjQ1LDAsMCwxLDQsMTIuMzdabTktLjc0djcuODdhNy43OCw3Ljc4LDAsMCwxLTQuMzUtMy4xOUE4LjM1LDguMzUsMCwwLDEsNy40MSwxMS42M1ptMiwwdjcuODdBNy43OCw3Ljc4LDAsMCwwLDE3LjM1LDE2LjMxYTguMzUsOC4zNSwwLDAsMCwxLjI3LTQuNjhabTgsLS43NFYxOS4xN2E4LjM0LDguMzQsMCwwLDEtMy4zNC0yLjE1QTcuNzYsNy43NiwwLDAsMCwxNywxMi4zN1oiLz48L3N2Zz4=" alt="Built with Eliza" />
  <img src="https://img.shields.io/badge/Craft-Perfumery-FF69B4?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNSAyIDIgNi41IDIgMTJzNC41IDEwIDEwIDEwIDEwLTQuNSAxMC0xMFMxNy41IDIgMTIgMm0wIDE4YTggOCAwIDAgMS04LThzMyAzIDggMyA4LTMgOC0zYTggOCAwIDAgMS04IDgiLz48L3N2Zz4=" alt="Craft Perfumery" />
</div>

## ✨ Introduction

**Eau d'Intelligence** is an extraordinary AI Agent that combines the therapeutic conversation style of Eliza with the sophisticated intelligence of OpenAI to create a unique virtual perfumer. With the persona of a master perfumer, this agent guides you through the art and science of fragrance creation, offering personalized scent recommendations and inspiring your olfactory imagination.

Unlike traditional chatbots, our AI Agent understands the complex language of scents, notes, and accords. It can transform your abstract descriptions like "I want something moody and rainy" into detailed perfume formulations with precise top, middle, and base notes.

## 🧪 Features

- **Creative Perfume Formulation**: Receive detailed fragrance recipes with top, middle, and base notes
- **Personalized Scent Recommendations**: Describe your mood or desired atmosphere and get tailored suggestions
- **Manufacturing Guidance**: Learn how to blend and create your custom scents with step-by-step instructions
- **Olfactory Education**: Expand your knowledge about fragrance families, notes, and perfumery techniques
- **JSON-formatted Output**: Perfectly structured data for integration with other applications

## 🛠️ Installation & Setup

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   
   # Eliza configuration
   USE_ELIZA=true
   ELIZA_API_URL=http://localhost:3001
   ```

## 🔍 Running Modes

### Direct OpenAI Mode
- Uses OpenAI API directly for fragrance recommendations
- Set `USE_ELIZA=false` in your `.env` file

### Mock Eliza Server Mode (Recommended for Testing)
- Uses the included mock Eliza server
- Enables testing of the Eliza API format without setting up the actual infrastructure

To activate:
1. Start the mock Eliza server:
   ```bash
   python src/mock_eliza_server.py
   ```
2. Verify server status:
   ```bash
   python src/check_eliza.py
   ```
3. Set `USE_ELIZA=true` in your `.env` file

### Full Eliza Server Mode (Advanced)
- Process requests through actual Eliza infrastructure
- Benefits from advanced caching, enhanced logging, and additional features
- Requires Node.js 23.3.0 and pnpm

To activate:
1. Install required tools:
   ```bash
   npm install -g pnpm
   ```
2. Start Eliza server:
   ```bash
   # From project root
   PORT=3001 pnpm start
   
   # Or just DirectClient
   cd packages/client-direct && PORT=3001 pnpm dev
   ```
3. Set `USE_ELIZA=true` in your `.env` file

## 💫 Usage

1. Start the perfume agent:
   ```bash
   python src/main.py
   ```
   
   Or run the FastAPI server:
   ```bash
   uvicorn api.fastapi_app:app --reload
   ```

2. Describe your desired fragrance style:
   ```
   "I want something smoky and mysterious with a hint of sweetness"
   ```

3. Receive a detailed perfume formulation in beautiful JSON format:
   ```json
   {
     "top_note": {
       "name": "Smoked Bergamot",
       "ratio": 20,
       "description": "A vibrant citrus note infused with smoky undertones, creating a mysterious opening"
     },
     "middle_note": {
       "name": "Dark Cherry Blossom",
       "ratio": 30,
       "description": "A semi-sweet floral heart with enigmatic depth and subtle fruity nuances"
     },
     "base_note": {
       "name": "Amber Resin",
       "ratio": 50,
       "description": "A rich, warm foundation with honeyed sweetness and a lingering smoky character"
     },
     "manufacturing_guide": {
       "ethanol": 75,
       "water": 5,
       "steps": [
         "Blend the top and middle notes with ethanol",
         "Add the base note and mix thoroughly",
         "Add filtered water while stirring",
         "Allow to mature for 3-4 weeks in a cool, dark place",
         "Filter and bottle your creation"
       ]
     },
     "description": "A captivating fragrance that balances smoky mystery with subtle sweetness, evoking the atmosphere of twilight in an ancient forest"
   }
   ```

## 🌐 API Integration

Eau d'Intelligence offers a FastAPI microservice for integration with web applications and other services. Access the interactive API documentation at http://localhost:8000/docs when running the FastAPI server.

## 📚 Project Structure

- `src/agent.py`: Core agent logic with OpenAI and Eliza integration
- `src/mock_eliza_server.py`: Mock Eliza API server for testing
- `src/check_eliza.py`: Eliza server status verification tool
- `src/main.py`: Main execution file
- `api/fastapi_app.py`: FastAPI service for web integration
- `knowledge/perfume_data.json`: Reference data for perfume formulations

## 🪄 Experience the Art of Perfumery

Unleash your creativity and explore the world of scents with Eau d'Intelligence. Whether you're a perfume enthusiast, a professional seeking inspiration, or simply curious about fragrance creation, our AI Agent will guide you on an enchanting olfactory journey.

<div align="center">
  <em>Where Artificial Intelligence meets the Art of Perfumery</em>
</div>
