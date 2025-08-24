provider "aws" {
  region = "eu-west-1"

  default_tags {
    tags = {
      Git-Repo = "https://github.com:curlyboi123/item-price-checker"
    }
  }
}
