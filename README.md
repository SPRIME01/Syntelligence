# 🧠 Syntelligence

> 🚀 Transform Your Thinking with AI-Enhanced Syntelligence

[![Build Status](https://img.shields.io/github/workflow/status/username/cognitive-workspace/CI?style=flat-square)](https://github.com/username/cognitive-workspace/actions)
[![License](https://img.shields.io/badge/license-GPL%20v3-blue.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.13+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/typescript-4.9+-blue.svg?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

## 🌟 Vision

Syntelligence is your digital command center for knowledge work—where artificial intelligence meets human intelligence. Our platform provides a unified environment that adapts to your thinking process, seamlessly integrating advanced AI capabilities with intuitive knowledge management tools.

At its core, Syntelligence transforms knowledge work by providing an AI-enhanced workspace where thinking processes are externalized through dynamic cognitive artifacts that evolve into polished intellectual outputs. The platform helps you capture insights, make connections, and develop ideas with unprecedented clarity and speed.

Whether you're researching, writing, analyzing data, or solving complex problems, Syntelligence augments your cognitive abilities by eliminating busywork, allowing you to focus on creating meaningful work that makes an impact. Experience the next evolution in knowledge work: a true partnership between human creativity and machine intelligence.

## ✨ Key Features

- 🗣️ **AI-Powered Conversation System** - Engage with specialized AI assistants to explore ideas and generate insights
- 📝 **Dynamic Cognitive Artifacts** - Externalize thinking processes with structured templates
- 🔄 **Artifact Transformation** - Convert rough cognitive artifacts into polished intellectual outputs
- 🤖 **Customizable Agents** - Create specialized AI agents to assist with specific thinking tasks
- 🧩 **Knowledge Graph** - Connect and discover relationships between ideas and artifacts
- 👥 **Collaborative Workspace** - Work together with team members on shared thinking processes

## 🏗️ Architecture

Syntelligence follows **Domain-Driven Design** and **Clean Architecture** principles:

- 🧩 **Hexagonal Architecture** (Ports & Adapters) for flexible integration
- 📣 **Event-Driven Architecture** using message bus for loose coupling
- 🧱 **Monorepo Structure** that can easily evolve to microservices
- 🔍 **Domain-Focused Organization** with clear bounded contexts

![Architecture Diagram](./docs/architecture/architecture-overview.png)

## 🛠️ Tech Stack

### Backend
- 🐍 Python 3.10+
- 🚀 FastAPI for REST APIs
- 📩 RabbitMQ for message broker
- 📊 PostgreSQL for structured data
- 📝 MongoDB for document storage
- 🕸️ ArangoDB for knowledge graph

### Frontend
- ⚛️ React with TypeScript
- 🎨 Styled Components
- 🧠 Redux Toolkit for state management
- 📊 D3.js for visualizations
- 🎞️ Motion for animation

## 📋 Prerequisites

- 🐳 Docker and Docker Compose
- 🐍 Python 3.10+
- 📦 Node.js 16+
- 📦 NPM
- 📝 UV (Python dependency management)

## 🚀 Getting Started

### 🔧 Installation

1. **Clone the repository**

```bash
git clone https://github.com/sprime01/syntelligence.git
cd syntelligence
```

2. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start the development environment**

```bash
# Start all services using Docker
npm run dev

# Or start only specific components
npm run client
npm run services
```

4. **Access the application**

- 🌐 Frontend: [http://localhost:3000](http://localhost:3000)
- 📚 API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

## 💻 Development Workflow

### 🏗️ Project Structure

```
cognitive-workspace/
├── .github/                      # GitHub workflows
├── docs/                         # Documentation
├── packages/                     # Shared packages
├── services/                     # Backend services
│   ├── api-gateway/              # API Gateway service
│   ├── conversation-service/     # Conversation management
│   ├── artifact-service/         # Artifact management
│   └── ...                       # Other services
├── client/                       # Frontend application
└── infrastructure/               # Infrastructure config
```

### 🔄 Common Tasks

```bash
# Run tests
npm run test

# Lint code
npm run lint

# Format code
npm run format

# Build for production
npm run build
```

## 🧪 Testing

We use a comprehensive testing strategy:

- 🧩 **Unit Tests** - Test individual components in isolation
- 🔄 **Integration Tests** - Test interactions between components
- 🌐 **End-to-End Tests** - Test complete user flows

Run tests with:

```bash
# Run all tests
npm run test

# Run specific service tests
cd services/conversation-service
uv run pytest
```

## 📚 Documentation

- 📖 [Architecture Overview](./docs/architecture/README.md)
- 🧩 [Domain Model](./docs/domain-model/README.md)
- 🔌 [API Documentation](./docs/api/README.md)
- 🚀 [Deployment Guide](./docs/deployment/README.md)

## 🤝 Contributing

We welcome contributions to syntelligence! Please check out our [Contributing Guide](CONTRIBUTING.md) to learn more about:

- 🐛 Reporting issues
- 🌱 Feature requests
- 🛠️ Pull requests
- 📝 Coding standards
- 🧪 Testing requirements


## 📊 Project Status

syntelligence is currently in **Alpha** development. We're actively working on core features and stabilizing the architecture.

- ✅ Conversation System
- ✅ Basic Cognitive Artifacts
- 🚧 Artifact Transformation
- 🚧 Agent System
- 📅 Knowledge Graph (Planned)
- 📅 Collaborative Features (Planned)

## 📜 License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.



---

⭐ If you find this project useful, please consider giving it a star!

