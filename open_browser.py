
#!/usr/bin/env python3
"""
إصلاح نهائي لمشكلة Selenium في Codespace
"""

import os
import sys
import subprocess

def fix_selenium():
    """إصلاح مشاكل Selenium"""
    print("🔧 جاري إصلاح مشاكل Selenium...")
    
    # 1. تثبيت المتطلبات
    print("📦 تثبيت/تحديث الحزم...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", 
                   "selenium", "webdriver-manager", "chromedriver-autoinstaller"], 
                   capture_output=True)
    
    # 2. تنظيف عمليات Chrome القديمة
    print("🧹 تنظيف العمليات القديمة...")
    subprocess.run(["pkill", "-f", "chrome"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-f", "chromedriver"], stderr=subprocess.DEVNULL)
    
    # 3. اختبار Selenium باستخدام chromedriver-autoinstaller
    print("🧪 اختبار Selenium بعد الإصلاح...")
    
    try:
        import chromedriver_autoinstaller
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        # تثبيت ChromeDriver تلقائياً
        chromedriver_path = chromedriver_autoinstaller.install()
        print(f"✅ تم تثبيت ChromeDriver في: {chromedriver_path}")
        
        # إعداد Chrome بسيط للغاية
        options = Options()
        options.add_argument("--headless")  # ضروري في Codespace
        options.add_argument("--no-sandbox")  # ضروري للغاية
        options.add_argument("--disable-dev-shm-usage")  # مهم للذاكرة
        
        # محاولة تشغيل Chrome
        print("🚀 جاري تشغيل Chrome...")
        driver = webdriver.Chrome(options=options)
        
        # اختبار بسيط
        driver.get("https://www.google.com")
        print(f"✅ Chrome يعمل! العنوان: {driver.title}")
        
        driver.quit()
        print("✅ تم إصلاح المشكلة بنجاح!")
        return True
        
    except Exception as e:
        print(f"❌ فشل الإصلاح: {e}")
        return False

def run_simple_test():
    """تشغيل اختبار بسيط"""
    print("\n" + "="*50)
    print("🧪 تشغيل اختبار بسيط")
    print("="*50)
    
    try:
        import chromedriver_autoinstaller
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import time
        
        # إعداد Chrome
        options = Options()
        
        # سؤال المستخدم
        print("\n🎯 كيف تريد فتح المتصفح؟")
        print("1. مع نافذة مرئية (قد لا يعمل في Codespace)")
        print("2. بدون نافذة (headless - الأفضل في Codespace)")
        
        choice = input("👉 أدخل 1 أو 2: ").strip()
        
        if choice == "1":
            print("⚠️  تحذير: النافذة المرئية قد لا تعمل بشكل جيد في Codespace")
            options.add_argument("--window-size=1280,720")
        else:
            options.add_argument("--headless")
        
        # الإعدادات الأساسية
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # سؤال عن الرابط
        url = input("\n🔗 أدخل الرابط (أو اترك فارغاً لـ Google): ").strip()
        if not url:
            url = "https://www.google.com"
        
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        print(f"\n🚀 جاري فتح: {url}")
        
        # تشغيل المتصفح
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(2)
        
        print(f"✅ تم الفتح بنجاح!")
        print(f"📄 العنوان: {driver.title}")
        print(f"🔗 الرابط: {driver.current_url}")
        print(f"📏 حجم الصفحة: {len(driver.page_source):,} حرف")
        
        # خيارات إضافية
        print("\n🎯 خيارات إضافية:")
        print("1. حفظ لقطة شاشة")
        print("2. حفظ HTML الصفحة")
        print("3. فتح موقع آخر")
        print("4. إغلاق المتصفح")
        
        while True:
            choice2 = input("\n👉 اختر خياراً (1-4): ").strip()
            
            if choice2 == "1":
                filename = f"screenshot_{int(time.time())}.png"
                driver.save_screenshot(filename)
                print(f"📸 تم حفظ لقطة شاشة: {filename}")
                
            elif choice2 == "2":
                filename = f"page_{int(time.time())}.html"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                print(f"💾 تم حفظ HTML: {filename}")
                
            elif choice2 == "3":
                new_url = input("🔗 أدخل الرابط الجديد: ").strip()
                if new_url:
                    if not new_url.startswith(("http://", "https://")):
                        new_url = "https://" + new_url
                    
                    driver.get(new_url)
                    time.sleep(2)
                    print(f"✅ تم فتح: {driver.title}")
                
            elif choice2 == "4":
                break
                
            else:
                print("❌ خيار غير صحيح")
        
        # إغلاق المتصفح
        driver.quit()
        print("\n👋 تم إغلاق المتصفح")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        print("\n💡 حاول استخدام الخيار 2 (headless)")

if __name__ == "__main__":
    print("="*60)
    print("🔧 إصلاح وتشغيل Selenium في Codespace")
    print("="*60)
    
    # محاولة الإصلاح أولاً
    if fix_selenium():
        # تشغيل الاختبار بعد الإصلاح
        run_simple_test()
    else:
        print("\n❌ فشل الإصلاح. يرجى المحاولة مرة أخرى.")

