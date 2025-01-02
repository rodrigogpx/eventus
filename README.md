# Eventus - Sistema de Gestão de Eventos

Eventus é um sistema web completo para gestão de eventos e encontros, desenvolvido com Flask e PostgreSQL. O sistema permite o gerenciamento de eventos, participantes, encontros e controle de presença.

## Funcionalidades

### Gestão de Eventos
- Criar, editar e excluir eventos
- Definir tema, data e descrição
- Estabelecer número máximo de participantes
- Visualizar lista de participantes por evento
- Gerenciar encontros dentro de cada evento

### Gestão de Participantes
- Cadastro de participantes com informações completas (nome, email, telefone, cidade)
- Associação de participantes a múltiplos eventos
- Importação em massa via arquivo Excel
- Exportação de lista de participantes para Excel
- Verificação de email duplicado
- Sistema de check-in

### Gestão de Encontros
- Criar encontros vinculados a eventos
- Definir título, data, hora e descrição
- Controle de presença dos participantes
- Relatórios de presença por encontro

### Área Administrativa
- Login seguro para administradores
- Dashboard com visão geral do sistema
- Métricas de participação
- Gestão completa de eventos e participantes
- Exportação de relatórios

## Requisitos Técnicos

- Python 3.8+
- PostgreSQL
- Docker e Docker Compose (para ambiente de desenvolvimento)

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/eventus.git
cd eventus
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

3. Inicie o ambiente com Docker:
```bash
docker-compose up -d
```

4. Acesse a aplicação:
```
http://localhost:5000
```

## Estrutura do Projeto

```
eventus/
├── app.py              # Aplicação principal
├── database/           # Modelos e configurações do banco
├── templates/          # Templates HTML
├── static/            # Arquivos estáticos (CSS, JS, imagens)
├── migrations/        # Scripts de migração do banco
├── config/           # Configurações do sistema
└── docker/           # Arquivos Docker
```

## Uso do Sistema

### Área Pública
1. Acesse a página inicial
2. Faça o check-in em eventos usando seu email
3. Visualize informações públicas dos eventos

### Área Administrativa
1. Acesse `/admin` e faça login
2. Use o menu lateral para navegar entre as funcionalidades
3. Gerencie eventos, participantes e encontros
4. Exporte relatórios conforme necessário

## Importação de Participantes

1. Baixe o template de importação em Excel
2. Preencha seguindo o modelo
3. Faça upload do arquivo na área administrativa
4. Verifique os resultados da importação

## Exportação de Dados

- Lista de participantes em Excel
- Relatórios de presença por encontro
- Dados formatados para análise

## Segurança

- Autenticação requerida para área administrativa
- Proteção CSRF em formulários
- Validação de dados em todos os inputs
- Sanitização de dados importados

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.

## Suporte

Para suporte, envie um email para [seu-email@dominio.com] ou abra uma issue no GitHub.
