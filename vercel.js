{
  "version": 2,
  "builds": [
    {
      "src": "wsgi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "wsgi.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production",
    "FLASK_DEBUG": "false",
    "SECRET_KEY": "escala360_secretkey",
    "APP_NAME": "ESCALA360",
    "APP_VERSION": "1.0.0",
    "AUTHOR": "Anderson de Matos Guimarães",
    "ENABLE_BI": "true",
    "PLOTLY_THEME": "plotly_dark",
    "DB_ENGINE": "sqlite",
    "DB_NAME": "escala360.db",
    "LOG_LEVEL": "INFO"
  },
  "functions": {
    "api/**/*.py": {
      "maxDuration": 30,
      "memory": 1024
    }
  },
  "regions": ["gru1", "iad1", "sfo1"],
  "github": {
    "enabled": true,
    "silent": false,
    "autoJobCancelation": true
  }
}
