# Documento de Diseño de Juego (GDD)  
**Proyecto:** *[Título provisional]* – “Square Rush”  

> **Nota:** Este documento está escrito en español y formateado en Markdown para facilitar su publicación en repositorios (GitHub, GitLab) y su uso colaborativo dentro del equipo de desarrollo.

---  

## 1. Resumen Ejecutivo  

### 1.1 Título provisional  
**Square Rush** (nombre provisional, sujeto a cambios de marketing).  

### 1.2 Elevator pitch (una frase)  
Un frenético platformer 2D en el que controlas un cuadrado que salta de plataforma en plataforma al ritmo de música electrónica de alta energía, desafiando la gravedad y tus reflejos en niveles cada vez más rápidos y peligrosos.  

### 1.3 Visión del juego  
Crear una experiencia de “arcade” minimalista y adictiva que combine controles precisos, desafíos de timing y una banda sonora pulsante, todo dentro de una estética geométrica y limpia que aproveche al máximo el motor Godot 4 y sea fácilmente exportable a PC, consola y móviles.

---  

## 2. Gameplay  

### 2.1 Bucle de juego principal  
1. **Inicio** → Pantalla de título → Selección de nivel / modo.  
2. **Carga del nivel** → El jugador controla el cuadrado y debe avanzar lo más rápido posible.  
3. **Core loop (ciclo)**  
   - Saltar entre plataformas.  
   - Evitar o superar obstáculos/hazards.  
   - Recoger “boosts” y “puntos” (opcional).  
   - Mantener el ritmo con la música (puntos de ritmo, combos).  
4. **Final del nivel** → Se muestra la puntuación, tiempo, combos, y opciones de reintento o pasar al siguiente nivel.  
5. **Progresión** → Cada nivel aumenta la velocidad, complejidad de plataformas y frecuencia de hazards.  

### 2.2 Mecánicas principales  

| Mecánica | Descripción | Parámetros clave |
|----------|-------------|------------------|
| **Movimiento horizontal** | El cuadrado se desplaza a velocidad constante, se puede acelerar/pedir “dash” (opcional). | Velocidad base = 200 px/s, aceleración = 0 (movimiento instantáneo). |
| **Salto** | Salto simple con física de gravedad. Altura y tiempo ajustables. | Fuerza de salto = 500 px/s, gravedad = 1200 px/s², “coyote time” = 0.15 s. |
| **Doble salto (opcional)** | Permitido en algunos niveles para añadir complejidad. | Consumo de “energy” (recurso). |
| **Dash (opcional)** | Impulso breve horizontal o diagonal, útil para cruzar brechas largas. | Duración 0.2 s, velocidad 600 px/s, cooldown 1 s. |
| **Recolectables** | “Boosts” que otorgan velocidad extra o puntos. | Valor de puntos, duración del efecto. |
| **Combo de ritmo** | Si el jugador ejecuta saltos/alineaciones con el beat, se otorgan multiplicadores. | Ventana de timing ±0.1 s del beat. |
| **Vida/Resurrección** | El jugador tiene 3 vidas; al perder todas, se muestra “Game Over”. | Respawn en último checkpoint. |

---  

## 3. Personaje Jugador  

### 3.1 Descripción visual  
- **Forma:** Cuadrado puro (sin texturas).  
- **Tamaño:** 32 × 32 px (puede escalarse según resolución).  
- **Color base:** #FF5722 (naranja brillante). Cambios de color pueden indicar “power‑ups” o daño.  

### 3.2 Física y movimiento  

| Propiedad | Valor | Comentario |
|-----------|-------|-------------|
| **Masa** | 1 kg (valor por defecto de Godot) | Afecta la gravedad. |
| **Fricción** | 0 (sin fricción lateral) | Movimiento sin desaceleración. |
| **Gravedad** | 1200 px/s² (global) | Ajustable por nivel. |
| **Colisionador** | `CollisionShape2D` (cuadrado) | Preciso y sencillo. |
| **Animaciones** | Simple “scale bounce” al saltar (opcional) | Para feedback visual. |

