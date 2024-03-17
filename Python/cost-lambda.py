import boto3

# Initialize AWS Lambda client
lambda_client = boto3.client('lambda')

# Specify the Lambda function to test
function_name = 'your-lambda-function-name'

# Specify the range of memory sizes to test (in MB)
min_memory = 128
max_memory = 3008
memory_increment = 64

def lambda_handler(event, context):
    # Initialize dictionary to store cost results
    cost_results = {}

    # Iterate over memory sizes
    for memory_size in range(min_memory, max_memory + 1, memory_increment):
        # Update Lambda function configuration with current memory size
        lambda_client.update_function_configuration(
            FunctionName=function_name,
            MemorySize=memory_size
        )

        # Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload='{}'
        )

        # Calculate cost based on Lambda pricing model
        billed_duration = response['ExecutionTime'] / 1000  # Billed duration in seconds
        cost_per_invocation = 0.0000002  # Cost per GB-second for Lambda executions
        cost = billed_duration * (memory_size / 1024) * cost_per_invocation  # Cost in dollars

        # Store cost result for current memory size
        cost_results[memory_size] = cost

    # Output cost results
    print("Memory Size (MB)  Cost ($)")
    for memory_size, cost in cost_results.items():
        print(f"{memory_size:<16} {cost:.2f}")

    # Determine the memory size with the lowest cost
    optimal_memory_size = min(cost_results, key=cost_results.get)
    print(f"\nOptimal Memory Size for Cost Optimization: {optimal_memory_size} MB")
