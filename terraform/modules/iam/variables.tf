variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "bucket_arns" {
  type = map(string)
}
