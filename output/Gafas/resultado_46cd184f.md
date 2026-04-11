**Documento de Diseño de Juego (GDD) – “Limpieza Pixelada”**  
*Juego de arte 2D en estilo pixel art donde el jugador debe limpiar una casa.*

---

### 1. Visión General
- **Género:** Simulación / Arte interactivo  
- **Perspectiva:** Vista superior (top‑down) 2D  
- **Plataformas objetivo:** PC (Windows/macOS/Linux), Nintendo Switch, dispositivos móviles (iOS/Android)  
- **Duración de una partida:** 10‑30 min por ronda (modo historia) o sesiones libres ilimitadas (modo sandbox)  
- **Público objetivo:** Jugadores casuales, amantes del arte pixelado, educadores que busquen actividades de orden y mindfulness, y fans de juegos “cozy”.  
- **Propósito artístico:** Explorar la belleza de lo cotidiano, transformar una tarea doméstica en una experiencia meditativa y estética mediante colores, sonido y mecánicas de limpieza que favorezcan la atención plena.

---

### 2. Mecánicas de Juego
| Mecánica | Descripción | Interacción |
|----------|-------------|-------------|
| **Movimiento del personaje** | Control libre con teclado/gamepad o toque (joystick virtual). | Desplazamiento fluido en 8 direcciones. |
| **Herramientas de limpieza** | - Escoba (barre polvo y migas) <br> - Trapeador (elimina manchas de líquido) <br> - Aspiradora (succión de pelo y pequeños objetos) <br> - Paño de polvo (quita telarañas y polvo fino) | Cada herramienta se selecciona con una tecla/button y se activa manteniendo presionado el botón de acción mientras se pasa sobre el área sucia. |
| **Sistema de suciedad** | La casa tiene un mapa de “nivel de suciedad” por tile (0‑100). Las acciones reducen ese valor según la eficiencia de la herramienta. Cuando el tile llega a 0, vuelve a su estado limpio (sprite limpio). | Visualización mediante partículas y cambio de sprite (sucio → limpio). |
| **Gestión de tiempo / energía** (opcional) | Barra de energía que se agota con cada acción; se recoge con objetos de descanso (taza de té, ventana abierta) o se recarga automáticamente en modo libre. | Añade un ligero desafío sin romper la sensación cozy. |
| **Objetos interactivos** | Muebles, juguetes, ropa, platos, etc. pueden ser movidos o ordenados para acceder a áreas ocultas. | Arrastrar y soltar (click‑drag) o pulsar para interactuar. |
| **Modo Foto** | Pausa el juego y permite al jugador tomar una captura de la habitación limpia con filtros pixel‑art y marcos decorativos. | Compartir en redes o guardar como obra de arte. |
| **Logros y Coleccionables** | - “Habitación Impecable” (limpiar 100 % de una habitación) <br> - “Coleccionista de Polvo” (recoger 1000 partículas de polvo) <br> - “Objetos Perdidos” (encontrar y devolver objetos extraviados a su lugar) | Desbloquean paletas de color extra, nuevos sprites de herramientas y pistas de música. |

---

### 3. Historia / Narrativa
- **Premisa:** El jugador asume el rol de un “Espíritu del Hogar”, una entidad ligada a la casa que se manifiesta cuando el orden y la armonía se pierden. Su tarea es restaurar la paz limpiando y reorganizando cada espacio.
- **Estructura:** El juego está dividido en capítulos que representan diferentes momentos del día (mañana, tarde, noche) y estaciones del año. Cada capítulo introduce una nueva habitación y una pequeña historia ambiental (ej. una foto antigua encontrada detrás del sofá que revela un recuerdo de los habitantes).
- **Narración ambiental:** No hay diálogos extensos; la historia se cuenta mediante objetos coleccionables, notas adhesivas, y cambios sutiles en la iluminación y el sonido que reflejan el estado de ánimo de la casa.
- **Final abierto:** Después de limpiar todas las áreas, el jugador puede continuar en modo “Sandbox” para seguir decorando y experimentar con nuevas combinaciones de colores y objetos.

---

### 4. Estilo Artístico
- **Resolución pixel art:** 32×32 píxeles por tile (escala 2x o 3x según plataforma).  
- **Paleta de colores:** Base cálida (tonos tierra, crema, gris suave) con acentos pastel según la estación (azules cielo para primavera, naranjas otoñales, blancos nevados para invierno).  
- **Iluminación dinámica:** Sistemas de luz puntual (lámparas, ventanas) que cambian la sombra y el color de los tiles según la hora del día, reforzando la sensación de tiempo pasando.  
- **Animaciones:**  
  - Personaje: 4‑frame walk cycle, idle con respiración sutil.  
  - Herramientas: partículas de polvo, burbujas de agua, chispas de aspiradora.  
  - Suciedad: transición de sprite “sucio” → “limpio” en 2‑3 frames con efecto de desvanecimiento.  
- **Interfaz de usuario:** Minimalista, iconos pixelados para barra de herramientas, energía y minimapa. Tipografía tipo “Press Start 2P” para mantener la coherencia retro.  
- **Audio:** Banda sonora chiptune relajante (lo‑fi + melodías simples). Efectos de sonido: barrido suave, aspiradora zumbante, gota de agua, crujido de madera bajo los pies. Opcional modo “ASMR” con sonidos amplificados.

