from app.models.role import Role

def get_role_by_id(id):
    result = Role.query.filter(
        Role.id == id,
        Role.is_active == 1
    ).first()
    return result or None

def get_all_role():
    result = Role.query.filter(
        Role.is_active == 1
    ).all()
    return result or None