### 3.3 Habilidades  

1. **Saltar** – Básico.  
2. **Doble salto** – Disponible en niveles avanzados o como power‑up.  
3. **Dash** – Disponible tras recoger “dash token”.  
4. **Invulnerabilidad breve** – Al sincronizar salto con beat (combo de ritmo).  

---  

## 4. Plataformas y Hazards  

### 4.1 Tipos de plataformas  

| Tipo | Comportamiento | Visual | Uso típico |
|------|----------------|--------|-----------|
| **Estática** | No se mueve. | Color #4CAF50 (verde). | Base de niveles. |
| **Movimiento horizontal** | Desplazamiento constante entre dos puntos. | Verde con flechas. | Añade timing. |
| **Movimiento vertical** | Subida/bajada cíclica. | Verde con flechas verticales. | Requiere anticipación. |
| **Desaparecedor** | Se vuelve invisible/inhóspito tras tocarlo (tiempo de 0.5 s). | Verde con bordes punteados. | Penaliza errores. |
| **Temporizado** | Aparece y desaparece según ritmo (sincronizado con la música). | Verde con pulsación de brillo. | Refuerza conexión musical. |
| **Con “boost”** | Al tocarla otorga velocidad extra por breve tiempo. | Verde con icono “+”. | Recompensa riesgo. |

### 4.2 Hazards (obstáculos)  

| Hazard | Descripción | Visual | Daño/penalización |
|--------|-------------|--------|-------------------|
| **Pinchos** | Lugar de daño instantáneo. | Rojo con picos. | Pierde vida. |
| **Agujeros** | Caída al vacío. | Negro/negro. | Muerte inmediata. |
| **Láser horizontal** | Barrera que se activa/desactiva con ritmo. | Rojo con línea pulsante. | Daño instantáneo. |
| **Plataforma colapsante** | Se rompe tras 1 segundo de contacto. | Marrón con grietas. | Caída al vacío si se queda demasiado. |
| **Zona de “slow”** | Reduce la velocidad del jugador (campo). | Azul con icono “-”. | Penaliza tiempo. |

---  

## 5. Niveles  

### 5.1 Estructura y progresión  

- **Cantidad total de niveles:** 30 (10 “Worlds” de 3 niveles cada una).  
- **World 1 – Introducción:** Tutorial de movimiento y salto. Plataformas estáticas.  
- **World 2 – Movimiento:** Introducción de plataformas móviles.  
- **World 3 – Riesgo:** Introducción de hazards simples.  
- **World 4 – Ritmo:** Sincronización con música, plataformas temporizadas.  
- **World 5 – Combos:** Introducción de doble salto, dash.  
- **World 6 – Velocidad:** Niveles ultra‑rápidos, ritmo acelerado.  
- **World 7 – Multicombos:** Combos de ritmo + power‑ups.  
- **World 8 – Laberinto:** Plataformas interconectadas, decisiones de ruta.  
- **World 9 – Jefe:** Secuencia larga con varios hazards y música épica.  
- **World 10 – Último desafío:** Mezcla de todas mecánicas en máxima dificultad.  

### 5.2 Escalado de dificultad  

- **Velocidad base de desplazamiento** aumenta 5 % por world.  
- **Frecuencia de plataformas móviles** aumenta 10 % por world.  
- **Número de hazards** aumenta 2 por nivel.  
- **Ritmo musical (BPM)** incrementa 5 bpm cada world (p.ej., 120 BPM → 165 BPM).  

### 5.3 Checkpoints  

- **Automáticos** al comienzo de cada nivel.  
- **Opcionales** en niveles largos (World 9, World 10) mediante “flag” visual.  

---  

## 6. Arte  

### 6.1 Estilo visual  