---

### 5. Objetivo del Jugador
- **Primario:** Reducir el nivel de suciedad de cada habitación a 0 % utilizando las herramientas disponibles.  
- **Secundario (opcional):**  
  - Ordenar objetos fuera de lugar a su ubicación correcta.  
  - Descubrir y coleccionar todos los objetos narrativos (fotos, notas, recuerdos).  
  - Alcanzar altos puntajes de eficiencia (menos movimientos, menos energía usada).  
  - Crear composiciones estéticas mediante la disposición de muebles y decoración (modo foto).  

---

### 6. Niveles / Áreas de la Casa
| Área | Descripción | Mecánicas destacadas | Tiempo estimado |
|------|-------------|----------------------|-----------------|
| **Entrada** | Zapatero, perchero, alfombra. Introduce barra y escoba. | Aprender movimiento y barrido básico. | 2‑3 min |
| **Sala de estar** | Sofá, mesa de café, estantería, planta. | Uso de trapeador para manchas de vino, aspirador para pelo de mascota. | 4‑5 min |
| **Cocina** | Encimera, fregadero, nevera, basura. | Combina trapeador (derrames), aspiradora (migotas), paño (grasa). | 5‑6 min |
| **Baño** | Inodoro, ducha, lavabo, toallas. | Enfocado en manchas de agua y moho (trapeador + producto especial). | 3‑4 min |
| **Dormitorio** | Cama, armario, mesilla. | Ordenar ropa, limpiar polvo bajo la cama (escoba + aspiradora). | 4‑5 min |
| **Estudio / Oficina** | Escritorio, computadora, estanterías. | Organización de papeles, limpieza de pantalla (paño), aspirar migas de comida. | 4‑5 min |
| **Patio / Jardín** (opcional, modo expansión) | Césped, macetas, mobiliario exterior. | Nuevo tool: manguera y rastrillo. | 5‑6 min |

Cada área se desbloquea secuencialmente en la historia; al completar todas se accede al modo libre donde el jugador puede visitar cualquier habitación en cualquier orden.

---

### 7. Elementos Interactivos
- **Objetos móviles:** sillas, cajas, juguetes – pueden ser empujados o arrastrados para acceder a zonas ocultas.  
- **Puertas y armarios:** abren/cierran con un botón, revelando espacios de almacenamiento o áreas sucias escondidas.  
- **Interruptores de luz:** cambian la intensidad ambiental, afectando la visibilidad de la suciedad.  
- **Ventanas:** al abrirlas, entra luz exterior y se activa un pequeño bonus de energía (representa aire fresco).  
- **Objetos coleccionables:** fotos, cartas, juguetes antiguos – al examinarse muestran una breve ventana de lore o ilustración pixelada.  
- **Mascotas virtuales (opcional):** un gato o perro que sigue al jugador y deja pelo que debe aspirarse; interactuar con ellos otorga puntos de amistad.  

---

### 8. Características Adicionales / Expansiones Futuras
- **Modo Cooperativo local:** dos jugadores controlan dos espíritus con herramientas diferentes, fomentando la colaboración.  
- **Editor de habitaciones:** permite al jugador crear su propia distribución de salas y compartirla mediante códigos.  
- **Eventos estacionales:** actualizaciones que cambian la decoración (Halloween, Navidad) y añaden suciedad temática (telarañas, nieve, hojas).  
- **Integración de accesibilidad:** modos para daltónicos, controles remappables, opción de reducción de efectos visuales intensos.  
- **Logros de “Arte”:** desbloquear paletas de colores alternativas basadas en obras de arte famosas (ej. paleta “Starry Night”, “Monet’s Garden”).  
- **Versión Educativa:** guías para profesores que quieran usar el juego para enseñar hábitos de orden y responsabilidad.  

---

### 9. Resumen de Producción (para el equipo de desarrollo)
| Área | Responsable | Entregable clave |
|------|-------------|------------------|
| **Diseño de juego & Narrativa** | Coordinador de Proyecto (usted) + Diseñador | GDD (este documento), flowchart de progresión, guiones de objetos coleccionables. |
| **Arte & Animación** | Artista Pixel | Sprites de tiles, personajes, herramientas, partículas, UI, paletas de colores por estación. |
| **Programación (Godot)** | Desarrollador Godot | Sistema de mapa de suciedad, control de herramientas, gestión de energía, guardar/cargar, modo foto, logros. |
| **Audio & Música** | Compositor / Sound Designer | Banda sonora chiptune loops, efectos de limpieza, ambientación por habitación. |
| **QA & Testing** | Tester interno | Pruebas de balance de dificultad, verificación de bugs de colisión, testeo de accesibilidad. |
| **Marketing & Comunidad** | Comunidad Manager | Material promocional (gifs, capturas), plan de lanzamiento en itch.io/Steam, outreach a streamers cozy. |

---

**Conclusión**  
“Limpieza Pixelada” transforma una tarea doméstica rutinaria en una experiencia artística y meditativa mediante mecánicas de limpieza claras, un estilo pixel art acogedor y una narrativa ambiental que invita al jugador a encontrar belleza en el orden. Este GDD provee una base completa para pasar a la fase de prototipado y producción. ¡Listo para comenzar el desarrollo!