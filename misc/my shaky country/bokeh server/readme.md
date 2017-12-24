## Contents and How to run

1. ``config`` : nginx config file
2. ``myapp.py``: actual web app
3. ``latest.xml`` placeholder file for latest eartquakes

Start nginx with ``config`` file and execute this command ``bokeh serve myapp.py --port 5100   --allow-websocket-origin=SERVER-IP-HERE``.

