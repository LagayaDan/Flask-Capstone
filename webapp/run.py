import sys
import os

# Ensure the project root (parent of webapp/) is on sys.path so that
# `from webapp import create_app` works regardless of how this file is launched.
_here   = os.path.dirname(os.path.abspath(__file__))   # …/Capstone Payroll - Copy/webapp
_root   = os.path.dirname(_here)                       # …/Capstone Payroll - Copy
if _root not in sys.path:
    sys.path.insert(0, _root)

from webapp import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
