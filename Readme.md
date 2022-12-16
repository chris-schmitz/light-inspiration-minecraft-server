# Light Inspiration Minecraft Server 

## Overview

This is an infrastructure as code project that serves several purposes:

- Setting up a private mincraft server on aws for my family to play on
- As a practical practice project for learning more about aws, terraform, and infrastructure as code in general
- As a engineering learning session demo

## Challenges to overcome
- Pointing the route53 dns records to the ec2 instance ip address in code
- Best way of installing, configuring, and launching minecraft server once the instance is upG

## The infrastructure 


### Security Group rules
**Inbound rules**:
- 22: ssh
- 25565: minecraft client port

**Outbound rules**:
- All ports

### EC2 instance details
Multiplayer minecraft requires a decent amount of power, so to run it we'll be using a **c6g.medium** EC2 instance type. 


### Route 53

## Planning notes

### Picking the instance type
We're using a `c6g.medium` ec2 instance. This type was decided based on the facts:

- Minecraft java edition requires an ARM processor to run on a linux instance
- We need a decent amount of ram to run multiplayer

### To scale or not to scale
One of the concerns/questions I had while thinking through this project is: how many players can a single minecraft server support -> do we need to be concerned with scaling?

The plan for the server at this point is to have maybe 5 people at the most playing at the same time. Looking it up:

> One minecraft server application can't support more than about 20 players per gb of RAM. Beyond that critical point of ~200 players, however, it's not the RAM that's the problem, but the CPU.

So, considering we're using a `c6g.medium` ec2 instance with 2 gb of ram:
- We're well within the playable limits with our estimated total player count
- Figuring out scaling would be premature optimization
  - Not to mention the concept of scaling a java application that requires player communication and interaction across instances is [a non-trivial task](https://www.worldql.com/posts/2021-08-worldql-scalable-minecraft/)
- If we ever got to the point where we needed more players it would be worth paying for a service that already handles it and transferring our world instance there

## Resources
- [Making Amazon Route 53 the DNS service for an existing domain](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/MigratingDNS.html)
- [Routing traffic to an Amazon EC2 instance](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-ec2-instance.html)
- [Example of a simple route53 -> ec2 instance terraform structure](https://stackoverflow.com/questions/63307373/terraform-route53-simplest-example-to-create-a-dns-record-in-hosted-zone-pointin)
- [Helpful walkthrough re: getting started with aws via terraform](https://www.youtube.com/watch?v=iRaai1IBlB0&ab_channel=freeCodeCamp.org)
### Terraform tools
- [aws_provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [aws_route53_record](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route53_record)
- [aws_security_group](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group)
- [aws_instance](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance)