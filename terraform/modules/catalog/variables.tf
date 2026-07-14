variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "bucket_names" {
  type = map(string)
}
