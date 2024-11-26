from datetime import datetime, timedelta

def delete_tenant(admin, session):
    """Delete tenants that were disabled more than 2 weeks ago"""
    from database.models import Portal
    
    two_weeks_ago = datetime.utcnow() - timedelta(weeks=2)
    
    # Get all disabled portals that haven't been deleted yet
    portals = session.query(Portal).filter(
        Portal.status == 'disabled',
        Portal.delete_completed_at.is_(None)
    ).all()
    
    for portal in portals:
        if portal.disable_completed_at is None:
            print(f"Portal {portal.portal_name} not yet disabled")
            continue
            
        days_since_disable = (datetime.utcnow() - portal.disable_completed_at).days
        if portal.disable_completed_at > two_weeks_ago:
            print(f"Portal {portal.portal_name} was disabled {days_since_disable} days ago. Waiting for 14 days before deletion.")
            continue
            
        try:
            # Delete the portal
            admin.portals.delete(portal.portal_name)
            
            # Update portal status and timestamp
            portal.status = 'deleted'
            portal.delete_completed_at = datetime.utcnow()
            session.commit()
            
            print(f"Successfully deleted portal {portal.portal_name}")
        except Exception as e:
            session.rollback()
            print(f"Error deleting portal {portal.portal_name}: {str(e)}")