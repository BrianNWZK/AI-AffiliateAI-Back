from ariel_matrix.ariel_user import ARIEL, ArielUser

# For compatibility, expose SYSTEM_USER and ARIEL_MATRIX_USER as aliases
SYSTEM_USER = ARIEL
ARIEL_MATRIX_USER = ARIEL

# Alias for compatibility with 'from ariel_matrix.user import User'
User = ArielUser
