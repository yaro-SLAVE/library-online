from app.settings import *  # pylint: disable=wildcard-import,unused-wildcard-import
from library_service.tests import opac_mock

# Use mock OPAC for tests
OPAC_HOSTNAME = f"http://localhost:{opac_mock.PORT}"
OPAC_INTERNAL_TOKEN = "internal-token"

# Override URL configuration to use TokenObtainPairView instead of OPAC-based auth
ROOT_URLCONF = "library_service.tests.urls"
