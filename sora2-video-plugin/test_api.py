"""
Direct API test script for Zhenzhen platform Sora2 API
Run with: python test_api.py
"""

import requests
import time
import json
import sys
import io

# Fix Unicode output for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Test credentials
API_KEY = "sk-2TqUEzLnk28nJzvXBRPlMX25a1F23hYXZy0BlRxDtWE4Kcn0"
BASE_URL = "https://ai.t8star.cn"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def test_text_to_video():
    """Test text-to-video API"""
    print("\n=== Testing Text-to-Video ===")

    params = {
        "prompt": "一只可爱的橙猫在草地上奔跑",
        "model": "sora-2",
        "duration": "10",
        "aspect_ratio": "16:9"
    }

    print(f"Creating task with params: {json.dumps(params, ensure_ascii=False)}")

    # Create task
    response = requests.post(
        f"{BASE_URL}/v2/videos/generations",
        headers=HEADERS,
        json=params,
        timeout=30
    )

    print(f"Response status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        task_id = data.get("task_id")
        print(f"[OK] Task created successfully!")
        print(f"  Task ID: {task_id}")

        # Query task status
        if task_id:
            print("\nPolling task status...")
            for i in range(5):  # Poll up to 5 times
                time.sleep(5)  # Wait 5 seconds between polls
                response = requests.get(
                    f"{BASE_URL}/v2/videos/generations/{task_id}",
                    headers=HEADERS,
                    timeout=10
                )
                if response.status_code == 200:
                    task_data = response.json()
                    status = task_data.get("status")
                    print(f"  Poll {i+1}: Status = {status}")
                    if status == "SUCCESS":
                        video_url = task_data.get("data", {}).get("output")
                        print(f"  [OK] Video URL: {video_url}")
                        break
                    elif status == "FAILURE":
                        fail_reason = task_data.get("fail_reason", "Unknown error")
                        print(f"  [FAIL] Task failed: {fail_reason}")
                        break
                else:
                    print(f"  [FAIL] Query failed: {response.status_code}")
                    break
    else:
        print(f"[FAIL] Request failed: {response.status_code}")
        print(f"  Response: {response.text[:500]}")


def test_image_to_video():
    """Test image-to-video API"""
    print("\n=== Testing Image-to-Video ===")

    image_url = "https://lowly-rain-658.notion.site/image/attachment%3A2a817484-73a6-474a-a7ea-ca013e594c3d%3A3.jpg?table=block&id=2d8a3f92-69aa-8036-8f5b-fadc62538c98&spaceId=86aa3f92-69aa-81db-ab3d-00033d2c4978&width=2000&userId=&cache=v2"

    params = {
        "prompt": "让图片中的角色动起来",
        "model": "sora-2",
        "duration": "10",
        "images": [image_url]
    }

    print(f"Creating task with params: {json.dumps(params, ensure_ascii=False)}")

    # Create task
    response = requests.post(
        f"{BASE_URL}/v2/videos/generations",
        headers=HEADERS,
        json=params,
        timeout=30
    )

    print(f"Response status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        task_id = data.get("task_id")
        print(f"[OK] Task created successfully!")
        print(f"  Task ID: {task_id}")

        # Query task status once
        if task_id:
            time.sleep(3)
            response = requests.get(
                f"{BASE_URL}/v2/videos/generations/{task_id}",
                headers=HEADERS,
                timeout=10
            )
            if response.status_code == 200:
                task_data = response.json()
                status = task_data.get("status")
                print(f"  Status: {status}")
            else:
                print(f"  [FAIL] Query failed: {response.status_code}")
    else:
        print(f"[FAIL] Request failed: {response.status_code}")
        print(f"  Response: {response.text[:500]}")


def test_provider_validation():
    """Test provider credential validation"""
    print("\n=== Testing Provider Validation ===")

    response = requests.get(
        f"{BASE_URL}/v2/videos/generations",
        headers=HEADERS,
        timeout=10
    )

    print(f"Validation response status: {response.status_code}")

    if response.status_code == 401:
        print("[FAIL] Invalid API Key")
    elif response.status_code in [200, 404, 405]:
        print("[OK] API Key is valid (endpoint accessible)")
    else:
        print(f"Response: {response.text[:500]}")


if __name__ == "__main__":
    print("Sora2 API Test Script")
    print("=" * 40)

    # Test 1: Provider validation
    test_provider_validation()

    # Test 2: Text-to-video
    test_text_to_video()

    # Test 3: Image-to-video
    test_image_to_video()

    print("\n" + "=" * 40)
    print("Tests completed!")
