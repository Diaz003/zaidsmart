#!/bin/bash

# Colores y Banner
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
RED='\033[38;5;167m'    # Muted coral red
ORANGE='\033[38;5;208m' # True orange
NC='\033[0m' # No Color

clear
echo -e "${RED}███████╗ █████╗ ██╗██████╗ ███████╗███╗   ███╗█████╗ ██████╗ ████████╗"
echo -e "${RED}╚══███╔╝██╔══██╗██║██╔══██╗██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝"
echo -e "${RED}  ███╔╝ ███████║██║██║  ██║███████╗██╔████╔██║███████║██████╔╝   ██║   "
echo -e "${RED} ███╔╝  ██╔══██║██║██║  ██║╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   "
echo -e "${RED}███████╗██║  ██║██║██████╔╝███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   "
echo -e "${RED}╚══════╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ${NC}"
echo -e "${ORANGE}───────────────────────────────────────────────────────────────────────${NC}"
echo -e "${RED}➤ Iniciando entorno de Inteligencia Artificial para: ZAIDSMART...${NC}"

# 1. Directorio base
cd "$(dirname "$0")"

# 2. Limpieza de puerto 8000
PORT=8000
echo -e "${PURPLE}🔍 Verificando puerto $PORT...${NC}"
PID_ON_PORT=$(lsof -t -i :$PORT)
if [ ! -z "$PID_ON_PORT" ]; then
    echo -e "${RED}⚠️ Puerto $PORT ocupado (PID: $PID_ON_PORT). Limpiando...${NC}"
    kill -9 $PID_ON_PORT 2>/dev/null
    sleep 1
fi

# 3. Manejo de señales (Trap)
trap 'echo -e "\n${RED}🛑 Deteniendo sistema ZAIDSMART...${NC}"; kill $(jobs -p) 2>/dev/null; exit' SIGINT SIGTERM

# 4. Entorno Virtual
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo -e "${PURPLE}✔ Entorno virtual activado.${NC}"
    pip install -q rich httpx
else
    echo -e "${PURPLE}⚠ No se encontró .venv, usando Python global.${NC}"
fi

# 5. Ejecutar Backend
echo -e "${BLUE}🌐 Escuchando tu dashboard en: http://0.0.0.0:$PORT${NC}"
echo -e "${BLUE}📱 Entra desde Tailscale con la IP Mágica en tu móvil.${NC}"
echo "------------------------------------------------------------------"
uvicorn api.main:app --host 0.0.0.0 --port $PORT --reload --log-level warning &

# Mantenemos el script vivo
wait
