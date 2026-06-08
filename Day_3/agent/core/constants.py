SERVER_CONFIG = {
    "job": {
        "transport": "streamable_http",
        "url": "http://localhost:3000/mcp",
        "headers": {
            "Authorization": "Bearer writer-token"
        }
    },

    "call": {
        "transport": "streamable_http",
        "url": "http://localhost:3001/mcp",
        "headers": {
            "Authorization": "Bearer writer-token"
        }
    }
}
# System settings
TIMEOUT_SECONDS = 30
MAX_RETRIES = 2

# Logging
ENABLE_TOOL_LOGGING = True
LOG_LEVEL = "INFO"