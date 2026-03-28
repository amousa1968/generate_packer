# Packer HCL Generator for Platform9 Private Cloud

This project generates Packer HCL configuration files for creating VMs with attached data volumes in OpenStack/Platform9 Private Cloud environments.

## Features

- Generates complete Packer HCL from JSON configuration templates
- Supports multiple VM configurations (Rocky Linux, Windows, etc.)
- Automatic volume creation and attachment
- Cloud-init integration
- Production-ready Packer configurations for OpenStack v1.1.3+

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate Packer HCL
python generate_packer.py
```

## Directory Structure

```
├── generate_packer.py          # Main generator script
├── templates/configuration/    # JSON configuration templates
│   ├── rocky97/
│   │   └── vars.json
│   └── win2022/
│       └── vars.json
├── files/                      # Supporting files (user-data, keys)
├── generator_packer.pkr.hcl    # Generated output (example)
└── requirements.txt
```

## GitHub Actions

This repository includes CI/CD workflows:

### CI Workflow (`.github/workflows/ci.yml`)
- **Linting**: Ruff for Python code quality
- **Tests**: Run generator with all configurations
- **Packer Validation**: Validate all generated `.pkr.hcl` files

Triggers on:
- Push/PR to `main/master`
- Changes to Python files, templates, requirements

### Release Workflow (`.github/workflows/release.yml`)
- Build Python package on `v*` tags
- Publish to PyPI (configure `PYPI_API_TOKEN` secret)
- Create GitHub Release

## Usage Examples

### Generate for specific config
```bash
python generate_packer.py --config rocky97
```

### Validate generated HCL
```bash
packer validate generator_packer.pkr.hcl
```

### Full build (with vars)
```bash
packer build -var-file=vars.pkrvars.hcl generator_packer.pkr.hcl
```

## Sample vars.pkrvars.hcl

```hcl
os_auth_url = "https://your-openstack:5000/v3"
os_username = "admin"
os_password = "secret"
os_project_name = "admin"
# ... other vars
```

## Development

```bash
# Lint
ruff check .

# Install dev deps
pip install -e '.[dev]'

# Run tests
pytest
```

## License

MIT

