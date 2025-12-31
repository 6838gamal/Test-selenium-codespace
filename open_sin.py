#!/usr/bin/env python3
"""
اختبار Selenium - يفتح كل موقع في نافذة جديدة مستقلة
"""

import os
import sys
import time

print("="*60)
print("🚀 Selenium Test - Opens each site in NEW WINDOW")
print("="*60)

# بسيط ومباشر
from selenium import webdriver

def open_site_in_new_window(url, site_name):
    """يتم فتح كل موقع في نافذة متصفح جديدة مستقلة"""
    print(f"\n🎯 Opening: {site_name}")
    print(f"   URL: {url}")
    
    try:
        # إعدادات Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # لجعل النافذة كبيرة وواضحة
        options.add_argument("--start-maximized")
        
        # إنشاء نافذة جديدة
        driver = webdriver.Chrome(options=options)
        
        # فتح الموقع
        driver.get(url)
        time.sleep(3)  # انتظار التحميل
        
        print(f"✅ SUCCESS: {site_name} opened in new window")
        print(f"   Title: {driver.title}")
        print(f"   Window ID: {driver.current_window_handle}")
        
        # لقطة شاشة للتوثيق
        if "import-dep" in url:
            filename = f"IMPORT_DEP_{int(time.time())}.png"
            driver.save_screenshot(filename)
            print(f"📸 Screenshot saved: {filename}")
        
        # إبقاء النافذة مفتوحة
        print(f"💡 The window for {site_name} will stay open")
        print("   Close it manually when done")
        
        return driver
        
    except Exception as e:
        print(f"❌ FAILED to open {site_name}: {e}")
        return None

# المواقع المراد فتحها
sites_to_open = [
    ("https://www.google.com", "Google"),
    ("https://github.com", "GitHub"),
    ("https://www.python.org", "Python"),
    ("https://import-dep.mega-sy.com/registration", "TARGET SITE - Import Dep"),
]

print("\n" + "="*60)
print("SITES TO OPEN (each in separate window):")
print("="*60)
for i, (url, name) in enumerate(sites_to_open, 1):
    print(f"{i}. {name:20} - {url}")

print("\n" + "="*60)
input("Press Enter to start opening sites...")

# فتح كل موقع في نافذة جديدة
all_windows = []
for url, name in sites_to_open:
    driver = open_site_in_new_window(url, name)
    if driver:
        all_windows.append((name, driver))
    
    # انتظار 2 ثانية بين كل نافذة
    time.sleep(2)

print("\n" + "="*60)
print("✅ ALL SITES OPENED SUCCESSFULLY!")
print("="*60)
print(f"📊 Total windows opened: {len(all_windows)}")
print("\nYou can now:")
print("1. Test each site manually")
print("2. Close windows when finished")
print("3. The program will exit after you press Enter")

input("\nPress Enter when you're done testing...")

print("\n👋 Test completed!")
print("Remember to close browser windows manually")
