from .utils import execute_query  # Import the execute_query function

def admin_context(request):
    """
    Provides context variables for admin users.
    """
    admin_user = None
    if 'admin_id' in request.session:
        query = "SELECT * FROM admins WHERE id = %s"
        admin_user = execute_query(query, [request.session['admin_id']], fetchone=True)

    return {
        'admin_user': admin_user,
    }
