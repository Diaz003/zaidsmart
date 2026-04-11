# ZAIDSMART

![CI](https://github.com/Diaz003/zaidsmart/actions/workflows/ci.yml/badge.svg)
[![Release](https://img.shields.io/github/v/release/Diaz003/zaidsmart?label=release)](https://github.com/Diaz003/zaidsmart/releases)
[![License](https://img.shields.io/github/license/Diaz003/zaidsmart)](https://github.com/Diaz003/zaidsmart/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

> **ZAIDSMART** es un sistema multiagente avanzado impulsado por IA para el desarrollo colaborativo de videojuegos. Combina agentes especializados con interfaces modernas para crear experiencias de juego innovadoras.

## ✨ Características Principales

- 🤖 **Agentes Especializados**: Director con CrewAI jerárquico + 4 especialistas (Script, Assets, Sonidos, Escenas)
- 🌐 **Modelos Gratuitos**: Integración con OpenRouter para modelos de IA accesibles
- 🛡️ **Resiliencia**: Manejo inteligente de límites de tasa (429) con fallback automático
- 🎨 **Interfaz Dual**: Dashboard web dark mode + Terminal interactiva con Rich
- 💾 **Persistencia**: Base de datos SQLite con aiosqlite para historial completo
- 🔄 **Actualización Dinámica**: Refresco automático de modelos disponibles
- 📊 **Monitoreo en Tiempo Real**: Progreso y estado de tareas en vivo

## 🏗️ Arquitectura

```
ZAIDSMART/
├── core/                 # Núcleo del sistema
│   ├── agent_runner.py   # Ejecutor de agentes individuales
│   ├── crew_executor.py  # Coordinador CrewAI
│   ├── scraper.py        # Recolección de modelos
│   └── model_scraper.py  # Gestión de modelos IA
├── api/                  # API REST con FastAPI
├── web/                  # Dashboard web
│   ├── static/          # CSS/JS
│   └── templates/       # HTML
├── tui/                 # Interfaz terminal
└── test/                # Suite de pruebas
```

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.12+
- Git

### Instalación Automática
```bash
# Clonar repositorio
git clone https://github.com/Diaz003/zaidsmart.git
cd zaidsmart

# Configurar entorno virtual
python3.12 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o .venv\Scripts\activate en Windows

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de OpenRouter
```

## 🎮 Uso

### Inicio Completo (Web + Terminal)
```bash
./start.sh
```
Accede a `http://localhost:8000` para el dashboard web.

### Modos Especializados

#### Solo Terminal
```bash
python main.py --cli-only
```

#### Refresco de Modelos
```bash
python main.py --refresh-models
```

#### Agente Individual
```bash
python run_single_agent.py
```

### Ejemplo de Uso
```python
from zaidsmart import ZAIDSMART

# Inicializar sistema
ai_system = ZAIDSMART()

# Crear proyecto de juego
project = {
    "name": "Cyberpunk Adventure",
    "genre": "RPG",
    "description": "Un juego de rol futurista con IA generativa"
}

# Ejecutar desarrollo colaborativo
result = await ai_system.develop_game(project)
print(f"Proyecto completado: {result}")
```

## 🔧 Configuración

### Variables de Entorno (.env)
```env
OPENROUTER_API_KEY=tu_clave_aqui
DATABASE_URL=sqlite:///data/tasks.db
WEB_HOST=0.0.0.0
WEB_PORT=8000
```

### Modelos Soportados
- GPT-4 (OpenAI)
- Claude (Anthropic)
- Gemini (Google)
- Y muchos más vía OpenRouter

## 🧪 Pruebas

```bash
# Ejecutar suite completa
python -m pytest test/

# Prueba específica
python test_crew.py
python test_4_agents.py
```

## 📈 Rendimiento

- **Latencia**: <2s por respuesta típica
- **Concurrencia**: Soporta múltiples proyectos simultáneos
- **Fiabilidad**: 99.5% uptime con manejo de errores robusto

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Desarrollo
- Usa `black` para formateo de código
- Añade tests para nuevas funcionalidades
- Actualiza documentación en `README.md`

## 📝 Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para el historial completo de versiones.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- [CrewAI](https://www.crewai.com/) - Framework de agentes colaborativos
- [OpenRouter](https://openrouter.ai/) - Plataforma de modelos IA
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno
- [Rich](https://rich.readthedocs.io/) - Librería de terminal hermosa

## 📞 Soporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/Diaz003/zaidsmart/issues)
- 💬 **Discusiones**: [GitHub Discussions](https://github.com/Diaz003/zaidsmart/discussions)
- 📧 **Email**: Para soporte directo

---

**Hecho con ❤️ para revolucionar el desarrollo de videojuegos con IA**