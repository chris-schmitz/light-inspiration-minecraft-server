resource "aws_security_group" "minecraft_security_group" {
  name   = "minecraft_security_group"
  vpc_id = aws_vpc.minecraft_vpc.id

  # TODO: limit to ssh and minecraft ports
  ingress {
    from_port   = 0
    protocol    = "-1"
    to_port     = 0
    cidr_blocks = [var.my_ip_address_in_cidr]
  }
  egress {
    from_port   = 0
    protocol    = "-1"
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_key_pair" "minecraft_auth" {
  key_name   = "minecraft_key"
  public_key = file("~/.ssh/minecraft_key.pub")
}

resource "aws_instance" "minecraft_ec2" {
  instance_type = "c6g.large"
  ami           = data.aws_ami.server_ami.id

  key_name        = aws_key_pair.minecraft_auth.key_name
  security_groups = [aws_security_group.minecraft_security_group.id]
  subnet_id       = aws_subnet.minecraft_subnet.id

  user_data = file("userdata.tpl")

  provisioner "local-exec" {
    command = templatefile("${path.module}/ssh-config.tpl", {
      serverLabel=self.tags.Name
      hostname= self.public_ip
      user= "ec2-user",
      identityFile = "~/.ssh/minecraft_key"
    })
    interpreter = ["bash", "-c"]
  }

  tags = {
    Name   = "minecraft-server"
    domain = "minecraft"
  }
}
