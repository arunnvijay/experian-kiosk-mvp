# Server Runner 
import uvicorn 
import sys 
import os 
 
# Add backend to path 
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend')) 
 
if __name__ == "__main__": 
    print("Starting Experian Kiosk MVP Server...") 
    print("Access at: http://127.0.0.1:8000") 
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True) 
