output "bronze_bucket_name" {
  value = module.storage.bronze_bucket_name
}

output "silver_bucket_name" {
  value = module.storage.silver_bucket_name
}

output "gold_bucket_name" {
  value = module.storage.gold_bucket_name
}

output "role_arns" {
  value = module.iam.role_arns
}

output "catalog_database_name" {
  value = module.catalog.database_name
}
