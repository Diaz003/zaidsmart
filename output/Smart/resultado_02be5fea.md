**Game Design Document (GDD) – “Pixel Conquest”**  
*2D Pixel‑Art Strategy Game Focused on Country Conquest*  

---

### 1. Game Overview  
**Title:** Pixel Conquest  
**Genre:** Turn‑Based Strategy / Grand Strategy (with optional real‑time mode)  
**Perspective:** Top‑down 2D  
**Target Audience:** Fans of classic strategy titles (Risk, Civilization, Europa Universalis) who appreciate retro pixel art and deep tactical gameplay.  
**Platform:** PC (Windows/macOS/Linux), with potential ports to Nintendo Switch and PlayStation/Xbox consoles.  
**Core Hook:** Lead a fledgling nation to global domination through military might, economic savvy, diplomacy, and technological advancement—all rendered in lovingly crafted 16‑bit‑style pixel art.  

---

### 2. Core Mechanics  

| Mechanic | Description | Player Interaction |
|----------|-------------|--------------------|
| **World Map** | Procedurally generated or hand‑crafted world map divided into countries (tiles). Each country has terrain type, resources, population, and strategic value. | Click/drag to select countries, view info panels, issue orders. |
| **Turn Structure** | Each turn consists of **Phase 1: Production**, **Phase 2: Diplomacy**, **Phase 3: Movement**, **Phase 4: Combat**, **Phase 5: End‑Turn** (optional real‑time mode skips phases). | Players allocate resources, negotiate, move armies, resolve battles, then end turn. |
| **Resource Management** | Three primary resources: **Gold** (economy), **Manpower** (military), **Tech Points** (research). Generated each turn based on controlled territories, buildings, and trade agreements. | Adjust sliders in the Economy panel; build improvements to boost output. |
| **Armies & Units** | Units are pixel‑art sprites (infantry, cavalry, artillery, navy, air). Each unit has stats: Attack, Defense, Movement, Cost, and special abilities (e.g., Blitz, Fortify). Units can be upgraded via tech. | Train units from barracks/factories; assign to armies; move on map; engage in combat. |
| **Combat System** | Turn‑based tactical combat on a separate battlefield grid (hex or square). Terrain modifiers (forest, mountain, river) affect defense. Auto‑resolve option for speed. | Choose formations, issue orders (attack, hold, retreat), use abilities, view combat log. |
| **Diplomacy** | Options: alliances, non‑aggression pacts, trade deals, vassalage, war declarations, espionage. Diplomatic reputation influences AI willingness to negotiate. | Open Diplomacy menu; select target country; propose/action. |
| **Technology Tree** | Split into **Military**, **Economy**, **Culture** branches. Unlocks new units, buildings, policies, and victory conditions. Tech points spent each turn. | Open Tech screen; research nodes; prerequisites shown. |
| **Buildings & Infrastructure** | Construct within owned countries: farms, mines, factories, barracks, academies, forts, ports. Each provides resource boosts, unit recruitment, or defensive bonuses. | Build menu per country; queue construction; view progress. |
| **Events & Narrative** | Random and scripted events (natural disasters, rebel uprisings, great leaders, discoveries) provide bonuses/penalties and flavor. Event outcomes can be influenced by choices. | Event popup; choose option; see result. |
| **Victory Conditions** | Multiple paths: **Domination** (control X% of world territory), **Economic** (accumulate Y gold and maintain Z trade routes), **Technological** (complete top‑tier tech tree), **Diplomatic** (be elected World Leader via alliance votes), **Score** (highest points after set turns). | Players pursue preferred condition; game ends when condition met. |

---

### 3. Progression System  

1. **Early Game (Turns 1‑30)**  
   - Focus on securing home continent, building basic economy, training initial armies.  
   - Low‑tech units dominate; exploration reveals neighboring countries.  

2. **Mid Game (Turns 31‑80)**  
   - Expansion via conquest or diplomacy.  
   - Tech tree opens mid‑tier units (e.g., tanks, battleships).  
   - Diplomatic blocs begin to form; espionage becomes valuable.  

3. **Late Game (Turns 81+)**  
   - Global powers clash; high‑tech units (jet fighters, nukes) appear.  
   - Victory conditions become attainable; players may switch strategies (e.g., from conquest to diplomatic win).  
   - Endgame events (world crisis, super‑weapon race) add tension.  

**Progression Rewards:**  
- **Experience Points (XP)** earned per turn and from victories; unlocks **Leader Traits** (passive bonuses) for the player’s nation.  
- **Achievements** for milestones (first naval victory, peace treaty with 5 nations, etc.).  

---

### 4. Win/Lose Conditions  

| Condition | Win Criteria | Lose Criteria |
|-----------|--------------|---------------|
| **Domination** | Control ≥ 60% of total world territory (land tiles) for two consecutive turns. | Capital captured and no remaining core territories. |
| **Economic** | Accumulate 500,000 Gold and maintain ≥ 15 active trade routes for 5 turns. | Treasury drops below 0 for 3 turns (bankruptcy). |
| **Technological** | Complete the final node in all three tech branches. | Fall behind tech leader by ≥ 3 eras for 10 turns (AI declares tech superiority). |
| **Diplomatic** | Be elected World Leader by securing ≥ 50% of votes in the World Council (held every 20 turns). | Lose Council seat and fall below 10% approval for two consecutive votes. |
| **Score** (Sandbox) | Highest score after a set number of turns (e.g., 200). | N/A (game ends by timer). |
| **Defeat** | — | Any of the above lose triggers, or player quits. |

---

