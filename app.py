# -*- coding: utf-8 -*-
from src.pdftextify.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1100)
