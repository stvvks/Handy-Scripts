import subprocess
import os
import configparser
import signal

# Exit script cleanly if interupted
def signal_handler(signum, frame):
    print('Interrupted! Exiting...')
    exit(1)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

################################################################################
#                             Initial Setup                                    #
################################################################################

def execute_command(command, interactive=True):
    try:
        if interactive:
            print(f"Executing interactive command: {command}")
            process = subprocess.Popen(command, shell=True)
            process.communicate()
            return process.returncode == 0
        else:
            print(f"Executing command: {command}")
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            out = out.decode("utf-8").strip()
            err = err.decode("utf-8").strip()
            if process.returncode != 0:
                print(f"Command failed with error: {err}")
                return False, err
            else:
                print(out)
                return True, out
    except KeyboardInterrupt:
        print('Interrupted! Exiting...')
        exit(1)

# Check if AWS credentials exists, prompt to create if not.
def check_aws_profile_exists(profile_name):
    aws_credentials_path = os.path.expanduser("~/.aws/credentials")
    if os.path.exists(aws_credentials_path):
        config = configparser.ConfigParser()
        config.read(aws_credentials_path)
        if profile_name in config.sections():
            return True
    return False

# AWS Configuration
aws_profile = 'default'

# Terraform Configuration
terraform_directory = "../terraform"

# Initial AWS setup
print("Checking if AWS profile exists...")
if not check_aws_profile_exists(aws_profile):
    print("AWS profile does not exist. Configuring...")
    success = execute_command("aws configure", interactive=True)
    if not success:
        print("Failed to set AWS profile. Exiting.")
        exit(1)
else:
    print("AWS profile exists. Proceeding...")
################################################################################
#                             Application Build                                #
################################################################################
print("Starting Gradle build...")
def run_gradlew_bootjar():
    os.chdir("../hello-world/")
    
    try:
        print("Running Gradle bootJar...")
        result = subprocess.run(["./gradlew", "bootJar"], check=True, capture_output=True, text=True)
        
        print("Standard Output:", result.stdout)
        print("Standard Error:", result.stderr)
        
        print("Successfully compiled the JAR.")
        return True
        
    except subprocess.CalledProcessError as e:
        print("Standard Output:", e.stdout)
        print("Standard Error:", e.stderr)
        
        print("Failed to compile the JAR.")
        return False

success = run_gradlew_bootjar()
if not success:
    print("Failed to compile the JAR. Exiting.")
    exit(1)

################################################################################
#                             Docker Build & Push Stage                        #
################################################################################

# Docker Configuration
docker_image_name = "hello-world"
docker_tag = "v1"
ecr_repo_name = "684235178456.dkr.ecr.us-east-1.amazonaws.com/rocketmiles/hello-world"
ecr_repo_url = f"{ecr_repo_name}:{docker_tag}"

# Change to the 'build' directory
os.chdir('../hello-world')

# Build Docker Image 
success = execute_command(f"docker build -t {docker_image_name}:{docker_tag} .", interactive=True)
if not success:
    print(f"Failed to build Docker image. Exiting.")
    exit(1)

# Tag Docker Image for ECR 
success = execute_command(f"docker tag {docker_image_name}:{docker_tag} {ecr_repo_url}", interactive=True)
if not success:
    print("Failed to tag Docker image for ECR. Exiting.")
    exit(1)

# Push to ECR 
success = execute_command(f"docker push {ecr_repo_url}", interactive=True)
if not success:
    print("Failed to push Docker image to ECR. Exiting.")
    exit(1)


################################################################################
#                             Terraform Stage                       #
################################################################################

# Initialize Terraform
success = execute_command(f"cd {terraform_directory} && terraform init", interactive=True)
if not success:
    print("Failed to initialize Terraform. Exiting.")
    exit(1)

# Apply Terraform configuration
success = execute_command(f"cd {terraform_directory} && terraform apply -var 'docker_tag={docker_tag}'", interactive=True)
if not success:
    print("Failed to apply Terraform configurations. Exiting.")
    exit(1)