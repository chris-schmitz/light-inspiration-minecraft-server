resource "aws_vpc" "minecraft_vpc" {
  cidr_block           = "10.123.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "minecraft-vpc"
    domain = "minecraft"
  }
}

resource "aws_subnet" "minecraft_subnet" {
  vpc_id     = aws_vpc.minecraft_vpc.id
  cidr_block = "10.123.1.0/24"
  map_public_ip_on_launch = true
  availability_zone = "us-east-1a"

  tags = {
    domain = "minecraft"
    visibility = "public"
  }
}

resource "aws_internet_gateway" "minecraft_internet_gateway" {
  vpc_id = aws_vpc.minecraft_vpc.id

  tags = {
    domain = "minecraft"
  }
}

resource "aws_route_table" "minecraft_route_table" {
  vpc_id = aws_vpc.minecraft_vpc.id

  tags = {
    domain = "minecraft"
    visibility = "public"
  }
}

resource "aws_route" "default_route" {
  route_table_id = aws_route_table.minecraft_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.minecraft_internet_gateway.id
}

resource "aws_route_table_association" "minecraft_route_table_association" {
  route_table_id = aws_route_table.minecraft_route_table.id
  subnet_id = aws_subnet.minecraft_subnet.id
}