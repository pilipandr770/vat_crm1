#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting VAT CRM application (backend and frontend)...${NC}"

# Start the backend in a new terminal window
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && export FLASK_APP=backend.app:create_app && export FLASK_ENV=development && flask run --host=0.0.0.0 --port=8000"'
else
    # Linux
    gnome-terminal -- bash -c "cd $(pwd) && export FLASK_APP=backend.app:create_app && export FLASK_ENV=development && flask run --host=0.0.0.0 --port=8000; exec bash" || xterm -e "cd $(pwd) && export FLASK_APP=backend.app:create_app && export FLASK_ENV=development && flask run --host=0.0.0.0 --port=8000; exec bash" &
fi

echo -e "${CYAN}Backend server starting at http://localhost:8000${NC}"
sleep 2

# Determine which frontend to use (new_frontend if it exists, otherwise frontend)
FRONTEND_PATH="new_frontend"
if [ ! -d "$FRONTEND_PATH" ]; then
    FRONTEND_PATH="frontend"
fi

# Start the frontend in a new terminal window
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"'/'${FRONTEND_PATH}' && npm run dev"'
else
    # Linux
    gnome-terminal -- bash -c "cd $(pwd)/${FRONTEND_PATH} && npm run dev; exec bash" || xterm -e "cd $(pwd)/${FRONTEND_PATH} && npm run dev; exec bash" &
fi

echo -e "${CYAN}Frontend development server starting...${NC}"
echo -e "\n${GREEN}Application is now running:${NC}"
echo -e "${WHITE}- Backend: http://localhost:8000${NC}"
echo -e "${WHITE}- Frontend: Check the terminal window for URL (typically http://localhost:5173)${NC}"
echo -e "\n${YELLOW}Press Ctrl+C in the respective terminal windows to stop the servers.${NC}"
