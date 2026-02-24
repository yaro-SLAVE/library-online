"""Settings for integration tests - uses REAL OPAC service"""
from app.settings import *  # pylint: disable=wildcard-import,unused-wildcard-import

# Use REAL OPAC for integration tests
OPAC_HOSTNAME = "https://library.istu.edu/opac"
OPAC_INTERNAL_TOKEN = "internal-token"

# Override URL configuration to use TokenObtainPairView for simpler auth
ROOT_URLCONF = "library_service.tests.urls"
