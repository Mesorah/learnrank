# LearnRank


O **LearnRank** é uma plataforma inteligente de aprendizado de idiomas que utiliza IA para personalizar atividades e otimizar o progresso do aluno.
O usuário não apenas pratica, mas também evolui com planos montados pelo sistema, que analisa erros, vocabulário e desempenho em tempo real.

### Objetivo:
Transformar o aprendizado de línguas **tranquilo, conciso e moldado**, para uma fluência mais rápida, com o uso de feedbacks inteligentes, roadmaps eficientes para seu objetivo em específico.

---

## Status do Projeto

**Em desenvolvimento inicial.**

Atualmente em construção o módulo **Authors**, responsável por:
- Registro, login e logout de usuários.
- Recuperação e redefinição de senhas.
- Alteração de nome de usuário.
- Exclusão de conta.

---

### Próximos módulos planejados:
- Geração automática de **exercícios personalizados**.
- Sistema de **níveis e progresso** baseado em IA.

---

## Tecnologias Utilizadas (até o momento)
- **Python 3.10+**
- **Django 5.x**
- **SQLite**
- **Django REST Framework**
- **HTML, CSS e JavaScript**

---

## Instalação do Projeto

```bash
# Clonar o repositório
git clone https://github.com/Mesorah/learnrank.git
cd learnrank

# Criar ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar migrações
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```
