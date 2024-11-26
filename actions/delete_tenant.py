from datetime import datetime, timedelta

def delete_tenant(admin, session):
    """Delete tenants that were disabled more than 2 weeks ago"""
    from database.models import Portal
    
    two_weeks_ago = datetime.utcnow() - timedelta(weeks=2)
    
    # Get portals that were disabled more than 2 weeks ago and not yet deleted
    portals = session.query(Portal).filter(
        Portal.disable_completed_at <= two_weeks_ago,
        Portal.delete_completed_at.is_(None)
    ).all()
    
    print("\nProcessing tenants for deletion:")
    print("-" * 40)
    
    for portal in portals:
        print(f"Processing portal: {portal.portal_name}")
        try:
            # Delete the portal
            admin.portals.delete(portal.portal_name)
            
            # Update portal status and timestamp
            portal.status = 'deleted'
            portal.delete_completed_at = datetime.utcnow()
            session.commit()
            
            print(f"Successfully deleted portal {portal.portal_name} and updated timestamp")
        except Exception as e:
            session.rollback()
            print(f"Error deleting portal {portal.portal_name}: {str(e)}")