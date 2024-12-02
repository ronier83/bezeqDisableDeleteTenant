# CTERA Portal Management Tool

A Python-based tool for managing CTERA portals, including tenant ID mapping, disabling, and deletion operations.

## Features

- Load portal names from CSV file
- Automatically map tenant IDs to portals
- Disable tenants
- Automatically delete disabled tenants after 2 weeks
- SQLite database for tracking operations
- Command-line interface for easy automation

## Prerequisites

- Python 3.6 or higher
- CTERA Portal admin access
- Required Python packages (see requirements.txt)

## Project Structure

```
ctera-portal-tool/
├── actions/
│   ├── __init__.py
│   ├── delete_tenant.py
│   └── disable_tenant.py
├── database/
│   ├── __init__.py
│   └── models.py
├── main.py
├── requirements.txt
├── tenants.csv
├── .gitignore
└── README.md
```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ctera-portal-tool.git
   cd ctera-portal-tool
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `tenants.csv` file with your portal names:
   ```csv
   portal_name
   tenant1.portal.com
   tenant2.portal.com
   ```

2. Set up your environment variables:
   ```bash
   export CTERA_USERNAME="your_admin_username"
   export CTERA_PASSWORD="your_admin_password"
   ```

## Usage

Basic usage:

1. Run the script with required arguments:
   ```bash
   python main.py -a admin.ctera.com -u admin@ctera.com -p YourSecurePassword123
   ```

2. The script will:
   - Read portal names from tenants.csv
   - Connect to each portal
   - Disable the tenant
   - Update the status in the database

3. Monitor the output for:
   - Processing status for each tenant:
     - Portal name and tenant ID
     - Current activation status
     - Success/failure of disable operation
   - Any errors that occur during execution:
     - API connection issues
     - Database errors
     - Permission problems

## Automation with Crontab

To run the script daily at 2 AM, add the following to your crontab:

1. Open crontab editor:
   ```bash
   crontab -e
   ```

2. Add the following line:
   ```bash
   0 2 * * * cd /path/to/ctera-portal-tool && /path/to/venv/bin/python main.py -a admin.ctera.com -u admin@ctera.com -p YourSecurePassword123 >> /path/to/ctera-portal-tool/cron.log 2>&1
   ```

Note: For better security, consider using environment variables or a configuration file for credentials:

1. Create a config file (config.sh):
   ```bash
   export CTERA_ADDRESS="admin.ctera.com"
   export CTERA_USERNAME="admin@ctera.com"
   export CTERA_PASSWORD="YourSecurePassword123"
   ```

2. Update crontab to use config:
   ```bash
   0 2 * * * cd /path/to/ctera-portal-tool && source config.sh && /path/to/venv/bin/python main.py -a $CTERA_ADDRESS -u $CTERA_USERNAME -p $CTERA_PASSWORD >> /path/to/ctera-portal-tool/cron.log 2>&1
   ```

Required packages:
   - sqlalchemy: Database ORM for tenant management
   - cterasdk: Official CTERA SDK for portal operations