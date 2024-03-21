# Making a module for cpu & memory metric and you specify the ec2
# main.tf

variable "ec2_instance_id" {
  description = "The ID of the EC2 instance to attach CloudWatch alarms to"
}

module "cloudwatch_metrics" {
  source             = "./modules/cloudwatch_metrics"
  ec2_instance_id    = var.ec2_instance_id
}
# End of Main.tf

# modules/cloudwatch_metrics/main.tf

variable "ec2_instance_id" {
  description = "The ID of the EC2 instance to attach CloudWatch alarms to"
}

# Create CloudWatch alarms for CPU utilization
resource "aws_cloudwatch_metric_alarm" "cpu_alarm" {
  alarm_name          = "CPUUtilization-${var.ec2_instance_id}"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300" # 5 minutes
  statistic           = "Average"
  threshold           = "90" # Example threshold
  actions_enabled     = true

  dimensions = {
    InstanceId = var.ec2_instance_id
  }

  alarm_description = "Alarm when CPU utilization is greater than or equal to 90% for 2 consecutive periods"
}

# Create CloudWatch alarms for memory utilization
resource "aws_cloudwatch_metric_alarm" "memory_alarm" {
  alarm_name          = "MemoryUtilization-${var.ec2_instance_id}"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "2"
  metric_name         = "MemoryUtilization" # Example metric name (replace with actual memory metric name)
  namespace           = "Custom/Metrics"    # Example namespace (replace with actual namespace)
  period              = "300"               # 5 minutes
  statistic           = "Average"
  threshold           = "80"                # Example threshold
  actions_enabled     = true

  dimensions = {
    InstanceId = var.ec2_instance_id
  }

  alarm_description = "Alarm when memory utilization is greater than or equal to 80% for 2 consecutive periods"
}
