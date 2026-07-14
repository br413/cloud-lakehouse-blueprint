terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      ManagedBy   = "terraform"
      Environment = var.environment
    }
  }
}

module "storage" {
  source = "./modules/storage"

  project_name = var.project_name
  environment  = var.environment
}

module "iam" {
  source = "./modules/iam"

  project_name = var.project_name
  environment  = var.environment
  bucket_arns = {
    bronze = module.storage.bronze_bucket_arn
    silver = module.storage.silver_bucket_arn
    gold   = module.storage.gold_bucket_arn
  }
}

module "catalog" {
  source = "./modules/catalog"

  project_name = var.project_name
  environment  = var.environment
  bucket_names = module.storage.bucket_names
}
