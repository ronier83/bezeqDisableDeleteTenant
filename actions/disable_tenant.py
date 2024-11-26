from datetime import datetime

def disable_tenant(admin, session):
    """Disable tenants and update their status"""
    from database.models import Portal
    
    # Get portals that need to be disabled
    portals = session.query(Portal).filter(
        Portal.tenant_id.isnot(None),
        Portal.disable_completed_at.is_(None)
    ).all()

    for portal in portals:
        try:
            # Get current tenant parameters
            params = admin.api.get(f"objs/{portal.tenant_id}/")
            print(f"Current activation status for tenant {portal.portal_name}: {params.activationStatus}")
            
            # Set activation status to Disabled
            params.activationStatus = 'Disabled'
            admin.api.put(f"objs/{portal.tenant_id}/", params)
            
            # Update portal status and timestamp
            portal.status = 'disabled'
            portal.disable_completed_at = datetime.utcnow()
            session.commit()
            
            print(f"Successfully disabled tenant {portal.portal_name} and updated timestamp")
        except Exception as e:
            if "Editing portal in trashcan is forbidden" in str(e):
                # Update portal status to deleted and set both timestamps
                portal.status = 'deleted'
                current_time = datetime.utcnow()
                portal.disable_completed_at = current_time
                portal.delete_completed_at = current_time
                session.commit()
                print(f"Portal {portal.portal_name} was in trashcan. Updated status to deleted with timestamps.")
            else:
                session.rollback()
                print(f"Error disabling tenant {portal.portal_name}: {str(e)}")