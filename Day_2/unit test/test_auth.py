from core.auth import validate_token
from core.auth import get_current_auth


print(validate_token("reader-token"))

print(get_current_auth())