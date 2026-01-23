variable "aws_region" {
    description = "AWS region to deploy resources into"
    type        = string
    default     = "eu-west-1"
}

variable "project_name" {
    description = "Base name for all Continuo resources"
    type        = string
    default     = "continuo"
}

variable "environment" {
    description = "Deployment environment"
    type        = string
    default     = "dev"
}

variable "s3_bucket_name" {
    type    = string
    default = "continuo-midi-bucket"
}