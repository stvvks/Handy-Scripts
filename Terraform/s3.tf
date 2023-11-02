#tfsec:ignore:aws-s3-enable-bucket-logging:exp:2023-09-19
resource "aws_s3_bucket" "main" {
  bucket        = "${var.platform_name}-${var.env}-cdn-${var.name}"
  force_destroy = true
}

resource "aws_s3_bucket_website_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "404.html"
  }
}

resource "aws_s3_bucket_ownership_controls" "main" {
  bucket = aws_s3_bucket.main.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "main" {
  bucket = aws_s3_bucket.main.id
  acl    = "private"

  depends_on = [
    aws_s3_bucket_ownership_controls.main
  ]
}

resource "aws_s3_bucket_cors_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  cors_rule {
    allowed_headers = ["Authorization", "Content-Length"]
    allowed_methods = ["GET", "POST"]
    allowed_origins = ["https://${var.domain_name}"]
    max_age_seconds = 3000
  }
}


resource "aws_s3_bucket_public_access_block" "main" {
  bucket                  = aws_s3_bucket.main.id
  ignore_public_acls      = true
  block_public_acls       = true
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "main" {
  bucket = aws_s3_bucket.main.id

  versioning_configuration {
    # Valid values: "Enabled" or "Suspended"
    status = var.enable_s3_bucket_versioning ? "Enabled" : "Suspended"
  }
}

#tfsec:ignore:aws-s3-encryption-customer-key:exp:2023-09-19
resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    apply_server_side_encryption_by_default {
      #kms_master_key_id = aws_kms_key.mykey.arn
      sse_algorithm = "aws:kms"
    }
  }
}