### 5. Art Style  

- **Resolution:** 320×180 base, scaled up to full‑screen with integer scaling to preserve pixel crispness.  
- **Palette:** Limited 16‑color palettes per biome (e.g., desert: sandy yellows, browns; tundra: icy blues, whites). Global palette switching for day/night cycles and weather effects.  
- **Sprites:**  
  - **Countries/Tiles:** Hand‑drawn terrain tiles (grass, forest, mountain, water) with animated subtle details (waving grass, flowing water).  
  - **Units:** 32×32 pixel sprites with 4‑directional animation (idle, move, attack). Distinct silhouettes for easy recognition.  
  - **Buildings:** Isometric‑style 48×48 pixel structures with construction progress overlay.  
  - **UI:** Retro‑style windows, pixel fonts (e.g., Press Start 2P), iconography using simple shapes.  
- **Effects:** Particle explosions, smoke, and muzzle flashes rendered in limited palettes; screen shake and flash for major events.  
- **Audio (optional note):** Chiptune soundtrack (FM synth) with adaptive layers for peace/war; SFX sourced from classic 8‑bit libraries.  

**Art Direction Goal:** Evoke nostalgia for 16‑bit era strategy games while providing clear visual feedback for gameplay mechanics.  

---

### 6. Target Platform & Technical Specs  

| Platform | Reason | Notes |
|----------|--------|-------|
| **PC (Windows/macOS/Linux)** | Primary development platform; ease of distribution via Steam/itch.io. | Built in **Godot 4.x** (engine supports pixel‑perfect scaling, export to desktop). |
| **Nintendo Switch** | Strong indie strategy audience; handheld play fits turn‑based nature. | Export via Godot’s Switch export templates; ensure button mapping. |
| **PlayStation 5 / Xbox Series X|S** | Access to console strategy market; potential for cross‑save. | Similar export process; adjust UI for TV safe zones. |
| **Mobile (iOS/Android)** *(future)* | Optional casual mode with simplified UI. | Would require touch‑friendly redesign; not in initial scope. |

**Technical Highlights:**  
- **Deterministic Turn Engine** for easy netplay (optional hot‑seat or LAN multiplayer).  
- **Save/Load**: Binary save files compressing map state, units, resources, and diplomacy.  
- **Modding Support**: JSON‑based data files for units, tech trees, events; Steam Workshop integration planned.  

---

### 7. Unique Features  

1. **Pixel‑Perfect Tactical Battles** – Separate combat screens that retain the same aesthetic, allowing deep tactical play without leaving the strategic map.  
2. **Dynamic World Events System** – Procedurally generated crises (e.g., pandemics, meteor strikes) that can shift the balance of power and force adaptive strategies.  
3. **Leader Traits & Legacy System** – Each playthrough generates a unique leader with traits that affect gameplay; traits can be inherited by successors, adding RPG‑like progression across multiple campaigns.  
4. **Diplomatic Reputation Wheel** – Visual reputation meter that influences AI behavior, unlocks special diplomatic options (e.g., marriage alliances, royal claims).  
5. **Alternative Victory Paths** – Encourages replayability: a player can win through economic dominance without ever declaring war, or via cultural influence (soft power) by spreading technology and culture.  
6. **Retro‑Futuristic Soundtrack** – Chiptune score that evolves with era (8‑bit early era → 16‑bit mid era → 32‑bit late era), reinforcing the sense of technological progress.  

---

### 8. Narrative Elements (Flavor & Context)  

While Pixel Conquest is primarily a sandbox strategy game, light narrative layers provide immersion:  

- **Prologue:** The player’s nation begins as a small tribe on a procedurally generated continent, with a brief backstory explaining its ambitions (e.g., “The Sun Kingdom seeks to reclaim the lost Golden Age”).  
- **Historical Eras:** As technology advances, the world transitions through **Ancient**, **Medieval**, **Industrial**, **Modern**, and **Future** eras, each reflected in unit/building art and event flavor text.  
- **Great Leaders:** Randomly generated historical‑style figures (e.g., “Empress Kira the Unifier”) appear, offering unique bonuses or quests when recruited.  
- **World Chronicle:** An in‑game journal logs major events (wars fought, treaties signed, disasters survived) that can be reviewed post‑game for storytelling.  
- **Endgame Epilogue:** Depending on victory condition, a unique pixel‑art ending scene depicts the outcome (e.g., a map unified under one flag, a bustling trade network, a space‑faring civilization).  

These narrative touches are optional and can be toggled off for pure strategy purists.  

---

### 9. Monetization & Post‑Launch Plan (Optional)  

- **Base Game:** One‑time purchase (USD $19.99).  
- **DLC:** Optional expansion packs adding new regions (e.g., “Arctic Front”, “Tropical Isles”), extra unit sets, and alternate history scenarios.  
- **Cosmetic Packs:** Alternative palettes, unit skins, and UI themes (does not affect gameplay).  
- **Community Updates:** Quarterly balance patches, new events, and modding tools.  

---

## 10. Summary  

Pixel Conquest delivers a deep, rewarding strategy experience wrapped in a lovingly crafted 2D pixel‑art presentation. By combining classic turn‑based conquest mechanics with tactical battles, dynamic diplomacy, multiple victory paths, and rich procedural storytelling, the game appeals to both hardcore strategists and fans of retro aesthetics. The design is scoped for production in Godot 4.x, targeting PC and consoles with clear pathways for post‑launch content and community engagement.  

---  

*Prepared by the Coordinador de Proyecto (Project Lead) for the development team.*  
*End of Document.*