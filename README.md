# 🧠 Syntelligence

> 🚀 Transform Your Thinking with an AI-Enhanced Cognitive Workspace

[![Build Status](https://img.shields.io/github/workflow/status/username/cognitive-workspace/CI?style=flat-square)](https://github.com/username/cognitive-workspace/actions)
[![License](https://img.shields.io/badge/license-GPL%20v3-blue.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.13+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/typescript-4.9+-blue.svg?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

## 🌟 Vision

Cognitive Workspace transforms knowledge work by providing an AI-powered environment where thinking processes are externalized through dynamic cognitive artifacts that evolve into polished intellectual outputs. It's designed to augment human cognition, structure knowledge work, and enable effective human-AI collaboration.

## ✨ Key Features

- 🗣️ **AI-Powered Conversation System** - Engage with specialized AI assistants to explore ideas and generate insights
- 📝 **Dynamic Cognitive Artifacts** - Externalize thinking processes with structured templates
- 🔄 **Artifact Transformation** - Convert rough cognitive artifacts into polished intellectual outputs
- 🤖 **Customizable Agents** - Create specialized AI agents to assist with specific thinking tasks
- 🧩 **Knowledge Graph** - Connect and discover relationships between ideas and artifacts
- 👥 **Collaborative Workspace** - Work together with team members on shared thinking processes

## 🏗️ Architecture

Cognitive Workspace follows **Domain-Driven Design** and **Clean Architecture** principles:

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
- 🕸️ Neo4j for knowledge graph

### Frontend
- ⚛️ React with TypeScript
- 🎨 Styled Components
- 🧠 Redux Toolkit for state management
- 📊 D3.js for visualizations

## 📋 Prerequisites

- 🐳 Docker and Docker Compose
- 🐍 Python 3.10+
- 📦 Node.js 16+
- 🧶 Yarn
- 📝 Poetry (Python dependency management)

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
yarn dev

# Or start only specific components
yarn start:client
yarn start:services
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
yarn test

# Lint code
yarn lint

# Format code
yarn format

# Build for production
yarn build
```

## 🧪 Testing

We use a comprehensive testing strategy:

- 🧩 **Unit Tests** - Test individual components in isolation
- 🔄 **Integration Tests** - Test interactions between components
- 🌐 **End-to-End Tests** - Test complete user flows

Run tests with:

```bash
# Run all tests
yarn test

# Run specific service tests
cd services/conversation-service
poetry run pytest
```

## 📚 Documentation

- 📖 [Architecture Overview](./docs/architecture/README.md)
- 🧩 [Domain Model](./docs/domain-model/README.md)
- 🔌 [API Documentation](./docs/api/README.md)
- 🚀 [Deployment Guide](./docs/deployment/README.md)

## 🤝 Contributing

We welcome contributions to Cognitive Workspace! Please check out our [Contributing Guide](CONTRIBUTING.md) to learn more about:

- 🐛 Reporting issues
- 🌱 Feature requests
- 🛠️ Pull requests
- 📝 Coding standards
- 🧪 Testing requirements


## 📊 Project Status

Cognitive Workspace is currently in **Alpha** development. We're actively working on core features and stabilizing the architecture.

- ✅ Conversation System
- ✅ Basic Cognitive Artifacts
- 🚧 Artifact Transformation
- 🚧 Agent System
- 📅 Knowledge Graph (Planned)
- 📅 Collaborative Features (Planned)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



---

⭐ If you find this project useful, please consider giving it a star!

📧 **Contact:** [team@cognitive-workspace.com](mailto:team@cognitive-workspace.com)
