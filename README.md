# 🌍 Travel Assistant Chat

An intelligent travel planning assistant that demonstrates advanced conversational AI capabilities through natural language processing, external API integration, and sophisticated prompt engineering techniques.

## 📋 Project Overview

This travel assistant is designed to handle diverse travel-related queries while maintaining natural, contextual conversations. The system combines LLM capabilities with real-time data from external APIs to provide accurate, helpful travel advice.

### Core Capabilities

- **Destination Recommendations & Attractions**: Get personalized suggestions for places to visit
- **Packing Lists**: Customized packing suggestions based on destination and weather
- **Local Attractions**: Discover museums, historical sites, and points of interest
- **Weather Forecasting**: Real-time weather data for travel planning
- **Currency Exchange**: Current exchange rates for budget planning

## 🏗️ Architecture

### System Components

1. **Conversation Manager**: Handles chat history, context management, and response verification
2. **Travel Tools**: External API integrations for real-time data
3. **Prompt Engineering System**: Advanced prompting with chain-of-thought reasoning
4. **Verification Layer**: Quality control using a separate LLM for response validation
5. **Gradio Interface**: User-friendly web interface for testing

### Technical Stack

- **Language**: Python 3.8+
- **LLM Provider**: Google Gemini (2.5 Flash & 2.5 Pro)
- **Interface**: Gradio
- **External APIs**:
  - OpenWeatherMap (Weather data)
  - OpenTripMap (Attractions & POI)
  - ExchangeRate-API (Currency conversion)

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- API keys for external services

### Step 1: Clone and Install Dependencies

```bash
git clone <repository-url>
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
│   ├── constants.py        # Configuration constants
│   ├── prompts/
│   │   ├── prompts.py      # System prompts and examples
│   │   └── schemas.py      # JSON schemas for structured responses
│   └── utils/
│       └── utils.py        # Utility functions
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
└── README.md              # This file
```

## 🎯 Key Features

### 1. Conversation-First Design
- Maintains context across multiple exchanges
- Handles follow-up questions naturally
- Supports complex, multi-part queries

### 2. Chain-of-Thought Reasoning
- Explicit reasoning steps in prompts
- Decision-making transparency
- Tool selection logic

### 3. Response Verification
- Dual-model verification system
- Automatic error detection and correction
- Quality assurance layer

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

3. **Budget Planning**:
   ```
   User: "How much is 500 USD in Japanese Yen?"
   Assistant: [Gets current exchange rates and calculates conversion]
   ```

### Try These Examples
- "What are the best beaches in Thailand for October?"
- "I'm traveling to London tomorrow, what should I pack?"
- "Show me historical attractions in Rome"
- "What's the weather like in New York this weekend?"

## 🔧 Configuration

### Conversation Settings
- **Max History**: 10 exchanges (configurable in `ConversationManager`)
- **API Timeouts**: Standard timeout handling for all external APIs
- **Response Streaming**: Real-time response generation

### Model Configuration
- **Primary Model**: Gemini 2.5 Flash (for main conversations)
- **Verification Model**: Gemini 2.5 Pro (for response validation)

## 🛡️ Error Handling

The system implements robust error handling:

- **API Failures**: Graceful fallback to LLM knowledge
- **Rate Limiting**: Built-in retry logic
- **Invalid Inputs**: User-friendly error messages
- **Network Issues**: Timeout handling and recovery

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

## 🤝 Future Improvements

- Additional API integrations (Hotels, Flights, etc.)
- Extended conversation memory
- Advanced personalization features
