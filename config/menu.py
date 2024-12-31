class MenuItem:
    def __init__(self, title, url, icon, children=None):
        self.title = title
        self.url = url
        self.icon = icon
        self.children = children or []

def get_admin_menu():
    return [
        MenuItem('Dashboard', 'admin_dashboard', 'fas fa-tachometer-alt'),
        MenuItem('Eventos', 'manage_events', 'fas fa-calendar-alt'),
        MenuItem('Participantes', 'manage_participants', 'fas fa-users'),
        MenuItem('Encontros', 'manage_meetings', 'fas fa-clock'),
        MenuItem('Check-in', 'public_checkin', 'fas fa-check-circle'),
    ]
