# main.tf

provider "aws" {
  region = "us-east-1"  # Update with your preferred AWS region
}

# Create a VPC
resource "aws_vpc" "staging_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "staging-vpc"
  }
}

# Create a subnet in the VPC
resource "aws_subnet" "staging_subnet" {
  vpc_id                  = aws_vpc.staging_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"  # Update with your preferred availability zone

  tags = {
    Name = "staging-subnet"
  }
}

# Create a security group
resource "aws_security_group" "staging_security_group" {
  name        = "staging-security-group"
  description = "Allow incoming SSH and HTTP traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id = aws_vpc.staging_vpc.id

  tags = {
    Name = "staging-security-group"
  }
}

# Create an EC2 instance in the subnet with the security group
resource "aws_instance" "staging_instance" {
  ami           = "ami-12345678"  # Update with a valid AMI ID
  instance_type = "t2.micro"  # Update with your preferred instance type
  key_name      = "your-key-pair"  # Update with your key pair name

  subnet_id          = aws_subnet.staging_subnet.id
  security_group_ids = [aws_security_group.staging_security_group.id]

  tags = {
    Name = "staging-instance"
  }
}
