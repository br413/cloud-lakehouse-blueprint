# Run the cloud lakehouse blueprint demo
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot ..

Write-Host "Validating blueprint..."
python -m src.lakehouse.cli validate

Write-Host ""
Write-Host "Deployment plan:"
python -m src.lakehouse.cli plan

Write-Host ""
Write-Host "Cost estimate (prod):"
python -m src.lakehouse.cli cost --environment prod

Write-Host ""
Write-Host "Lineage from bronze.raw_orders:"
python -m src.lakehouse.cli lineage --from-node bronze.raw_orders

Write-Host ""
Write-Host "Partition DDL:"
python -m src.lakehouse.cli ddl --table silver.stg_orders

Write-Host ""
Write-Host "Running tests..."
python -m pytest -q

Write-Host "Demo complete. See docs/deployment.md for apply and rollback steps."
