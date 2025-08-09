# <div align="center">🌍 Travel Assistant Chat</div>

<div align="center">An intelligent travel planning assistant with advanced conversational AI capabilities</div>
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
git clone <repository-url>
pip install -r requirements.txt
```

### Step 2: Environment Setup

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
OPEN_TRIP_MAP_API_KEY=your_opentripmap_api_key
EXCHANGERATE_API_KEY=your_exchangerate_api_key
```

### Step 3: API Key Setup

1. **Google Gemini API**: Get your key from [Google AI Studio](https://aistudio.google.com)
2. **OpenWeatherMap**: Register at [openweathermap.org](https://openweathermap.org/api)
3. **OpenTripMap**: Sign up at [opentripmap.io](https://opentripmap.io/product)
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
   User: "What are the top museums in Tokyo?"
   Assistant: [Uses OpenTripMap API to fetch current museum data]
   ```

2. **Weather-Based Packing**:
   ```
   User: "Create a packing list for Paris in May"
   Assistant: [Checks weather forecast, creates detailed packing list]
   ```

3. **Destination Recommendations**:
   ```
   User: "Recommended destinations for a beach vacation in October"
   Assistant: [Analyzes global beach destinations optimal for October travel]
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
