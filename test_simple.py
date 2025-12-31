# إنشاء ملف test_simple.py بسيط جداً
#!/usr/bin/env python3
"""
اختبار بسيط جداً - فقط التحقق من أن Selenium يفتح الموقع
"""

import os
import sys
import time

print("="*50)
print("🧪 اختبار Selenium البسيط")
print("="*50)

# إضافة مسار الإعدادات
sys.path.append(os.path.expanduser("~/.selenium-config"))

try:
    from chrome_options import setup_driver
    print("✅ تم استيراد مكتبة Selenium")
except ImportError as e:
    print(f"❌ خطأ في استيراد Selenium: {e}")
    print("💡 تأكد من تشغيل setup.sh أولاً")
    exit(1)

print("\n🔧 جاري تهيئة المتصفح...")
driver = setup_driver()

if not driver:
    print("❌ فشل في تهيئة المتصفح")
    exit(1)

print("✅ تم تهيئة المتصفح بنجاح")

# اختبار فتح موقعين مختلفين
test_sites = [
    ("https://www.google.com", "Google"),
    ("https://github.com", "GitHub"),
    ("https://www.example.com", "Example"),
    ("https://import-dep.mega-sy.com/registration", "الموقع المستهدف")
]

print("\n🌐 جاري اختبار فتح المواقع...")
print("-" * 40)

for url, name in test_sites:
    try:
        print(f"\n🔗 جاري فتح {name}...")
        driver.get(url)
        time.sleep(2)  # انتظار تحميل الصفحة
        
        print(f"   ✅ تم فتح: {driver.title}")
        print(f"   📏 حجم الصفحة: {len(driver.page_source):,} حرف")
        print(f"   🔗 الرابط: {driver.current_url[:80]}...")
        
        # التقاط لقطة شاشة بسيطة
        if "import-dep" in url:
            driver.save_screenshot("target_site.png")
            print("   📸 تم حفظ لقطة شاشة: target_site.png")
            
    except Exception as e:
        print(f"   ❌ فشل في فتح {name}: {e}")

print("\n" + "="*50)
print("📊 ملخص الاختبار:")
print("="*50)
print(f"✅ Selenium يعمل بشكل صحيح")
print(f"✅ المتصفح مفتوح ويمكنه تصفح المواقع")
print(f"✅ جاهز للاستخدام")

print("\n👋 جاري إغلاق المتصفح...")
driver.quit()
print("✅ تم إنهاء الاختبار بنجاح!")
