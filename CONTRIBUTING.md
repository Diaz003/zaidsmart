# Guía de Contribución

¡Gracias por tu interés en contribuir a ZAIDSMART! Este documento describe cómo puedes ayudar al proyecto.

## 🚀 Inicio Rápido

1. **Fork** el repositorio
2. **Clona** tu fork: `git clone https://github.com/tu-usuario/zaidsmart.git`
3. **Crea** una rama: `git checkout -b feature/nueva-funcionalidad`
4. **Instala** dependencias: `pip install -r requirements.txt`
5. **Desarrolla** tu feature
6. **Prueba** tus cambios: `python -m pytest test/`
7. **Commit**: `git commit -m "feat: descripción de la funcionalidad"`
8. **Push**: `git push origin feature/nueva-funcionalidad`
9. **Pull Request**: Abre un PR en GitHub

## 📋 Estándares de Código

### Python
- Usa **Black** para formateo: `black .`
- Sigue **PEP 8** con excepciones razonables
- Tipos de datos con **mypy** cuando sea posible
- Docstrings en formato **Google**

### Commits
Usamos [Conventional Commits](https://conventionalcommits.org/):

```
feat: nueva funcionalidad
fix: corrección de bug
docs: cambios en documentación
style: cambios de formato
refactor: refactorización de código
test: añadir o modificar tests
chore: cambios de mantenimiento
```

### Pull Requests
- Describe claramente qué hace el PR
- Referencia issues relacionados
- Incluye screenshots si aplica (UI)
- Asegúrate de que CI pase

## 🧪 Testing

```bash
# Ejecutar todos los tests
python -m pytest

# Con cobertura
python -m pytest --cov=zaidsmart

# Tests específicos
python test_crew.py
python test_4_agents.py
```

### Tipos de Tests
- **Unit tests**: Para funciones individuales
- **Integration tests**: Para componentes
- **E2E tests**: Para flujos completos

## 🐛 Reportando Bugs

Usa el template de [GitHub Issues](https://github.com/Diaz003/zaidsmart/issues/new?template=bug_report.md):

- Describe el bug claramente
- Pasos para reproducir
- Comportamiento esperado vs actual
- Logs relevantes
- Información del entorno

## 💡 Sugiriendo Features

Usa el template de [GitHub Issues](https://github.com/Diaz003/zaidsmart/issues/new?template=feature_request.md):

- Describe la funcionalidad propuesta
- Explica el problema que resuelve
- Consideraciones de implementación
- Mockups o ejemplos si aplica

## 📚 Documentación

- Actualiza README.md para cambios importantes
- Añade docstrings a nuevas funciones
- Mantén CHANGELOG.md actualizado
- Documenta APIs en el código

## 🔒 Seguridad

- No commits con credenciales
- Usa variables de entorno para secrets
- Reporta vulnerabilidades vía email privado

## 🎯 Áreas de Contribución

### Alto Impacto
- Nuevos agentes especializados
- Mejoras en rendimiento
- Integración con más modelos IA
- UI/UX del dashboard

### Principiante
- Corrección de typos
- Mejoras en documentación
- Tests adicionales
- Scripts de utilidad

## 📞 Comunicación

- **Issues**: Para bugs y features
- **Discussions**: Para preguntas generales
- **Discord/Slack**: Para chat en tiempo real (próximamente)

## 🙏 Reconocimiento

Todos los contribuidores serán reconocidos en:
- CHANGELOG.md
- README.md (sección de agradecimientos)
- Releases de GitHub

¡Gracias por hacer ZAIDSMART mejor! 🎮🤖