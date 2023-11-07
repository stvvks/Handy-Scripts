provider "aws" {
    region = "us-east-1"# Set your desired AWS region
}

resource "aws_sns_topic" "cloudwatch_alarm_notifications" {
    name = "CloudWatchAlarmNotifications"
}

resource "aws_cloudwatch_metric_alarm" "high_cpu_alarm" {
    alarm_name= "HighCPULoad"
    comparison_operator = "GreaterThanOrEqualToThreshold"
    evaluation_periods = 1
    metric_name = "CPUUtilization"
    namespace = "AWS/EC2"
    period = 300
    statistic = "Average"
    threshold = 80
    alarm_description = "CPU utilization is high"
    alarm_action = aws_sns_topic.cloudwatch_alarm_notifications.arn

dimensions = {
    InstanceId = aws_instance.example.id
}
}

resource "aws_sns_topic_subscription" "slack_notification" {
    topic_arn = aws_sns_topic.cloudwatch_alarm_notifications.arn
    protocol = "https"
    endpoint = "https://hooks.slack.com/services/your/slack/webhook/endpoint"
}