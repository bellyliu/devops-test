# Overview
This repository only containt ansible playbook & roles to deploy wordpress to EC2 instances that already running so i assume the underlying AWS infrastructure has been setup. Other than that this repo also containt cronjob that will auto create post in wordpress every hour.

# Assumptions
The underlying infrastructure has been setup which consists of:
- VPC
- Public & Private Subnets
- Internete Gateway
- NAT Gateway
- ALB
- Target Group
- EC2 Instances
    - That has tags `Name: Prod_Wordpress`
- Security Groups
- Mysql RDS Multi-AZ
- Amazon EFS
- Cloudwatch logs & alarm
- Jumpt/Bastion Host
- S3 Gateway & S3 Bucket
- Cloudfront
- Route53
# Architecture
![](https://raw.githubusercontent.com/bellyliu/devops-test/main/assets/AWS-Wordpress-HA.png)
### Architecture components

The reference architecture illustrates a complete best practice deployment for a WordPress website on AWS.
- Amazon CloudFront to cache content close to end users for fasterdelivery.
CloudFront pulls static content from an S3 bucket and dynamic content from an Application Load Balancer in front of the web instances.
- Application Load Balancer with `sticky session` enabled.
- The EC2 instances run in 2 AZ to achive High Availability.
- An Amazon RDS MySQL with multi-AZ mode enabled, so we have 1 standby RDS instance in another AZ.
- The WordPress EC2 instances access shared WordPress data on an Amazon EFS file system via an EFS Mount Target in each Availability Zone.
- An Internet Gateway enables communication between resources in your VPC and the internet.
- NAT Gateways in each Availability Zone enable EC2 instances in private subnets to access the internet.
- With S3 gateway endpoint, we can access Amazon S3  with no additional newtork cost since the traffic will going through AWS private network not internet.

# Ansible in Docker
I have created `Dockerfile-ansible` which can be used to run `wordpress.yml` playbook. Here is the steps:
- Build image
It requires us to provide aws_access_key, aws_secret_key, & aws_region as build arguments which will be used to  authenticate with AWS once we run the playbook
```shell
docker build -f Dockerfile-ansible -t ansible:1.0 --build-args aws_access_key=<YOUR KEY> --build-args aws_secret_key=<YOUR SECRET> --build-args aws_region=<REGION> .
```
- Run the ansible
```shell
docker run -ti ansible:1.0 ansible-playbook wordpress.yml
```
# Cronjob Auto Post
I have create simple python script that will create wordpress post that contain current date only. It will run every hour with the help of `cronjob`. The codes located in [cronjob_auto_post folder](https://github.com/bellyliu/devops-test/tree/main/cronjob_auto_post).
# Manual Processes
### Offloading Static Assets
We need to install & setup W3-Total-Cache plugin manually that allow us to leverage other AWS services like Amazon S3 and Amazon CloudFront to offload and store static content. Others may like the simplicity of storing all content on Amazon EFS and avoid installing and managing 3rd party plugins.
