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
   git clone https://github.com/ronier83/bezeqDisableDeleteTenant.git
   cd bezeqDisableDeleteTenant
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `tenants.csv` file with your portal names:
   ```csv
   portal_name
   tenant1
   tenant2
   ```

2. Set up your environment variables:
   ```bash
   export CTERA_USERNAME="your_admin_username"
   export CTERA_PASSWORD="your_admin_password"
   ```

## Usage

Run the script with required arguments:
```bash
python main.py -a admin.ctera.com -u admin@ctera.com -p YourSecurePassword123
```

The script will:
- Read portal names from tenants.csv
- Connect to each portal
- Disable the tenant
- Update the status in the database

## Running with Crontab

To run the script automatically on a daily basis, you have two options:

### Option 1: Using Environment File

1. Create a `.env` file:
   ```bash
   CTERA_ADDRESS=admin.ctera.com
   CTERA_USERNAME=admin@ctera.com 
   CTERA_PASSWORD=YourSecurePassword123
   ```

2. Secure the file:
   ```bash
   chmod 600 .env
   ```

3. Add to crontab (`crontab -e`):
   ```bash
   # This will run at 2:00 AM (02:00) every day
   0 2 * * * . /full/path/to/.env; /path/to/python /path/to/bezeqDisableDeleteTenant/main.py -a $CTERA_ADDRESS -u $CTERA_USERNAME -p $CTERA_PASSWORD >> /path/to/cron.log 2>&1
   ```

### Option 2: Using Wrapper Script

1. Create a wrapper script (run.sh):
   ```bash
   #!/bin/bash
   source /full/path/to/.env
   /path/to/python /path/to/bezeqDisableDeleteTenant/main.py -a $CTERA_ADDRESS -u $CTERA_USERNAME -p $CTERA_PASSWORD
   ```

2. Make it executable:
   ```bash
   chmod +x run.sh
   ```

3. Add to crontab:
   ```bash
   0 2 * * * /full/path/to/run.sh >> /path/to/cron.log 2>&1
   ```

## Required Packages

- sqlalchemy: Database ORM for tenant management
- cterasdk: Official CTERA SDK for portal operations
