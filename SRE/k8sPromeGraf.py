from kubernetes import client, config
import yaml
import os

def create_prometheus_service_monitor(namespace, service_name, port, interval="30s"):
    # Load Kubernetes config
    config.load_kube_config()

    # Create ServiceMonitor object
    api_instance = client.CustomObjectsApi()
    service_monitor = {
        "apiVersion": "monitoring.coreos.com/v1",
        "kind": "ServiceMonitor",
        "metadata": {"name": f"{service_name}-monitor", "namespace": namespace},
        "spec": {
            "endpoints": [{"port": port}],
            "selector": {"matchLabels": {"app": service_name}},
            "namespaceSelector": {"matchNames": [namespace]},
            "interval": interval,
        },
    }

    # Create the ServiceMonitor
    api_instance.create_namespaced_custom_object(
        group="monitoring.coreos.com",
        version="v1",
        namespace=namespace,
        plural="servicemonitors",
        body=service_monitor,
    )

    print(f"Prometheus ServiceMonitor for {service_name} created successfully.")

def create_grafana_dashboard(namespace, dashboard_file):
    # Load Kubernetes config
    config.load_kube_config()

    # Create ConfigMap from Grafana dashboard YAML file
    with open(dashboard_file, "r") as f:
        dashboard_yaml = yaml.safe_load(f)

    cm_name = os.path.basename(dashboard_file).replace(".yaml", "")
    config_map = client.V1ConfigMap(
        api_version="v1",
        kind="ConfigMap",
        metadata={"name": cm_name, "namespace": namespace},
        data={"dashboard.json": yaml.dump(dashboard_yaml)},
    )

    # Create the ConfigMap
    core_v1_api = client.CoreV1Api()
    core_v1_api.create_namespaced_config_map(namespace=namespace, body=config_map)

    print(f"Grafana dashboard '{cm_name}' created successfully.")

# Example usage
namespace = "your-namespace"
service_name = "your-service"
port = 8080
interval = "30s"
dashboard_file = "path/to/grafana_dashboard.yaml"

create_prometheus_service_monitor(namespace, service_name, port, interval)
create_grafana_dashboard(namespace, dashboard_file)
