"""Summarize actual Trivy JSON reports; never synthesize scan findings."""

import json
from pathlib import Path
import sys

folder = Path(sys.argv[1] if len(sys.argv) > 1 else "reports")
summary = {}
lines = ["# TP 3 - Comparaison Trivy", "", "| Image | HIGH | CRITICAL |", "| --- | ---: | ---: |"]
for label in ["before", "after"]:
    report = json.loads((folder / f"trivy-{label}.json").read_text(encoding="utf-8"))
    vulnerabilities = [v for result in report.get("Results", []) for v in result.get("Vulnerabilities", []) if v["Severity"] in {"HIGH", "CRITICAL"}]
    counts = {severity: sum(v["Severity"] == severity for v in vulnerabilities) for severity in ["HIGH", "CRITICAL"]}
    examples = sorted(vulnerabilities, key=lambda v: (v["Severity"] != "CRITICAL", v["PkgName"], v["VulnerabilityID"]))[:3]
    summary[label] = {
        "artifact_name": report.get("ArtifactName"),
        "image_id": report.get("Metadata", {}).get("ImageID"),
        "os": report.get("Metadata", {}).get("OS"),
        "counts": counts,
        "examples": [{key: v.get(key, "") for key in ["PkgName", "InstalledVersion", "Severity", "VulnerabilityID", "FixedVersion", "PrimaryURL"]} for v in examples],
    }
    lines.append(f"| {label} | {counts['HIGH']} | {counts['CRITICAL']} |")
for label in ["before", "after"]:
    lines.extend(["", f"## {label}", "", "| Composant | Version | Gravité | CVE | Version corrigée |", "| --- | --- | --- | --- | --- |"])
    for v in summary[label]["examples"]:
        lines.append("| " + " | ".join([v["PkgName"], v["InstalledVersion"], v["Severity"], v["VulnerabilityID"], v["FixedVersion"] or "Non disponible"]) + " |")
    if not summary[label]["examples"]:
        lines.append("| Aucun résultat HIGH/CRITICAL détecté | - | - | - | - |")
lines.extend(["", "Résultats issus des deux rapports JSON Trivy de ce run. Les bases Debian et Alpine contiennent des paquets différents : une entrée absente après changement de base ne prouve pas à elle seule qu'un correctif a été appliqué au même paquet.", ""])
(folder / "comparison.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
(folder / "comparison.md").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
