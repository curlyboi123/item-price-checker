locals {
  lambda_function_zip = "../src/lambda_function/lambda_package.zip"
}
module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "aeron-price-checker"
  description   = "Lambda function for checking price of Herman Miller Aeron chair"
  handler       = "index.lambda_handler"
  runtime       = "python3.12"

  create_package         = false
  local_existing_package = local.lambda_function_zip
}
