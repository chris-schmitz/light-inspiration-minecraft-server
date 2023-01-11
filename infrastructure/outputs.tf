output "public_ip" {
  description = "The server's public IP address"
  value = aws_instance.minecraft_ec2.public_ip
}

output "ssh-config" {
  description = "The new server's ssh config"
  value = templatefile("${path.module}/ssh-config.tpl", {
    serverLabel=aws_instance.minecraft_ec2.tags.Name
    hostname= aws_instance.minecraft_ec2.public_ip
    user= "ec2-user",
    identityFile = "~/.ssh/minecraft_key"
  })
}
