from schemas.tool_log import ToolLog
from datetime import datetime
import json
import time


class ToolLogger:
    def __init__(self):
        # in-memory log store (replace with DB later if needed)
        self.logs = []

    # -----------------------------
    # MAIN LOG FUNCTION
    # -----------------------------
    async def log(self, log_entry: ToolLog):

        try:
            enriched_log = log_entry.model_dump()

            # add server-side timestamp
            enriched_log["logged_at"] = datetime.utcnow().isoformat()

            self.logs.append(enriched_log)

            # print structured log (VERY useful for debugging)
            print("\n📊 TOOL LOG")
            print(json.dumps(enriched_log, indent=2,default=str))

        except Exception as e:
            # NEVER crash system because of logging failure
            print(f"[LOGGER ERROR] {str(e)}")

    # -----------------------------
    # GET ALL LOGS
    # -----------------------------
    def get_logs(self):
        return self.logs

    # -----------------------------
    # FILTER BY TOOL
    # -----------------------------
    def get_logs_by_tool(self, tool_name: str):
        return [
            log for log in self.logs
            if log.get("tool") == tool_name
        ]

    # -----------------------------
    # FILTER BY SERVER
    # -----------------------------
    def get_logs_by_server(self, server: str):
        return [
            log for log in self.logs
            if log.get("server") == server
        ]

    # -----------------------------
    # SIMPLE STATS (OPTIONAL BUT USEFUL)
    # -----------------------------
    def get_stats(self):
        total = len(self.logs)

        success = len([l for l in self.logs if l.get("success", True)])

        failed = total - success

        return {
            "total_calls": total,
            "successful_calls": success,
            "failed_calls": failed
        }