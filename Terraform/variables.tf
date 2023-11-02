variable "platform_name" {
  description = "Name of platform that created by this TF module"
  type        = string
}

variable "env" {
  description = "Name of environment that managed by this terraform module"
  type        = string
}

variable "aws_region" {
  description = "The AWS region to which peering connection should be estabilished"
  type        = string
  default     = "us-east-1"
}

variable "name" {
  type        = string
  description = "Name of CDN distribution that should be created"
}

variable "domain_name" {
  type        = string
  description = "Domain name alias for CDN distribution"
}

variable "dns_zone_id" {
  type        = string
  description = "ARN of Route53 DNS zones where DNS records for CDN should be registered"
}

variable "ssl_cert_arn" {
  type        = string
  description = "ARN of certificate in AWS Certificate manager"
}

variable "enable_s3_bucket_versioning" {
  type        = bool
  description = "If true - S3 bucket versioning will be enabled"
  default     = true
}

variable "ssl_protocol_version" {
  type        = string
  description = "Name of AWS SSL Protocol version to use with Cloudfront"
  default     = "TLSv1.2_2021"
}