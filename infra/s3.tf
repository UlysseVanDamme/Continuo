resource "aws_s3_bucket" "midi" {
  bucket = "${var.project_name}-midi-${var.environment}"

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}
