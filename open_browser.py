
#!/usr/bin/env python3
"""
فتح المتصفح مع خيارات متعددة - يعرض نافذة مرئية أو خفية حسب الاختيار
"""

import os
import sys
import time

print("="*60)
print("🌐 فتح المتصفح مع خيارات متعددة")
print("="*60)

# إضافة مسار الإعدادات
sys.path.append(os.path.expanduser("~/.selenium-config"))

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.common.by import By
    
    print("✅ مكتبة Selenium جاهزة")
    
except ImportError as e:
    print(f"❌ خطأ في استيراد Selenium: {e}")
    print("💡 تأكد من تثبيت: pip install selenium")
    exit(1)

def setup_chrome(headless=False):
    """إعداد متصفح Chrome"""
    print(f"\n🔧 إعداد Chrome (headless={'نعم' if headless else 'لا'})...")
    
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless=new")
    
    # إعدادات ضرورية للعمل في Codespace
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # إعدادات النافذة
    if not headless:
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.add_argument("--start-maximized")
    
    # User-Agent واقعي
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # إعدادات لمكافحة الكشف
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # محاولة استخدام ChromeDriver الموجود
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Chrome جاهز للاستخدام")
        return driver
    except Exception as e:
        print(f"❌ فشل في تشغيل Chrome: {e}")
        return None

def setup_firefox(headless=False):
    """إعداد متصفح Firefox"""
    print(f"\n🦊 إعداد Firefox (headless={'نعم' if headless else 'لا'})...")
    
    firefox_options = FirefoxOptions()
    
    if headless:
        firefox_options.add_argument("--headless")
    
    # إعدادات النافذة
    if not headless:
        firefox_options.add_argument("--width=1280")
        firefox_options.add_argument("--height=720")
    
    try:
        driver = webdriver.Firefox(options=firefox_options)
        print("✅ Firefox جاهز للاستخدام")
        return driver
    except Exception as e:
        print(f"❌ فشل في تشغيل Firefox: {e}")
        return None

def main():
    """الدالة الرئيسية"""
    
    print("\n🎯 اختر المتصفح الذي تريد استخدامه:")
    print("1. Chrome (مع نافذة مرئية)")
    print("2. Chrome (بدون نافذة - خفي)")
    print("3. Firefox (مع نافذة مرئية)")
    print("4. Firefox (بدون نافذة - خفي)")
    print("5. اختبار جميع الخيارات")
    print("6. الخروج")
    
    while True:
        try:
            choice = input("\n👉 أدخل رقم الخيار (1-6): ").strip()
            
            if choice == "1":
                driver = setup_chrome(headless=False)
                browser_name = "Chrome مرئي"
            elif choice == "2":
                driver = setup_chrome(headless=True)
                browser_name = "Chrome خفي"
            elif choice == "3":
                driver = setup_firefox(headless=False)
                browser_name = "Firefox مرئي"
            elif choice == "4":
                driver = setup_firefox(headless=True)
                browser_name = "Firefox خفي"
            elif choice == "5":
                test_all_browsers()
                return
            elif choice == "6":
                print("\n👋 مع السلامة!")
                return
            else:
                print("❌ خيار غير صحيح. الرجاء اختيار 1-6")
                continue
            
            if not driver:
                print("❌ فشل في تهيئة المتصفح")
                continue
            
            # فتح المواقع
            open_websites(driver, browser_name)
            
            # السؤال عما إذا كان يريد فتح متصفح آخر
            again = input("\n🔁 هل تريد فتح متصفح آخر؟ (نعم/لا): ").strip().lower()
            if again not in ["نعم", "yes", "y"]:
                break
                
        except KeyboardInterrupt:
            print("\n\n⏹️ تم إيقاف البرنامج")
            break
        except Exception as e:
            print(f"\n❌ خطأ غير متوقع: {e}")

