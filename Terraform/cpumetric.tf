# Making a map for ec2 instances for one metric
# Define the list of EC2 instances
variable "ec2_instance_ids" {
  type    = list(string)
  default = ["instance_id_1", "instance_id_2"] # Add more instance IDs as needed
}

# Map EC2 instance IDs to CloudWatch alarm names
locals {
  cloudwatch_alarms = {
    for instance_id in var.ec2_instance_ids : instance_id => "CPUUtilization-${instance_id}"
  }
}

# Create CloudWatch alarms for CPU utilization
resource "aws_cloudwatch_metric_alarm" "cpu_alarm" {
  for_each          = local.cloudwatch_alarms
  alarm_name        = each.value
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300" # 5 minutes
  statistic           = "Average"
  threshold           = "90" # Example threshold
  actions_enabled     = true

  dimensions = {
    InstanceId = each.key
  }

  alarm_description = "Alarm when CPU utilization is greater than or equal to 90% for 2 consecutive periods"
}
