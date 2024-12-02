import csv
import argparse
from datetime import datetime, timedelta
from database import init_db, get_session
from database.models import Portal
from actions.disable_tenant import disable_tenant
from actions.delete_tenant import delete_tenant
from cterasdk import GlobalAdmin, settings
import time

settings.sessions.management.ssl = False

def load_csv_data(filename, session):
    """Load portal names from CSV file into database"""
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check if portal already exists
            existing_portal = session.query(Portal).filter_by(portal_name=row['portal_name']).first()
            if not existing_portal:
                portal = Portal(
                    portal_name=row['portal_name'],
                    status='new',
                    processed_at=datetime.utcnow()
                )
                session.add(portal)
            else:
                print(f"Portal {row['portal_name']} already exists in database, skipping.")
    session.commit()

def process_tenants(address, username, password, session):
    """Process all tenant operations using a single admin session"""
    with GlobalAdmin(address) as admin:
        try:
            admin.login(username, password)
            admin.portals.browse_global_admin()
            portals = session.query(Portal).all()
            
            try:
                # Process one portal at a time
                for portal in portals:
                    if portal.tenant_id is None:  # Only update those without tenant_id
                        print(f"\nProcessing portal: {portal.portal_name}")
                        tenants = admin.portals.list_tenants(include=['name', 'baseObjectRef'])
                        
                        for tenant in tenants:
                            if tenant.name == portal.portal_name:
                                tenant_id = tenant.baseObjectRef.split('/')[1]
                                portal.tenant_id = tenant_id
                                print(f"Found match! Portal: {portal.portal_name}, Tenant ID: {portal.tenant_id}")
                                session.commit()  # Commit immediately after finding each tenant
                                break
                        else:
                            print(f"No matching tenant found for portal: {portal.portal_name}")
                
                print("-" * 40)
                print("Finished tenant ID updates")
                print("-" * 40)
                
                # Now process each portal that has a tenant_id - only once
                disable_tenant(admin, session)
                print("-" * 40)
                print("Finished disable tenant action")
                print("-" * 40)
                print("Starting delete tenant action")
                print("-" * 40)
                delete_tenant(admin, session)
                print("-" * 40)
                print("Finished delete tenant action")
                print("-" * 40)
                
            except Exception as e:
                session.rollback()
                print(f"Error processing tenants: {str(e)}")
                
        except Exception as e:
            print(f"Error logging in: {str(e)}")

def main():
    """Main function to process portals and update tenant IDs"""
    parser = argparse.ArgumentParser(description='Process portal operations with CTERA')
    parser.add_argument('-a', '--address', required=True, help='Portal address')
    parser.add_argument('-u', '--username', required=True, help='Admin username')
    parser.add_argument('-p', '--password', required=True, help='Portal password')
    
    args = parser.parse_args()
    
    try:
        # Initialize database
        init_db()
        session = get_session()
        print("-" * 40)
        print("Starting tenant ID updates")
        print("-" * 40)
        # Load initial data from CSV
        load_csv_data('tenants.csv', session)
        # Process all tenant operations
        process_tenants(args.address, args.username, args.password, session)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()