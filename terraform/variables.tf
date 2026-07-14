variable "project_name" {
  description = "Lakehouse project identifier"
  type        = string
  default     = "retail-lakehouse"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region for lakehouse resources"
  type        = string
  default     = "us-east-1"
}
