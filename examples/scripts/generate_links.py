"""
Generate 3D viewer links for model files in the examples/scenarios folder.

This script checks all scenarios in the examples/scenarios folder,
finds model files (.obj and .mtl), builds GitHub URLs for each file,
and creates a 3D viewer URL that can be used to view the models online.
"""

import os
from typing import List, Dict

SCENARIOS_DIR = "examples/scenarios"
GITHUB_BASE_URL = "https://github.com/KoStard/optics_raytracer/blob/master"
VIEWER_BASE_URL = "https://3dviewer.net/#model="

def get_model_files(scenario_dir: str) -> List[str]:
    """Get all OBJ and MTL files in the scenario directory with their relative paths."""
    model_files = []
    full_path = os.path.join(SCENARIOS_DIR, scenario_dir)

    for file in sorted(os.listdir(full_path)):
        if file.endswith(".obj") or file.endswith(".mtl"):
            # Store relative path for GitHub URL
            relative_path = os.path.join(SCENARIOS_DIR, scenario_dir, file)
            model_files.append(relative_path)

    return model_files

def build_github_url(file_path: str) -> str:
    """Build a GitHub URL for a file."""
    return f"{GITHUB_BASE_URL}/{file_path}"

def build_viewer_url(github_urls: List[str]) -> str:
    """Build a 3D viewer URL from GitHub URLs."""
    return f"{VIEWER_BASE_URL}{','.join(github_urls)}"

def process_scenarios() -> Dict[str, Dict]:
    """Process all scenarios and build URLs."""
    results = {}

    # Get all scenario directories
    scenario_dirs = sorted([d for d in os.listdir(SCENARIOS_DIR)
                     if os.path.isdir(os.path.join(SCENARIOS_DIR, d))])

    for scenario_dir in scenario_dirs:
        model_files = get_model_files(scenario_dir)

        # Build GitHub URLs
        github_urls = [build_github_url(file) for file in model_files]

        # Build viewer URL
        viewer_url = build_viewer_url(github_urls)

        results[scenario_dir] = {
            "model_files": model_files,
            "github_urls": github_urls,
            "viewer_url": viewer_url
        }

    return results

def main():
    """Main function to process scenarios and print results."""
    results = process_scenarios()

    print("# 3D Model Viewer Links")
    print()

    for scenario_name, data in sorted(results.items()):
        print(f"## {scenario_name}")
        print(f"Viewer URL: {data['viewer_url']}")
        print()

        print("### Individual model files:")
        for i, (file, url) in enumerate(zip(data["model_files"], data["github_urls"])):
            print(f"{i+1}. [{os.path.basename(file)}]({url})")
        print()

if __name__ == "__main__":
    main()
