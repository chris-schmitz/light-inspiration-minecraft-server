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

resource "aws_security_group" "minecraft_security_group" {
  name = "minecraft_security_group"
  vpc_id = aws_vpc.minecraft_vpc.id

  ingress {
    from_port = 0
    protocol  = "-1"
    to_port   = 0
    cidr_blocks = [var.my_ip_address_in_cidr]
  }
  egress {
    from_port = 0
    protocol  = ""
    to_port   = 0
  }
}