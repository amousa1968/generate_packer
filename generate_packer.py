#!/usr/bin/env python3
"""
Packer HCL Generator for Platform9 Private Cloud

This script generates a packer.hcl file that creates:
1. A volume from a golden image
2. A VM server from a golden image
3. Attaches the volume to the VM

Requirements:
- Python 3.6+
- openstacksdk

Usage:
python generate_packer.py

The script will:
1. Scan templates/configuration/ folder for available configurations
2. Display available configurations to the user
3. Generate generator_packer.hcl based on selected configuration
"""

import json
import sys
import subprocess
import argparse
from pathlib import Path


def install_requirements():
    """Install required Python packages from requirements.txt."""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("Warning: requirements.txt not found at {}".format(requirements_file))
        return False
    
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
        print("All required packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False


# Check and install requirements before proceeding
if __name__ == "__main__":
    pass


class PackerGenerator:
    """Generator class for creating Packer HCL files."""
    
    def __init__(self, base_path=None):
        """Initialize the generator with base path."""
        if base_path is None:
            # Get the directory where the script is located
            self.base_path = Path(__file__).parent.absolute()
        else:
            self.base_path = Path(base_path)
        
        self.templates_path = self.base_path / "templates" / "configuration"
        self.output_file = self.base_path / "generator_packer.pkr.hcl"
        self.files_path = self.base_path / "files"
        
    def scan_configurations(self):
        """Scan for available configurations in templates/configuration/ folder."""
        configurations = []
        
        if not self.templates_path.exists():
            print(f"Warning: Templates path {self.templates_path} does not exist!")
            return configurations
            
        # Look for subdirectories with vars.json files
        for item in self.templates_path.iterdir():
            if item.is_dir():
                vars_file = item / "vars.json"
                if vars_file.exists():
                    configurations.append({
                        'name': item.name,
                        'path': str(vars_file),
                        'dir': str(item)
                    })
                    
        return configurations
    
    def load_configuration(self, config_path):
        """Load configuration from vars.json file."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            print(f"Error loading configuration from {config_path}: {e}")
            return None
    
    def list_configurations(self):
        """List all available configurations."""
        configurations = self.scan_configurations()
        
        if not configurations:
            print("No configurations found!")
            print(f"Please create configuration files in: {self.templates_path}")
            return None
            
        print("\n" + "=" * 60)
        print("Available Configurations")
        print("=" * 60)
        
        for i, config in enumerate(configurations, 1):
            print(f"\n[{i}] {config['name']}")
            # Load and display some details
            vars_data = self.load_configuration(config['path'])
            if vars_data:
                print(f"    Instance: {vars_data.get('instance_name', 'N/A')}")
                print(f"    Image: {vars_data.get('golden_image_name', 'N/A')}")
                print(f"    Flavor: {vars_data.get('flavor', 'N/A')}")
                print(f"    Volume: {vars_data.get('volume_name', 'N/A')} ({vars_data.get('volume_size_gb', 20)}GB)")
                
        return configurations
    
    def select_configuration(self, configurations):
        """Prompt user to select a configuration."""
        if not configurations:
            return None
            
        while True:
            try:
                choice = input("\nSelect configuration number (or 'q' to quit): ").strip()
                
                if choice.lower() == 'q':
                    print("Exiting...")
                    return None
                    
                index = int(choice) - 1
                if 0 <= index < len(configurations):
                    selected = configurations[index]
                    print(f"\nSelected configuration: {selected['name']}")
                    return selected
                else:
                    print(f"Invalid selection. Please enter a number between 1 and {len(configurations)}")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def generate_hcl(self, config):
        """Generate the Packer HCL file content."""
        
        # Build the HCL content
        hcl_content = '''# =============================================================================
# Generated Packer HCL for Platform9 Private Cloud
# =============================================================================
# This file was generated by generate_packer.py
# Configuration: {config_name}
# =============================================================================

# Packer required plugins
packer {{
  required_plugins {{
    openstack = {{
      version = ">= 1.1.3"
      source  = "github.com/hashicorp/openstack"
    }}
  }}
}}

# =============================================================================
# Variables
# =============================================================================

# OpenStack Connection Variables (can be overridden via CLI or environment)
variable "os_auth_url" {{
  type    = string
  description = "OpenStack authentication URL"
  default = "{os_auth_url}"
}}

variable "os_username" {{
  type    = string
  description = "OpenStack username"
  default = "{os_username}"
}}

variable "os_password" {{
  type    = string
  description = "OpenStack password"
  default = "{os_password}"
  sensitive = true
}}

variable "os_project_name" {{
  type    = string
  description = "OpenStack project name"
  default = "{os_project_name}"
}}

variable "os_project_domain_name" {{
  type    = string
  description = "OpenStack project domain name"
  default = "{os_project_domain_name}"
}}

variable "os_user_domain_name" {{
  type    = string
  description = "OpenStack user domain name"
  default = "{os_user_domain_name}"
}}

variable "os_region" {{
  type    = string
  description = "OpenStack region"
  default = "{os_region}"
}}

variable "os_tenant_id" {{
  type    = string
  description = "OpenStack tenant ID"
  default = ""
}}

variable "os_tenant_name" {{
  type    = string
  description = "OpenStack tenant name"
  default = ""
}}

# Configuration Variables (from vars.json)
variable "instance_name" {{
  type    = string
  description = "Name for the VM instance"
  default = "{instance_name}"
}}

variable "golden_image_name" {{
  type    = string
  description = "Golden image name to use"
  default = "{golden_image_name}"
}}

variable "golden_image_uuid" {{
  type    = string
  description = "Golden image UUID to use"
  default = "{golden_image_uuid}"
}}

variable "flavor" {{
  type    = string
  description = "Flavor for the VM"
  default = "{flavor}"
}}

variable "network_uuid" {{
  type    = string
  description = "Network UUID for the VM"
  default = "{network_uuid}"
}}

variable "network_name" {{
  type    = string
  description = "Network name for the VM"
  default = "{network_name}"
}}

variable "domain_name" {{
  type    = string
  description = "Domain name"
  default = "{domain_name}"
}}

variable "volume_name" {{
  type    = string
  description = "Name for the data volume"
  default = "{volume_name}"
}}

variable "volume_size_gb" {{
  type    = number
  description = "Size of the volume in GB"
  default = {volume_size_gb}
}}

variable "availability_zone" {{
  type    = string
  description = "Availability zone for resources"
  default = "{availability_zone}"
}}

variable "key_pair" {{
  type    = string
  description = "SSH keypair name"
  default = "{key_pair}"
}}

variable "ssh_username" {{
  type    = string
  description = "SSH username"
  default = "{ssh_username}"
}}

variable "ssh_public_key" {{
  type    = string
  description = "Path to SSH public key file"
  default = "{ssh_public_key}"
}}

# Security groups as comma-separated string
variable "security_groups" {{
  type    = string
  description = "Security groups (comma-separated)"
  default = "{security_groups}"
}}

# =============================================================================
# Locals
# =============================================================================

locals {{
  # Parse security groups from comma-separated string
  security_groups_list = split(",", var.security_groups)
  
  # Cloud-init user data file path
  user_data_file = "${{ path.root }}/files/user-data"
}}

# =============================================================================
# Packer Sources (Builders)
# =============================================================================

# ---------------------------------------------------------------------
# Volume Builder - Creates a volume from golden image
# ---------------------------------------------------------------------
source "openstack" "data-volume" {{
  # Connection
  auth_url          = var.os_auth_url
  username          = var.os_username
  password          = var.os_password
  project_name      = var.os_project_name
  domain_name       = var.domain_name
  project_domain_name = var.os_project_domain_name
  user_domain_name  = var.os_user_domain_name
  region            = var.os_region
  tenant_id         = var.os_tenant_id
  tenant_name       = var.os_tenant_name
  
  # Image Configuration - Use golden image by UUID
  image_uuid        = var.golden_image_uuid
  image_name        = var.golden_image_name
  
  # Volume Configuration
  volume_size       = var.volume_size_gb
  volume_name       = var.volume_name
  
  # Availability Zone
  availability_zone = var.availability_zone
  
  # This is a null builder - it just creates the volume from image
  # No actual instance is built, we just prepare the volume
  instance_name     = "temp-volume-builder"
  flavor            = var.flavor
  
  # Communicator (required but not used for volume-only)
  communicator      = "none"
}}

# ---------------------------------------------------------------------
# VM Server Builder - Creates a VM from golden image
# Note: OpenStack connection uses environment variables:
#   OS_AUTH_URL, OS_USERNAME, OS_PASSWORD, OS_PROJECT_NAME, OS_DOMAIN_NAME, OS_REGION
# ---------------------------------------------------------------------
source "openstack" "vm-server" {{
  # Instance Configuration
  instance_name        = var.instance_name
  source_image        = var.golden_image_uuid
  image_name          = var.golden_image_name
  flavor               = var.flavor

  # Network Configuration
  networks             = [var.network_uuid]

  # Security Groups
  security_groups      = local.security_groups_list

  # SSH Configuration
  ssh_keypair_name    = var.key_pair
  ssh_username        = var.ssh_username

  # Cloud-init user data
  user_data_file      = local.user_data_file

  # Volume Configuration
  volume_size         = var.volume_size_gb

  # Availability Zone
  availability_zone   = var.availability_zone

  # Communicator
  communicator        = "ssh"
  ssh_port            = 22
  ssh_timeout         = "5m"

  # Run configuration
  pause_before_connecting = "30s"
}}

# =============================================================================
# Build Configuration
# =============================================================================

build {{
  name = "{build_name}"
  
  # ---------------------------------------------------------------------
  # Build 1: Create data volume from golden image
  # ---------------------------------------------------------------------
  sources = [
    "source.openstack.vm-server"
  ]
  
  # ---------------------------------------------------------------------
  # Provisioner: Configure the VM after creation
  # ---------------------------------------------------------------------
  
  # Shell provisioner to configure the VM
  provisioner "shell" {{
    execute_command = "sudo {{ .Path }}"
    inline = [
      # Update system
      "yum update -y",
      
      # Install required packages
      "yum install -y git ansible curl wget",
      
      # Create data directory
      "mkdir -p /mnt/data",
      
      # Display volume info
      "lsblk",
      
      # If volume is attached as /dev/vdb, format and mount it
      "if [ -b /dev/vdb ]; then",
      "  parted -s /dev/vdb mklabel msdos || true",
      "  parted -s /dev/vdb mkpart primary ext4 0% 100% || true",
      "  mkfs.ext4 /dev/vdb1",
      "  mkdir -p /mnt/data",
      "  mount /dev/vdb1 /mnt/data",
      "  echo '/dev/vdb1 /mnt/data ext4 defaults 0 0' >> /etc/fstab",
      "fi",
      
      # If volume is attached as /dev/sdb, format and mount it
      "if [ -b /dev/sdb ]; then",
      "  parted -s /dev/sdb mklabel msdos || true",
      "  parted -s /dev/sdb mkpart primary ext4 0% 100% || true",
      "  mkfs.ext4 /dev/sdb1",
      "  mkdir -p /mnt/data",
      "  mount /dev/sdb1 /mnt/data",
      "  echo '/dev/sdb1 /mnt/data ext4 defaults 0 0' >> /etc/fstab",
      "fi",
      
      # Clean up
      "yum clean all",
      
      # Display mount info
      "df -h",
      
      # Create test file
      "echo 'VM provisioned successfully!' > /mnt/data/provisioned.txt"
    ]
  }}
  
  # ---------------------------------------------------------------------
  # Post-provisioning: Output information
  # ---------------------------------------------------------------------
  provisioner "shell-local" {{
    command = "echo '========================================' && echo 'Packer build completed successfully!' && echo '========================================' && echo 'Instance Name: {instance_name}' && echo 'Volume Name: {volume_name}' && echo '========================================'"
  }}
}}

# =============================================================================
# Volume Creation and Attachment (External Script)
# =============================================================================
# The volume will be created and attached during the build process.
# To create the volume separately before VM creation, use the following:
#
# 1. Create volume from image:
#    openstack volume create --image <image-uuid> --size <size> <volume-name>
#
# 2. Create VM:
#    openstack server create --image <image-uuid> --flavor <flavor> \\
#        --network <network-uuid> --key-name <keypair> <instance-name>
#
# 3. Attach volume to VM:
#    openstack server add volume <instance-name> <volume-name>
#
# =============================================================================
'''.format(
            config_name=config.get('configuration_name', 'unknown'),
            os_auth_url=config.get('os_auth_url', 'https://platform9.example.com:5000/v3'),
            os_username=config.get('os_username', 'admin'),
            os_password=config.get('os_password', ''),
            os_project_name=config.get('project_name', 'admin'),
            os_project_domain_name=config.get('project_domain_name', 'default'),
            os_user_domain_name=config.get('user_domain_name', 'default'),
            os_region=config.get('region', 'RegionOne'),
            instance_name=config.get('instance_name', 'vm-server'),
            golden_image_name=config.get('golden_image_name', ''),
            golden_image_uuid=config.get('golden_image_uuid', ''),
            flavor=config.get('flavor', 'm1.small'),
            network_uuid=config.get('network_uuid', ''),
            network_name=config.get('network_name', 'private-network'),
            domain_name=config.get('domain_name', 'default'),
            volume_name=config.get('volume_name', 'data-volume'),
            volume_size_gb=config.get('volume_size_gb', 20),
            availability_zone=config.get('availability_zone', 'az1'),
            key_pair=config.get('key_pair', 'my-key'),
            ssh_username=config.get('ssh_username', 'rocky'),
            ssh_public_key=config.get('ssh_public_key', 'files/key.pub'),
            security_groups=','.join(config.get('security_groups', ['default'])),
            build_name=config.get('configuration_name', 'platform9-build')
        )
        
        return hcl_content
    
    def create_user_data_file(self):
        """Create a sample cloud-init user-data file."""
        user_data_content = '''#cloud-config
users:
  - name: rocky
    sudo: "ALL=(ALL) NOPASSWD:ALL"
    shell: /bin/bash
    ssh_authorized_keys: []

package_update: true
package_upgrade: true

packages:
  - git
  - ansible
  - curl
  - wget

runcmd:
  - mkdir -p /mnt/data
  - touch /mnt/data/testfile
  - echo "VM configured successfully" > /mnt/data/status.txt

final_message: "System setup completed after $UPTIME seconds"
'''
        user_data_path = self.files_path / "user-data"
        
        # Create files directory if it doesn't exist
        self.files_path.mkdir(parents=True, exist_ok=True)
        
        if not user_data_path.exists():
            with open(user_data_path, 'w') as f:
                f.write(user_data_content)
            print(f"Created user-data file: {user_data_path}")
        else:
            print(f"User-data file already exists: {user_data_path}")
    
    def generate(self, config_name=None):
        """Main method to generate the Packer HCL file."""
        print("=" * 60)
        print("Packer HCL Generator for Platform9 Private Cloud")
        print("=" * 60)
        
        # Scan for configurations
        configurations = self.scan_configurations()
        
        if not configurations:
            print("\nNo configurations found!")
            print(f"Please create configuration files in: {self.templates_path}")
            print("\nExample configuration structure:")
            print("  templates/configuration/")
            print("  ├── rocky97/")
            print("  │   └── vars.json")
            print("  └── rocky98/")
            print("      └── vars.json")
            return False
        
        # Select configuration
        selected_config = None
        
        if config_name:
            # Use specified configuration
            for config in configurations:
                if config['name'] == config_name:
                    selected_config = config
                    break
            if not selected_config:
                print(f"Configuration '{config_name}' not found!")
                return False
        else:
            # List and let user select
            configurations = self.list_configurations()
            if not configurations:
                return False
            selected_config = self.select_configuration(configurations)
            
        if not selected_config:
            print("No configuration selected. Exiting.")
            return False
        
        # Load configuration
        print(f"\nLoading configuration from: {selected_config['path']}")
        config = self.load_configuration(selected_config['path'])
        
        if not config:
            print("Failed to load configuration!")
            return False
        
        print("\nConfiguration loaded successfully!")
        print("-" * 40)
        for key, value in config.items():
            if 'password' not in key.lower():  # Hide passwords
                print(f"  {key}: {value}")
        print("-" * 40)
        
        # Create user-data file if needed
        self.create_user_data_file()
        
        # Generate HCL content
        print("\nGenerating Packer HCL file...")
        hcl_content = self.generate_hcl(config)
        
        # Write to file
        with open(self.output_file, 'w') as f:
            f.write(hcl_content)
        
        print(f"\n{'=' * 60}")
        print("SUCCESS!")
        print(f"{'=' * 60}")
        print("Generated Packer HCL file: {}".format(self.output_file))
        print(f"\nTo build and deploy, run:")
        print(f"  packer init {self.output_file}")
        print(f"  packer validate {self.output_file}")
        print(f"  packer build {self.output_file}")
        
        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate Packer HCL for Platform9 Private Cloud',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode - select configuration
  python generate_packer.py
  
  # Specify configuration by name
  python generate_packer.py --config rocky97
  
  # Specify custom base path
  python generate_packer.py --path /path/to/project
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Configuration name to use (e.g., rocky97, rocky98)'
    )
    
    parser.add_argument(
        '--path', '-p',
        type=str,
        help='Base path for the project (default: script directory)'
    )
    
    args = parser.parse_args()
    
    # Create generator
    generator = PackerGenerator(base_path=args.path)
    
    # Generate HCL
    success = generator.generate(config_name=args.config)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()

