locals {
  roles = {
    data_engineer = {
      layers  = ["bronze", "silver", "gold"]
      actions = ["s3:GetObject", "s3:PutObject", "s3:ListBucket", "s3:DeleteObject"]
    }
    analytics_engineer = {
      layers  = ["silver", "gold"]
      actions = ["s3:GetObject", "s3:PutObject", "s3:ListBucket"]
    }
    analyst = {
      layers  = ["gold"]
      actions = ["s3:GetObject", "s3:ListBucket"]
    }
  }
}

resource "aws_iam_role" "lakehouse" {
  for_each = local.roles

  name = "${var.project_name}-${var.environment}-${each.key}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "layer_access" {
  for_each = local.roles

  name = "${each.key}-layer-access"
  role = aws_iam_role.lakehouse[each.key].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      for layer in each.value.layers : {
        Effect = "Allow"
        Action = each.value.actions
        Resource = [
          var.bucket_arns[layer],
          "${var.bucket_arns[layer]}/*",
        ]
      }
    ]
  })
}

output "role_arns" {
  value = { for role, config in aws_iam_role.lakehouse : role => config.arn }
}
