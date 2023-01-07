output "public_ip" {
  description = "The server's public IP address"
  value = aws_instance.minecraft_ec2.public_ip
}
