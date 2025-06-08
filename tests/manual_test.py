#!/usr/bin/env python3
"""
Manual testing script for TDS Virtual TA API
"""

import requests
import json
import base64
from io import BytesIO
from PIL import Image

# Configuration
API_BASE_URL = "http://localhost:8000"

def create_test_image():
    """Create a simple test image and return as base64"""
    # Create a simple 100x100 white image with text
    img = Image.new('RGB', (100, 100), color='white')
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str

def test_health_check():
    """Test health check endpoints"""
    print("Testing health check endpoints...")
    
    # Test root endpoint
    response = requests.get(f"{API_BASE_URL}/")
    print(f"Root endpoint: {response.status_code} - {response.json()}")
    
    # Test health endpoint  
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Health endpoint: {response.status_code} - {response.json()}")

def test_question_endpoint():
    """Test the main question answering endpoint"""
    print("\nTesting question endpoint...")
    
    test_questions = [
        "What is FastAPI and how do I use it?",
        "How do I deploy a Python application to Vercel?",
        "What are the differences between git add and git commit?",
        "Should I use GPT-4o-mini or GPT-3.5-turbo for my project?",
        "How do I create a Docker container for my application?"
    ]
    
    for question in test_questions:
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/",
                json={"question": question},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Question: {question}")
                print(f"   Answer: {data['answer'][:100]}...")
                print(f"   Links: {len(data['links'])} references")
            else:
                print(f"❌ Question failed: {question}")
                print(f"   Status: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error testing question: {e}")
        
        print("-" * 50)

def test_image_question():
    """Test question with image input"""
    print("\nTesting image question...")
    
    try:
        test_image = create_test_image()
        
        response = requests.post(
            f"{API_BASE_URL}/api/",
            json={
                "question": "What do you see in this image?",
                "image": test_image
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Image question processed successfully")
            print(f"   Answer: {data['answer'][:100]}...")
        else:
            print(f"❌ Image question failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing image question: {e}")

def test_invalid_requests():
    """Test handling of invalid requests"""
    print("\nTesting invalid requests...")
    
    # Test empty question
    response = requests.post(
        f"{API_BASE_URL}/api/",
        json={"question": ""},
        headers={"Content-Type": "application/json"}
    )
    print(f"Empty question: {response.status_code} (should be 422)")
    
    # Test missing question field
    response = requests.post(
        f"{API_BASE_URL}/api/",
        json={},
        headers={"Content-Type": "application/json"}
    )
    print(f"Missing question: {response.status_code} (should be 422)")
    
    # Test invalid JSON
    response = requests.post(
        f"{API_BASE_URL}/api/",
        data="invalid json",
        headers={"Content-Type": "application/json"}
    )
    print(f"Invalid JSON: {response.status_code} (should be 422)")

def main():
    """Run all tests"""
    print("TDS Virtual TA - Manual API Testing")
    print("=" * 50)
    
    try:
        test_health_check()
        test_question_endpoint()
        test_image_question()
        test_invalid_requests()
        
        print("\n✅ Manual testing completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the API server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