- **Minimalista geométrico**: Solo formas básicas (cuadrados, rectángulos, líneas).  
- **Paleta de colores** (modo “Neón”):  
  - Fondo: #0D0D0D (casi negro).  
  - Plataformas: tonos verdes (#4CAF50), azules (#2196F3) y amarillos (#FFC107).  
  - Hazards: rojos brillantes (#F44336).  
  - Player: naranja (#FF5722).  
- **Sombras y efectos**: Sutiles sombras paralelas para dar profundidad, sin texturas.  
- **Animaciones**: Escalado y “pulse” en plataformas sincronizadas con el beat.  

### 6.2 Guías de arte  

| Elemento | Resolución recomendada | Formato | Comentario |
|----------|------------------------|---------|------------|
| Player | 32 × 32 px (escala 1x/2x/3x) | PNG (sin alfa) | Color principal, con variante de “damage”. |
| Plataforma | 64 × 16 px (horizontal) | PNG | Color base, con efectos de “glow”. |
| Hazard | 48 × 48 px | PNG | Sprite con animación de parpadeo. |
| UI icons | 24 × 24 px (vector) | SVG | Escalable. |
| Fondo | 1920 × 1080 px (opcional) | PNG | Gradiente sutil o patrón geométrico simple. |

### 6.3 Herramientas  

- **Pixel art / vector:** Aseprite o Adobe Illustrator.  
- **Shader:** Godot Shading Language (GDScript/VisualShader) para efectos de glow y “beat pulse”.  

---  

## 7. Audio  

### 7.1 Música  

- **Estilo:** EDM / Electro‑House de alta energía, con BPM entre 120‑180, ritmo marcado y drops que coincidan con “puntos críticos” del nivel.  
- **Uso:** Cada mundo tiene su propia pista, con “stems” (batería, bajo, synth) que pueden ser activados/desactivados dinámicamente (ej. intensificar al recoger un boost).  
- **Integración:**  
  - **AudioStreamPlayer** por nivel.  
  - **AudioBus** “Music”, “SFX”, “UI”.  
  - **Sync Mapping:** Cada beat está marcado con un “beat event” (señal emitida a través de `Signal` en Godot) para sincronizar efectos de plataformas temporizadas y combos de ritmo.  

### 7.2 Efectos de sonido (SFX)  

| Acción | Archivo | Descripción | Volumen recomendado |
|--------|----------|-------------|---------------------|
| Salto | `jump.wav` | Pitido corto, tono ascendente. | -6 dB |
| Doble salto | `double_jump.wav` | Pitido más agudo. | -6 dB |
| Dash | `dash.wav` | Swoosh rápido. | -4 dB |
| Impacto con plataforma | `land.wav` | Golpe bajo. | -8 dB |
| Recolectar boost | `boost.wav` | Chime brillante. | -4 dB |
| Hazard | `hazard.wav` | Zumbido bajo + click. | -6 dB |
| Muerte | `death.wav` | Crash grave. | -8 dB |
| UI click | `ui_click.wav` | Click corto. | -12 dB |
| Pausa/Despausa | `pause.wav` / `resume.wav` | Swell suave. | -10 dB |  

### 7.3 Ambient & UI  

- **Ambiente:** Breves “whoosh” al cambiar de nivel, sonido de fondo de “circuit”.  
- **UI:** Feedback audible en menús (selección, confirmación).  

---  

## 8. Controles  

| Dispositivo | Acción | Tecla / Botón |
|-------------|--------|---------------|
| **Teclado** | Mover izquierda | ← o A |
|             | Mover derecha | → o D |
|             | Saltar | Barra espaciadora o W |
|             | Dash (opcional) | Shift izquierdo |
|             | Pausa | Esc |
| **Gamepad (Genérico X‑Box/PlayStation)** | Mover | Stick izquierdo (eje X) |
|                                 | Saltar | Botón A (X) |
|                                 | Dash | Botón B (Circle) |
|                                 | Pausa | Botón + (Start) |
| **Móviles (opcional)** | Mover | Touch left/right halves |
|                         | Saltar | Tap central superior |
|                         | Dash | Swipe lateral breve (opcional) |

> **Configuración de controles:** En el menú “Opciones” el jugador podrá reasignar teclas y sensibilidad del stick.

---  

## 9. Interfaz de Usuario (UI)  

### 9.1 HUD (Head‑Up Display)  

- **Marcador de puntuación** (esquina superior izquierda).  
- **Vidas** – Íconos de corazón (esquina superior derecha).  
- **Timer / Tiempo** – Centrado arriba, muestra tiempo actual del nivel.  
- **Combo de ritmo** – Indicador de barra que se rellena al sincronizar con el beat; color cambia a dorado cuando se alcanza el máximo.  

### 9.2 Menús  

| Menú | Elementos | Comentario |
|------|-----------|------------|
| **Pantalla de título** | Logo, botón *Play*, *Opciones*, *Créditos*, *Salir* (PC) | Animación ligera del logo al ritmo de la música. |
| **Selección de nivel** | Mapa de mundos con nodos desbloqueables, botón *Back* | Cada nodo muestra tiempo record y estrellas. |
| **Pause** | *Resume*, *Restart Level*, *Options*, *Quit to Menu* | Fondo difuminado, música se reduce a 50 %. |
| **Game Over** | *Retry*, *Quit to Menu* | Texto “Game Over” con efecto de glitch. |
| **Victory / Level Complete** | Puntuación, tiempo, combo, botones *Next Level*, *Replay*, *Menu* | Animación de “fireworks” minimalista. |
| **Opciones** | Volumen *Music*, *SFX*, *UI*; Sensibilidad de movimiento; Reasignar controles; Idioma. | Guardado en `config.cfg`. |

### 9.3 Tipografía  

- Fuente sans‑serif “Roboto” (tamaños 24, 18, 14).  
- Títulos en neón (color #FFEB3B).  

---  

## 10. Especificaciones técnicas  

| Ítem | Detalle |
|------|---------|
| **Motor** | Godot 4.2 (última versión LTS al momento de iniciar). |
| **Lenguaje** | GDScript 2.0 (principal), opcional C# para módulos críticos de rendimiento. |
| **Plataformas de exportación** | Windows (64 bit), macOS (Intel/Apple Silicon), Linux, Nintendo Switch, PlayStation 5, Xbox Series X, Android, iOS. |
| **Resolución mínima** | 1280 × 720 (aspect ratio 16:9). |
| **Escalado** | UI y sprites escalan mediante `Viewport` y `Stretch Mode = 2D` (Keep Aspect). |
| **Estructura de carpetas** | ```/project_root <br> ├─ assets/ <br> │   ├─ sprites/ <br> │   ├─ audio/ <br> │   └─ fonts/ <br> ├─ scenes/ <br> │   ├─ player/ <br> │   ├─ platforms/ <br> │   ├─ hazards/ <br> │   └─ ui/ <br> ├─ scripts/ <br> ├─ levels/ <br> └─ project.godot``` |
| **Gestión de datos** | `Singleton` *GameState* (autoload) – guarda progreso, puntuaciones, configuraciones. |
| **Audio Bus Layout** | Music → Master (volumen 0‑1), SFX → Master, UI → Master. |
| **Versionado** | Git, rama `main` para releases; `dev` para integración continua. |
| **CI/CD** | GitHub Actions → Build para Windows, Linux y macOS; pruebas unitarias con `godot -s`. |
| **Documentación** | GDD (este documento) + `README.md` + `docs/` con diagramas de flujo y API. |

---  

## 11. Plan de desarrollo (Milestones)  

| Fase | Duración estimada | Objetivos clave | Entregables |
|------|--------------------|----------------|-------------|
| **Pre‑producción** | 2 semanas | Conceptualizar juego, definir GDD, crear mock‑ups visuales, seleccionar música (licencias). | GDD final, moodboard, lista de assets. |
| **Prototipo básico** | 3 semanas | Implementar movimiento del cuadrado, salto, plataforma estática, HUD básico, música de prueba. | Demo jugable (proto) *Alpha 0*. |
| **Iteración 1 – Plataformas** | 4 semanas | Añadir tipos de plataformas (movimiento, temporizadas), hazards simples, nivel 1‑3 completados. | Build *Alpha 1* con 3 niveles. |
| **Iteración 2 – Ritmo y Audio** | 4 semanas | Sincronizar eventos de plataforma con beat, implementar combo de ritmo, música final para worlds 1‑3. | Build *Alpha 2* con 6 niveles, sistema de ritmo. |
| **Iteración 3 – Power‑ups y Dash** | 3 semanas | Implementar dash, doble salto, recolectables, UI de combo. | Build *Beta 1* con 12 niveles. |
| **Polishing & Niveles avanzados** | 5 semanas | Diseñar worlds 4‑10, integrar música final, equilibrar dificultad, añadir checkpoints, crear escena de “jefe”. | Build *Beta 2* con todos los niveles. |
| **Testing y QA** | 3 semanas | Pruebas de jugabilidad, corrección de bugs, optimización (FPS, consumo memoria), pruebas en dispositivos objetivo. | Release Candidate (RC). |
| **Release** | 1 semana | Preparar builds finales, crear paquetes de distribución, subir a Steam, consoles, tiendas móviles. | Versión 1.0 pública. |
| **Post‑release** | Ongoing | Soporte post‑lanzamiento, parches, DLC opcional (nuevos mundos, skins). | Parches y actualizaciones. |

> **Hitos clave de gestión:** Cada fase incluye revisión de “play‑test” con al menos 5 testers internos, y reunión de “sprint review” al finalizar la semana 2 de cada fase.  

---  

## 12. Riesgos y mitigación  

| Riesgo | Probabilidad | Impacto | Estrategia de mitigación |
|--------|--------------|--------|--------------------------|
| **Desalineación música‑ritmo** | Media | Alto (la jugabilidad depende del beat). | Implementar `AudioSyncManager` temprano; usar música con markers pre‑definidos; pruebas de sincronía cada sprint. |
| **Performance en dispositivos móviles** | Alta | Medio‑alto (poco margen de error). | Optimizar colisiones (uso de `CollisionShape2D` simples), limitar número de nodos activos, usar `TileMap` para plataformas estáticas; pruebas de perfilamiento en Android/iOS. |
| **Escasez de recursos musicales** | Baja | Alto (requiere licencias). | Contratar compositor o usar librerías libres de royalties (e.g., **Incompetech**, **Freesound**) con contrato claro. |
| **Cambios en la versión de Godot** | Baja | Medio. | Fijar versión en `godot_version=4.2` en `project.godot`; usar CI para bloquear builds si la versión cambia. |
| **Desbalance de dificultad** | Media | Medio‑alto. | Crear tabla de “scaling curve”; play‑test continuo; permitir ajuste de parámetros vía `tuning.cfg`. |
| **Problemas de control en gamepad** | Baja | Bajo‑medio. | Utilizar `Input.is_action_pressed` y mapear acciones en `project.godot`; test en múltiples controladores. |
| **Falta de documentación** | Media | Medio. | Mantener `CHANGELOG.md`, `docs/` actualizados cada commit; asignar “Documentation Lead”. |

---  

## 13. Apéndices  

### 13.1 Lista de assets (placeholders)  

| ID | Tipo | Nombre | Descripción | Tamaño/Resolución | Comentario |
|----|------|--------|-------------|-------------------|------------|
| A001 | Sprite | `player_square.png` | Cuadrado jugador (base) | 32 × 32 px | Color naranja. |
| A002 | Sprite | `platform_static.png` | Plataforma estática | 64 × 16 px | Verde. |
| A003 | Sprite | `platform_move_h.png` | Plataforma móvil horizontal | 64 × 16 px | Verde con flechas. |
| A004 | Sprite | `platform_move_v.png` | Plataforma móvil vertical | 16 × 64 px | Verde con flechas. |
| A005 | Sprite | `platform_temp.png` | Plataforma temporizada (beat) | 64 × 16 px | Verde con glow. |
| A006 | Sprite | `hazard_spike.png` | Pinchos | 48 × 48 px | Rojo. |
| A007 | Sprite | `hazard_laser.png` | Láser horizontal | 128 × 8 px | Rojo pulsante. |
| A008 | Audio | `music_world1.ogg` | Track EDM 120 BPM (World 1) | 3 min | Loopable. |
| A009 | Audio | `sfx_jump.wav` | Salto | 0.3 s | Mono. |
| A010 | Audio | `sfx_boost.wav` | Boost | 0.2 s | Brillante. |
| A011 | UI | `icon_heart.svg` | Vida | 24 × 24 px | Escalable. |
| A012 | UI | `icon_timer.svg` | Reloj | 24 × 24 px | Escalable. |
| … | … | … | … | … | … |

> **Nota:** Cada asset debe estar versionado y almacenado en la carpeta correspondiente (`/assets/sprites`, `/assets/audio`, `/assets/ui`).  

### 13.2 Juegos de referencia  

| Juego | Razón de referencia | Elementos útiles |
|-------|---------------------|------------------|
| **Super Meat Boy** | Precisión de salto y ritmo rápido. | Movimiento instantáneo, nivelación de dificultad. |
| **Geometry Dash** | Sincronía música‑plataforma. | Plataformas que “bailan” al beat. |
| **Celeste** | Sistema de “coyote time” y “dash”. | Sensibilidad de controles, feedback visual. |
| **Bit.Trip Runner** | Estética minimalista + música retro. | UI minimalista, efectos de ritmo. |
| **Hollow Knight** (modo audio) | Integración de audio como mecánica de juego. | Eventos de audio dirigidos. |

### 13.3 Diagramas de flujo (texto)  

#### 13.3.1 Flujo de nivel (simplificado)  

```
Start Level
   |
   v
Spawn Player → Load Music (BPM) → Spawn Platforms/Hazards
   |
   v
[Game Loop]
   ├─ Input (Move, Jump, Dash)
   ├─ Physics (Gravity, Collisions)
   ├─ Audio Sync (beat events)
   ├─ Checkpoints? (if reached)
   └─ UI Update (Score, Timer, Combo)
   |
   v
Player reaches EndZone ?
   ├─ Sí → Show Level Complete → Save Time/Score → Unlock Next Level
   └─ No → Player dies? (Lives >0) → Respawn at last checkpoint
```

#### 13.3.2 Audio‑Sync Manager  

```
AudioStreamPlayer (Music)
   |
   v
Signal: beat_event (every 1/BPM seconds)
   |
   v
Connected nodes:
   - PlatformTemporal (toggle visibility)
   - ComboMeter (increment)
   - VisualEffect (pulse)
```  

### 13.4 Configuración rápida del proyecto (pasos)  

1. **Clonar repo:** `git clone https://github.com/tu_org/square_rush.git`  
2. **Instalar Godot 4.2 LTS** (desde https://godotengine.org).  
3. **Abrir proyecto:** `godot -e project.godot`  
4. **Instalar dependencias:** (si se usa C#) `dotnet restore` dentro de `/src`.  
5. **Ejecutar prototipo:** `F5` (debug) o `godot --headless -s run_game.gd` (CI).  

---  

## 14. Conclusión  

Este GDD provee la visión completa y los detalles técnicos necesarios para que el equipo de desarrollo comience la producción de **Square Rush** de manera estructurada, coordinada y con claridad en metas, riesgos y entregables. Cada sección está pensada para ser iterada y mejorada a lo largo del ciclo de desarrollo, permitiendo un flujo de trabajo ágil y una entrega final de alta calidad que cumpla con los objetivos de jugabilidad, estética minimalista y una banda sonora electrónica que marque el ritmo del juego.  

> **Próximos pasos:**  
> 1. Validar este documento con los leads de arte, audio y programación.  
> 2. Asignar responsables a cada milestone.  
> 3. Iniciar la fase de pre‑producción y crear los primeros assets (player, plataformas).  

---  

*Fin del documento.*