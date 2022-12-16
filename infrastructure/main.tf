resource "aws_vpc" "mincraft_vpc" {
  cidr_block = "10.123.0.0/16"
  enable_dns_hostnames = true
  tags = {
    domain = "minecraft"
  }
}