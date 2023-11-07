provider "aws" {
    region = "us-east-1"# Set your desired AWS region
}

resource "aws_vpc" "my_vpc" {
    cidr_block = "10.0.0.0/16"# Replace with your desired CIDR block
    enable_dns_support = true
    enable_dns_hostnames = true
    tags = {
    Name = "MyVPC"
}
}

resource "aws_subnet" "my_subnet" {
    count = 1# You can create multiple subnets by changing the count
    vpc_id = aws_vpc.my_vpc.id
    cidr_block = "10.0.0.0/24"# Replace with your desired subnet CIDR block
    availability_zone = "us-east-1a"# Replace with your desired availability zone
    tags = {
    Name = "MySubnet"
}
}

resource "aws_internet_gateway" "my_internet_gateway" {
    vpc_id = aws_vpc.my_vpc.id
    tags = {
    Name = "MyInternetGateway"
}
}