locals {
  layers = ["bronze", "silver", "gold"]
}

resource "aws_s3_bucket" "layer" {
  for_each = toset(local.layers)

  bucket = "${var.project_name}-${var.environment}-${each.key}"
}

resource "aws_s3_bucket_versioning" "layer" {
  for_each = aws_s3_bucket.layer

  bucket = each.value.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "layer" {
  for_each = aws_s3_bucket.layer

  bucket = each.value.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

output "bronze_bucket_name" {
  value = aws_s3_bucket.layer["bronze"].bucket
}

output "silver_bucket_name" {
  value = aws_s3_bucket.layer["silver"].bucket
}

output "gold_bucket_name" {
  value = aws_s3_bucket.layer["gold"].bucket
}

output "bronze_bucket_arn" {
  value = aws_s3_bucket.layer["bronze"].arn
}

output "silver_bucket_arn" {
  value = aws_s3_bucket.layer["silver"].arn
}

output "gold_bucket_arn" {
  value = aws_s3_bucket.layer["gold"].arn
}

output "bucket_names" {
  value = { for layer, bucket in aws_s3_bucket.layer : layer => bucket.bucket }
}