def open_websites(driver, browser_name):
    """فتح المواقع المختلفة"""
    print(f"\n🌐 جاري فتح المواقع باستخدام {browser_name}...")
    print("-" * 50)
    
    # قائمة المواقع للاختيار
    websites = {
        "1": ("https://www.google.com", "Google"),
        "2": ("https://www.github.com", "GitHub"),
        "3": ("https://www.youtube.com", "YouTube"),
        "4": ("https://www.example.com", "Example"),
        "5": ("https://import-dep.mega-sy.com/registration", "الموقع المستهدف"),
        "6": ("رابط مخصص", "فتح رابط مخصص")
    }
    
    print("\n📋 اختر موقعاً لفتحه:")
    for key, (url, name) in websites.items():
        print(f"  {key}. {name}")
    print("  *. العودة")
    
    site_choice = input("\n👉 أدخل رقم الموقع (أو * للعودة): ").strip()
    
    if site_choice == "*":
        return
    
    if site_choice == "6":
        custom_url = input("🔗 أدخل الرابط الكامل (مثال: https://www.example.com): ").strip()
        if custom_url:
            if not custom_url.startswith("http"):
                custom_url = "https://" + custom_url
            websites["6"] = (custom_url, "الرابط المخصص")
        else:
            print("❌ لم تدخل رابطاً")
            return
    
    if site_choice in websites:
        url, name = websites[site_choice]
        
        try:
            print(f"\n🔗 جاري فتح {name}...")
            driver.get(url)
            time.sleep(3)  # انتظار تحميل الصفحة
            
            # عرض معلومات الصفحة
            print(f"   📄 العنوان: {driver.title}")
            print(f"   🔗 الرابط: {driver.current_url}")
            print(f"   📏 حجم الصفحة: {len(driver.page_source):,} حرف")
            
            # التحقق من النماذج
            try:
                forms = driver.find_elements(By.TAG_NAME, "form")
                print(f"   📋 عدد النماذج: {len(forms)}")
                
                if forms:
                    # تحليل النموذج الأول
                    form = forms[0]
                    inputs = form.find_elements(By.TAG_NAME, "input")
                    selects = form.find_elements(By.TAG_NAME, "select")
                    textareas = form.find_elements(By.TAG_NAME, "textarea")
                    
                    print(f"   📝 تفاصيل النموذج:")
                    print(f"      • حقول الإدخال: {len(inputs)}")
                    print(f"      • قوائم الاختيار: {len(selects)}")
                    print(f"      • مناطق النص: {len(textareas)}")
                    
                    # عرض بعض الحقول
                    print(f"   🔍 بعض الحقول:")
                    for i, inp in enumerate(inputs[:3], 1):
                        name_attr = inp.get_attribute("name") or inp.get_attribute("id") or f"حقل_{i}"
                        type_attr = inp.get_attribute("type") or "text"
                        print(f"      {i}. {name_attr} ({type_attr})")
                    
            except:
                print("   ⚠️  لم يتمكن من تحليل النماذج")
            
            # خيارات إضافية
            print("\n   🎯 خيارات إضافية:")
            print("      s. حفظ لقطة شاشة")
            print("      h. حفظ HTML الصفحة")
            print("      r. إعادة تحميل الصفحة")
            print("      n. فتح نافذة جديدة")
            print("      اكتب أي شيء للعودة")
            
            option = input("   👉 اختر خياراً: ").strip().lower()
            
            if option == "s":
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                driver.save_screenshot(filename)
                print(f"   📸 تم حفظ لقطة شاشة: {filename}")
                time.sleep(1)
            
            elif option == "h":
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"page_{timestamp}.html"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                print(f"   💾 تم حفظ HTML: {filename}")
                time.sleep(1)
            
            elif option == "r":
                print("   🔄 جاري إعادة تحميل الصفحة...")
                driver.refresh()
                time.sleep(2)
                print(f"   ✅ تم التحديث: {driver.title}")
            
            elif option == "n":
                print("   🆕 فتح نافذة جديدة...")
                driver.execute_script("window.open('');")
                
                # التبديل إلى النافذة الجديدة
                driver.switch_to.window(driver.window_handles[-1])
                
                # فتح موقع في النافذة الجديدة
                new_url = input("   🔗 أدخل رابط للنافذة الجديدة (أو اترك فارغاً لـ Google): ").strip()
                if not new_url:
                    new_url = "https://www.google.com"
                
                driver.get(new_url)
                print(f"   🌐 تم فتح: {driver.title}")
                
                # العودة للتحكم
                input("   ⏸️  اضغط Enter للعودة...")
            
            # السؤال عن موقع آخر
            again_site = input("\n   🔁 هل تريد فتح موقع آخر؟ (نعم/لا): ").strip().lower()
            if again_site in ["نعم", "yes", "y"]:
                open_websites(driver, browser_name)
            
        except Exception as e:
            print(f"   ❌ فشل في فتح الموقع: {e}")
    else:
        print("❌ خيار غير صحيح")

def test_all_browsers():
    """اختبار جميع المتصفحات"""
    print("\n🧪 اختبار جميع المتصفحات...")
    print("="*50)
    
    browsers = [
        ("Chrome مرئي", lambda: setup_chrome(headless=False)),
        ("Chrome خفي", lambda: setup_chrome(headless=True)),
        ("Firefox مرئي", lambda: setup_firefox(headless=False)),
        ("Firefox خفي", lambda: setup_firefox(headless=True))
    ]
    
    for browser_name, setup_func in browsers:
        print(f"\n🔍 اختبار {browser_name}...")
        
        try:
            driver = setup_func()
            if driver:
                # فتح موقع اختبار
                driver.get("https://www.google.com")
                time.sleep(2)
                
                print(f"   ✅ {browser_name}: يعمل ({driver.title})")
                
                # إغلاق المتصفح
                driver.quit()
                print(f"   👋 {browser_name}: تم الإغلاق")
            else:
                print(f"   ❌ {browser_name}: فشل")
        except Exception as e:
            print(f"   ❌ {browser_name}: خطأ - {e}")
    
    print("\n✅ اكتمل اختبار جميع المتصفحات")

if __name__ == "__main__":
    main()
