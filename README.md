# TradeFlood

**TradeFlood** is a flexible and extensible data acquisition framework designed for seamless integration with trading exchanges like Binance, Bitget, and Forex platforms. It provides a powerful mechanism for binding data models and collection logic, handling both historical and real-time data, all orchestrated through a modular system of connectors, bindings, and proxy routing.

---

## 📌 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Components](#components)
  - [Connectors](#connectors)
  - [Bindings](#bindings)
  - [Models](#models)
  - [Proxyter](#proxyter)
- [Modes of Operation](#modes-of-operation)
- [Request Lifecycle](#request-lifecycle)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Future Plans](#future-plans)
- [Contributing](#contributing)
- [License](#license)

---

## 🧠 Introduction

TradeFlood is more than a simple data harvester — it's a framework that allows rapid integration of custom collection flows from diverse trading data sources. Its modular structure emphasizes **extensibility**, making it suitable for evolving trading environments and high-volume data demands.

> 💡 **Design Principle**: Everything is extensible — even third-party modules.

---

## ✨ Features

- 🔌 Modular system for connecting to multiple exchanges
- 🔁 Real-time & historical data collection via WebSocket, Callback, LongPoll, and REST APIs
- 🔗 Dynamic binding system for flexible model-building
- 🧩 Strategy-based query planning to avoid redundant requests
- 🛡️ Integrated proxy service (`Proxyter`) with smart routing & error diagnostics
- 🐳 Dockerized server for running as an API interface
- 🧵 Declarative collection flows using decorators (`@turn_execution`)
- 📦 Usable both as a standalone service or a Python library

---

## 🏗️ Architecture Overview

```
Client Request
     │
     ▼
  Binding Layer
     │
     ▼
Turn Execution Logic (@turn_execution)
     │
     ▼
 Proxy Scheme → Proxyter (Go Service)
     │
     ▼
  Exchange Connector
     │
     ▼
  Model Assembly
     │
     ▼
   Response
```

---

## 🧰 Installation

### Prerequisites

- Python 3.10+
- Docker (for API server and Proxyter)
- Go (to compile the Proxyter service)

### Setup

```bash
git clone https://github.com/your-username/tradeflood.git
cd tradeflood
pip install -r requirements.txt
```

To build and run the Docker API interface:

```bash
docker-compose up --build
```

To compile and run the Proxyter service (in Go):

```bash
cd proxyter
go build -o proxyter
./proxyter
```

---

## 🚀 Usage

TradeFlood can be used both as a library or via its server API.

### Library Example

```python
from tradeflood.connectors import BitgetConnector
from tradeflood.bindings import BitgetCandleBinding

connector = BitgetConnector()
data = connector.fetch("BTC/USDT", "candles")
print(data)
```

### Server API Example

```http
POST /api/fetch
Content-Type: application/json

{
  "exchange": "bitget",
  "symbol": "BTC/USDT",
  "datatype": "candles"
}
```

---

## ⚙️ Configuration

Configurations for Proxyter, connectors, and bindings can be defined in `.yaml` or `.json` formats. Each proxy group supports:

- Max connections
- Load distribution strategy
- Failover settings
- Diagnostic callbacks

---

## 🔌 Components

### Connectors

Connectors handle all external API communication with exchanges.

- `BitgetConnector`
- `BinanceConnector`
- `ForexConnector`

Each connector uses decorators like `@turn_execution` to define actionable endpoints.

---

### Bindings

Bindings define how to associate models with connectors, handle request routing, and process responses.

Example:

```python
class BitgetCandleBinding:
    def __call__(self, connector: BitgetConnector):
        @turn_execution
        def get_candles():
            return connector.get_candles_request()
```

---

### Models

Models represent data structures like:

- Candles
- Order Books
- Ticker snapshots
- Custom financial indicators

---

### Proxyter

A standalone Go service for managing intelligent proxy routing.

Features:

- Load-balancing across proxy pools
- Failure diagnosis
- Proxy health checks
- Dynamic reconfiguration

---

## 🧭 Modes of Operation

| Mode                | Description                        |
|---------------------|------------------------------------|
| WebSocket           | For real-time streaming data       |
| Callback            | For data push mechanisms           |
| Long Polling        | Alternative real-time fetching     |
| REST API            | For historical data acquisition    |

> A connector can define multiple modes based on exchange capabilities.

---

## 🔄 Request Lifecycle

1. **Request Initiated** – API or direct library call
2. **Binding Evaluation** – Relevant bindings selected
3. **Turn Execution** – Strategy for query collection built
4. **Proxy Routing** – Load-balanced request dispatch
5. **Model Building** – Results packaged into defined data models
6. **Response Returned** – Final output sent to the user

---

## 🧪 Examples

### Adding a New Connector

```python
class MyExchangeConnector(Connector):
    @turn_execution
    def get_data():
        # implement API logic
        pass
```

### Adding a New Binding

```python
class MyDataBinding:
    def __call__(self, connector):
        @turn_execution
        def fetch_data():
            return connector.get_data()
```

---

## 🛠 Troubleshooting

- **Proxy errors?** Ensure `Proxyter` is running and accessible.
- **Empty responses?** Check if bindings are properly linked to connectors.
- **Slow response time?** Tune the proxy group settings and load balancing strategy.

---

## 📅 Future Plans

- [ ] Add UI dashboard for proxy status and API monitoring
- [ ] Create a connector/binding generator CLI
- [ ] Add more out-of-the-box bindings for common exchanges
- [ ] Publish Proxyter as a standalone open-source service

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a new branch
3. Submit a pull request

Also, feel free to open an issue for any bug reports or feature suggestions.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
