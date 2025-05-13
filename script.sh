#!/bin/bash

set -e

CLUSTER_NAME="livros"

echo "🔍 Verificando se Colima está instalado..."
if ! command -v colima &> /dev/null; then
  echo "❌ Colima não está instalado!"
  echo "💡 Instale com: brew install colima"
  exit 1
fi

echo "🔍 Verificando se kind está instalado..."
if ! command -v kind &> /dev/null; then
  echo "❌ kind (Kubernetes in Docker) não está instalado!"
  echo "💡 Instale com: brew install kind"
  exit 1
fi

echo "▶️ Iniciando a VM do Colima com Docker (rootful)..."
colima start --runtime docker --cpu 2 --memory 4096 --disk 20

echo "🔍 Verificando se Docker está rodando corretamente com Colima..."
if ! docker info > /dev/null 2>&1; then
  echo "❌ Docker (via Colima) não está acessível!"
  echo "💡 Algo deu errado com a inicialização. Tente: colima stop && colima start"
  exit 1
fi

echo "🔎 Verificando se o cluster kind \"$CLUSTER_NAME\" já existe..."
if kind get clusters | grep -q "$CLUSTER_NAME"; then
  echo "✅ Cluster \"$CLUSTER_NAME\" já existe. Reutilizando..."
else
  echo "🚀 Criando novo cluster Kubernetes com kind..."
  kind create cluster --name "$CLUSTER_NAME" --image kindest/node:v1.27.3
fi

echo "🐳 Buildando imagem da API com Docker..."
docker build -t livros-api:latest .

echo "📦 Carregando imagem no cluster kind \"$CLUSTER_NAME\"..."
kind load docker-image livros-api:latest --name "$CLUSTER_NAME"

echo "📄 Aplicando deployment no Kubernetes..."
kubectl apply -f deployment.yaml

echo "🌐 Aplicando service no Kubernetes..."
kubectl apply -f service.yaml

echo "⏳ Aguardando pod ficar disponível..."
kubectl wait --for=condition=available --timeout=60s deployment/livros-api

echo "🚪 Redirecionando porta para http://localhost:8000 ..."
kubectl port-forward service/livros-api-service 8000:80
