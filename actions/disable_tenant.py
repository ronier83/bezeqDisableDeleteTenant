from datetime import datetime

def disable_tenant(admin, session):
    """Disable tenants and update their status"""
    from database.models import Portal
    
    # Get portals that need to be disabled
    portals = session.query(Portal).filter(
        Portal.tenant_id.isnot(None),
        Portal.disable_completed_at.is_(None)
    ).all()
    
    print("\nProcessing tenants for disable action:")
    print("-" * 40)
    
    for portal in portals:
        print(f"Processing portal: {portal.portal_name} (Tenant ID: {portal.tenant_id})")
        try:
            # Get current tenant parameters
            params = admin.api.get(f"objs/{portal.tenant_id}/")
            print(f"Current activation status for tenant {portal.tenant_id}: {params.activationStatus}")
            
            # Set activation status to Disabled
            params.activationStatus = 'Disabled'
            admin.api.put(f"objs/{portal.tenant_id}/", params)
            
            # Update portal status and timestamp
            portal.status = 'disabled'
            portal.disable_completed_at = datetime.utcnow()
            session.commit()
            
            print(f"Successfully disabled tenant {portal.tenant_id} and updated timestamp")
        except Exception as e:
            session.rollback()
            print(f"Error disabling tenant {portal.tenant_id}: {str(e)}")