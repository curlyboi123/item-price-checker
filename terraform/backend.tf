terraform {
  backend "s3" {
    bucket = local.state_bucket_name
    key    = local.state_bucket_key
    region = local.state_bucket_region
  }
}
