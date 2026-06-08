from core.auth import validate_token
from tools.read_tools import list_jobs
from tools.write_tools import create_job
from schemas.job_schemas import CreateJobInput

payload = CreateJobInput(
  title="Fix AC",
  description="The Ac is not cooling and producing the too much heat",
)

validate_token("writer-token")

print(create_job(payload))
print(list_jobs())
