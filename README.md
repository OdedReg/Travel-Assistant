# <div align="center">🌍 Travel Assistant Chat</div>

<div align="center">An intelligent travel planning agent with advanced conversational AI capabilities</div>
<br>
<p align="center">
  <img src="travel_image.png" width="700">
</p>

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#️-architecture)
- [Installation & Setup](#-installation--setup)
- [Project Structure](#-project-structure)
- [Key Features](#-key-features)
- [Usage Examples](#-usage-examples)
- [Error Handling](#️-error-handling)
- [Response Verification System](#-response-verification-system)
- [Limitations](#-limitations)
- [Future Improvements](#-future-improvements)

## 📋 Project Overview

This travel assistant is designed to handle diverse travel-related queries while maintaining natural, contextual conversations. The system combines LLM capabilities with real-time data from external APIs to provide accurate, helpful travel advice.

### Core Capabilities

- **Destination Recommendations & Attractions**: Get personalized suggestions for places to visit
- **Weather Forecasting**: Real-time weather data for travel planning
- **Packing Lists**: Customized packing suggestions based on destination and weather
- **Currency Exchange**: Current exchange rates for budget planning
- **Local Attractions**: Discover museums, historical sites, and points of interest

## 🏗️ Architecture

### System Components

1. **Conversation Manager**: Handles chat history, context management, and response verification
2. **Travel Tools**: External API integrations for real-time data
3. **Prompt Engineering System**: Advanced prompting with chain-of-thought reasoning
4. **Verification Layer**: Quality control using a separate LLM for response validation
5. **Gradio Interface**: User-friendly web interface for testing

### Technical Stack

- **Language**: Python 3.12.11
- **LLM Provider**: Google Gemini (2.5 Flash & 2.5 Pro)
- **Interface**: Gradio
- **External APIs**:
  - OpenWeatherMap (Weather data)
  - OpenTripMap (Attractions & POI)
  - ExchangeRate-API (Currency conversion)

## 🚀 Installation & Setup

### Prerequisites

- Python 3.12.11 or compatible version
- API keys for external services

### Step 1: Clone and Install Dependencies

```bash
git clone https://github.com/OdedReg/Travel-Assistant
pip install -r requirements.txt
```

### Step 2: Environment Setup

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
OPEN_TRIP_MAP_API_KEY=your_opentripmap_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
EXCHANGERATE_API_KEY=your_exchangerate_api_key_here
```

### Step 3: API Key Setup

1. **Google Gemini API**: Get your key from [Google AI Studio](https://aistudio.google.com)
2. **OpenTripMap**: Sign up at [opentripmap.io](https://opentripmap.io/product)
3. **OpenWeatherMap**: Register at [openweathermap.org](https://openweathermap.org/api)
4. **ExchangeRate-API**: Get a free key at [exchangerate-api.com](https://exchangerate-api.com)

### Step 4: Run the Application

```bash
python main.py
```

The application will launch at `http://127.0.0.1:7860`

## 📁 Project Structure

```
travel-assistant/
├── main.py                 # Gradio web interface
├── src/
│   ├── travel_assistant.py # Main conversation logic
│   ├── travel_tools.py     # External API integrations
│   ├── constants.py        
│   ├── prompts/
│   │   ├── prompts.py      # System prompts and examples
│   │   └── schemas.py      # JSON schemas for structured responses
│   └── utils/
│       └── utils.py        
├── requirements.txt        
├── .env                   
└── README.md              
```

## 🎯 Key Features

### 1. Conversation-First Design
- Maintains context across multiple exchanges
- Handles follow-up questions naturally

### 2. Chain-of-Thought Reasoning
- Explicit reasoning steps in prompts
- Conditional chain of thought example
- Tool selection logic

### 3. Response Verification
- Stronger model used for verification
- Automatic error detection and correction

### 4. Smart Data Integration
- Intelligent decision-making between API data and LLM knowledge
- Graceful fallback handling
- Real-time data when available, knowledge-based responses when not

## 💡 Usage Examples

### Example Conversations

1. **Attraction Discovery**:
   ```
   User: 
   "What are the most famous water parks near Tel Aviv?"
   
   Assistant: 
   The most famous water parks near Tel Aviv are:
   * **Meimadyon**: Located in Yarkon Park in northern Tel Aviv, it's considered one of the largest in Israel, spanning 100 dunams. It was established in 1990 and attracts tens of thousands of visitors in the summer.
   * **Yamit 2000**: Situated in southeastern Holon, near Peres Park, this water park is also one of the largest in Israel. It started as a municipal pool in 1978 and expanded over the years.
   ```

2. **Weather-Based Packing**:
   ```
   User: 
   "Create a packing list for Paris in May"
   
   Assistant: 
   For a business trip to Paris in May, you can expect mild and pleasant weather, but it's always wise to be prepared for some rain. Here's a suggested packing list:
   **Clothing:**
   * **Business Attire:**
      * Suits or business casual outfits (blazers, dress shirts, blouses, smart trousers/skirts)
      * Formal shoes
      * Ties/accessories
   * **Casual Wear (for evenings or free time):**
      * Comfortable walking shoes (you'll likely do a lot of walking!)
      * Jeans or smart casual trousers
      * Light sweaters or cardigans
      * A few versatile tops
   * **Outerwear:**
      * A trench coat or a stylish, lightweight waterproof jacket
      * A compact umbrella
   **Essentials:**
   * **Toiletries:** All your personal care items.
   * **Medications:** Any prescription medications you need, plus basic over-the-counter remedies.
   * **Travel Adapter:** France uses Type E power sockets, so ensure you have the correct adapter for your electronics.
   * **Portable Charger:** Useful for keeping your devices charged on the go.
   * **Documents:** Passport, visa (if required), flight tickets, hotel reservations, business contacts, and any conference materials.
   * **Currency/Credit Cards:** Euros are the local currency. Inform your bank of your travel plans.
   **Other items:**
   * Small day bag or stylish tote for daily essentials.
   * Reusable water bottle.
   ```

3. **Destination Recommendations (with Verification Pipeline)**:
   ```
   User: 
   "Recommended destinations for a beach vacation in October"
   
   Assistant:
   [Initial Response]: 
   For a beach vacation in October, here are some excellent recommendations:
   * **The Caribbean:** Islands like **Barbados, St. Lucia, and Turks and Caicos** offer warm temperatures, low humidity, and minimal rainfall in October as it's typically outside the peak hurricane season.
   * **Maldives:** This is a fantastic choice for a luxurious beach getaway with consistently warm weather and clear waters, perfect for snorkeling and diving. October marks the transition to the dry season, meaning less rain.
   * **Fiji:** Enjoy tropical warmth, stunning coral reefs, and pristine beaches. October is a great time to visit as it falls within their dry season.
   * **Hawaii, USA:** Islands like **Maui and Kauai** offer beautiful beaches and warm weather. October is generally a pleasant month to visit before the winter crowds.
   * **Southeast Asia (Thailand, Vietnam):** While some parts might experience the tail end of the monsoon, destinations like **Phuket in Thailand** and **Phu Quoc in Vietnam** start entering their dry season in October, offering sunny days and calm waters.
   
   [Verification System Detects Error]: 
   I apologize, but my response contained inaccurate information. Let me provide you with a corrected answer...
   
   [Final Response]:
   For a beach vacation in October, here are some recommended destinations, keeping in mind typical weather patterns:
   **Maldives:** October marks the very end of the wet season in the Maldives, transitioning towards the dry season. While you might still experience some brief rain showers, these are usually short-lived, and you can expect plenty of sunshine.
   **Fiji:** October is an excellent time to visit Fiji. It falls within their dry season, offering warm temperatures, low humidity, and plenty of sunshine.
   **Hawaii, USA:** October in Hawaii generally offers pleasant weather with warm temperatures and less humidity compared to summer.
   **Seychelles:** October is a great month to visit the Seychelles. It's a transitional period between the southeast trade winds and the northwest monsoon.
   **Egypt (Red Sea Coast):** Consider the Red Sea coast in Egypt (e.g., Sharm El Sheikh, Hurghada). October offers pleasant temperatures, making it ideal for relaxing on the beach.
   **Important Note for Caribbean:** October is still within the peak Atlantic hurricane season, so it's generally not recommended to plan a beach vacation to the Caribbean during this time.
   ```

## 🛡️ Error Handling

The system implements robust error handling:

- **API Failures**: Graceful fallback to LLM knowledge
- **Rate Limiting**: Built-in retry logic
- **Invalid Inputs**: User-friendly error messages
- **Timeout handling**: Recovery mechanisms for external APIs

## 🔄 Response Verification System

The assistant uses a dual-model approach:

1. **Primary Response**: Generated by Gemini 2.5 Flash with tool access
2. **Verification**: Response validated by Gemini 2.5 Pro
3. **Correction**: Automatic regeneration if issues are detected

## 🚦 Limitations

- Weather forecasts limited to 5 days ahead
- Attraction data dependent on OpenTripMap coverage
- Exchange rates updated daily (not real-time)
- Limited conversation history (10 exchanges) to manage token usage

## 🚀 Future Improvements

- **Additional API integrations** (Hotels, Flights, etc.)
- **Extended conversation memory**
- **Advanced personalization features**
