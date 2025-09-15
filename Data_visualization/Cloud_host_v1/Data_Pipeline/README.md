For deployment, after updating the code, the files (main.py, index.html, and requirements.txt) were placed into a single folder. The VS Code Azure Web App extension was then used for easy deployment to the Azure Web App named serial-ws-backend.

In the Azure Web App Settings → Configuration, the startup command was set to:
python -m uvicorn main:app --host 0.0.0.0 --port 8000

Debugging was performed using the Log Stream output messages. The data pipeline was first tested by sending sample data through this channel, and then switched back to live data, which worked successfully. The UI was also improved with different colors and additional padding for the charts.
