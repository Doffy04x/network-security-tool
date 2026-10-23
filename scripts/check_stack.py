"""Record Compose runtime settings and verify the applied hardening."""

import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=["before", "after"])
parser.add_argument("compose")
parser.add_argument("project")
parser.add_argument("output")
args = parser.parse_args()


def run(*command):
    return subprocess.run(command, capture_output=True, text=True, check=True).stdout.strip()


services = {}
for service in ["api", "nginx"]:
    container = run("docker", "compose", "-p", args.project, "-f", args.compose, "ps", "-q", service)
    assert container, f"{service} is missing"
    info = json.loads(run("docker", "inspect", container))[0]
    uid = run("docker", "exec", container, "id", "-u")
    services[service] = {
        "image": info["Config"]["Image"],
        "image_id": info["Image"],
        "uid": int(uid),
        "running": info["State"]["Running"],
        "health": info["State"].get("Health", {}).get("Status"),
        "read_only": info["HostConfig"]["ReadonlyRootfs"],
        "cap_drop": info["HostConfig"]["CapDrop"],
        "security_opt": info["HostConfig"]["SecurityOpt"],
        "published_ports": info["NetworkSettings"]["Ports"],
        "networks": list(info["NetworkSettings"]["Networks"]),
        "mounts": [{"destination": mount["Destination"], "writable": mount["RW"], "type": mount["Type"]} for mount in info["Mounts"]],
    }
    assert services[service]["running"]

backend = json.loads(run("docker", "network", "inspect", args.project + "_backend"))[0]
report = {"mode": args.mode, "services": services, "backend_internal": backend["Internal"]}
if args.mode == "after":
    for service in services.values():
        assert service["uid"] != 0
        assert service["read_only"] is True
        assert "ALL" in (service["cap_drop"] or [])
        assert any(option.startswith("no-new-privileges") for option in service["security_opt"] or [])
        assert service["health"] == "healthy"
    assert services["api"]["published_ports"].get("8000/tcp") is None
    assert services["api"]["networks"] == [args.project + "_backend"]
    assert report["backend_internal"] is True
    binding = services["nginx"]["published_ports"]["8080/tcp"]
    assert binding == [{"HostIp": "127.0.0.1", "HostPort": "8080"}]
    assert all(not mount["writable"] for mount in services["nginx"]["mounts"] if mount["type"] == "bind")
else:
    assert services["api"]["uid"] == 0
    assert services["api"]["published_ports"].get("8000/tcp")

Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
