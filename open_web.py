#!/usr/bin/env python3
"""
اختبار Selenium - يفتح الموقع في تبويب جديد
"""

import os
import sys
import time

print("="*60)
print("🧪 اختبار Selenium - فتح في تبويب جديد")
print("="*60)

# إضافة مسار الإعدادات
config_path = os.path.expanduser("~/.selenium-config")
if os.path.exists(config_path):
    sys.path.append(config_path)
    print(f"✅ تم إضافة مسار الإعدادات: {config_path}")
else:
    print(f"⚠️  مسار الإعدادات غير موجود: {config_path}")

print("\n📦 جاري استيراد المكتبات...")
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    print("✅ تم استيراد مكتبة Selenium بنجاح")
    
    # محاولة استيراد الإعدادات المخصصة
    try:
        from chrome_options import setup_driver
        print("✅ تم استيراد إعدادات Chrome المخصصة")
    except ImportError:
        print("⚠️  لم يتم العثور على الإعدادات المخصصة، سيتم استخدام الإعدادات الافتراضية")
        
        def setup_driver():
            """إعداد افتراضي للسائق"""
            options = webdriver.ChromeOptions()
            # إزالة وضع headless للحصول على متصفح مرئي
            # options.add_argument("--headless")  # محذوف عمداً
            
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            # لجعل النافذة كبيرة
            options.add_argument("--start-maximized")
            
            # لجعل التجربة أفضل
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            return webdriver.Chrome(options=options)
            
except ImportError as e:
    print(f"❌ خطأ في استيراد المكتبات: {e}")
    print("💡 تأكد من تثبيت Selenium: pip install selenium")
    exit(1)

def open_in_new_tab(driver, url, name):
    """فتح الموقع في تبويب جديد"""
    try:
        print(f"\n{'='*40}")
        print(f"➕ جاري فتح {name} في تبويب جديد...")
        print(f"🔗 الرابط: {url}")
        
        # فتح تبويب جديد باستخدام JavaScript
        driver.execute_script("window.open('');")
        
        # التحول إلى التبويب الجديد
        driver.switch_to.window(driver.window_handles[-1])
        
        # فتح الموقع
        driver.get(url)
        time.sleep(3)  # انتظار تحميل الصفحة
        
        print(f"\n✅ تم فتح {name} في تبويب جديد!")
        print(f"📝 العنوان: {driver.title}")
        print(f"📍 الرابط الحالي: {driver.current_url}")
        print(f"📊 رقم التبويب: {len(driver.window_handles)}")
        
        # حفظ لقطة شاشة إذا كان الموقع المستهدف
        if "import-dep" in url:
            screenshot_path = f"target_site_tab_{len(driver.window_handles)}.png"
            driver.save_screenshot(screenshot_path)
            print(f"\n📸 تم حفظ لقطة شاشة: {screenshot_path}")
            
        return True
        
    except Exception as e:
        print(f"\n❌ فشل في فتح {name}: {e}")
        return False

def open_with_shortcut(driver, url, name):
    """فتح الموقع في تبويب جديد باستخدام اختصار لوحة المفاتيح"""
    try:
        print(f"\n{'='*40}")
        print(f"⌨️  جاري فتح {name} باستخدام Ctrl+T...")
        print(f"🔗 الرابط: {url}")
        
        # فتح تبويب جديد باستخدام Ctrl+T
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
        time.sleep(1)
        
        # فتح الموقع في التبويب الجديد
        driver.get(url)
        time.sleep(3)
        
        print(f"\n✅ تم فتح {name} باستخدام Ctrl+T!")
        print(f"📝 العنوان: {driver.title}")
        return True
        
    except Exception as e:
        print(f"\n❌ فشل في فتح باستخدام اختصار: {e}")
        return False

def switch_between_tabs(driver):
    """التبديل بين التبويبات وعرض معلوماتها"""
    tabs = driver.window_handles
    if len(tabs) <= 1:
        print("\n⚠️  هناك تبويب واحد فقط مفتوح")
        return
    
    print(f"\n📑 التبويبات المفتوحة ({len(tabs)}):")
    for i, tab in enumerate(tabs):
        driver.switch_to.window(tab)
        print(f"   {i+1}. {driver.title[:50]}...")
    
    # العودة للتبويب الأخير
    driver.switch_to.window(tabs[-1])

def main():
    """الدالة الرئيسية"""
    print("\n🔧 جاري تهيئة المتصفح...")
    
    try:
        driver = setup_driver()
        print("✅ تم تهيئة المتصفح بنجاح!")
        
        # فتح صفحة بداية
        driver.get("about:blank")
        print(f"\n🖥️  تم فتح المتصفح مع تبويب واحد.")
        print("💡 يمكنك الآن فتح مواقع في تبويبات جديدة.")
        
    except Exception as e:
        print(f"❌ فشل في تهيئة المتصفح: {e}")
        return
    
    # عرض التعليمات
    print("\n" + "="*60)
    print("📖 التعليمات:")
    print("="*60)
    print("1. ستفتح نافذة Chrome مع تبويب فارغ")
    print("2. اختر موقعاً لفتحه في تبويب جديد")
    print("3. يمكنك فتح عدة تبويبات في نفس الوقت")
    print("4. يمكنك التبديل بين التبويبات يدوياً")
    print("5. عند الانتهاء، اختر الخيار 0")
    print("="*60)
    
    # قائمة المواقع
    sites = [
        ("1️⃣", "https://www.google.com", "Google"),
        ("2️⃣", "https://github.com", "GitHub"),
        ("3️⃣", "https://www.python.org", "Python"),
        ("4️⃣", "https://import-dep.mega-sy.com/registration", "الموقع المستهدف"),
        ("5️⃣", "أدخل رابطاً يدوياً", "رابط مخصص"),
        ("6️⃣", "التبديل بين التبويبات", "عرض التبويبات"),
        ("7️⃣", "فتح باستخدام Ctrl+T", "اختصار لوحة المفاتيح"),
        ("0️⃣", "إنهاء البرنامج", "إغلاق")
    ]
    
    while True:
        print("\n" + "="*60)
        print("📋 قائمة الخيارات:")
        print("="*60)
        
        for num, url, name in sites:
            if url.startswith("أدخل"):
                print(f"{num} {name}")
            elif url.startswith("التبديل"):
                print(f"{num} {name}")
            elif url.startswith("فتح"):
                print(f"{num} {name}")
            elif url.startswith("إنهاء"):
                print(f"{num} {name}")
            else:
                print(f"{num} {name} - {url}")
        
        print("="*60)
        
        try:
            choice = input("\n🎯 اختر رقم الخيار (أو 0 للإغلاق): ").strip()
            
            if choice == "0":
                print("\n" + "="*60)
                print("👋 إنهاء البرنامج")
                print("="*60)
                
                print(f"\n📊 إحصائيات:")
                print(f"   - عدد التبويبات المفتوحة: {len(driver.window_handles)}")
                print(f"   - يمكنك إغلاق المتصفح يدوياً الآن")
                
                close_option = input("\n❓ هل تريد إغلاق جميع التبويبات تلقائياً؟ (ن/لا): ").strip().lower()
                
                if close_option in ['ن', 'yes', 'y', 'نعم']:
                    try:
                        driver.quit()
                        print("✅ تم إغلاق جميع التبويبات والمتصفح.")
                    except:
                        print("⚠️  تعذر إغلاق المتصفح تلقائياً.")
                else:
                    print("💡 تم ترك المتصفح مفتوحاً، يمكنك إغلاقه يدوياً.")
                
                print("\n✅ تم إنهاء البرنامج. وداعاً!")
                break
                
            elif choice == "1":
                open_in_new_tab(driver, "https://www.google.com", "Google")
                
            elif choice == "2":
                open_in_new_tab(driver, "https://github.com", "GitHub")
                
            elif choice == "3":
                open_in_new_tab(driver, "https://www.python.org", "Python")
                
            elif choice == "4":
                open_in_new_tab(driver, "https://import-dep.mega-sy.com/registration", "الموقع المستهدف")
                
            elif choice == "5":
                custom_url = input("\n🔗 أدخل الرابط الكامل (مع https://): ").strip()
                if custom_url:
                    site_name = custom_url.split('//')[-1].split('/')[0]
                    open_in_new_tab(driver, custom_url, f"المخصص ({site_name})")
                else:
                    print("❐ لم يتم إدخال رابط.")
                    
            elif choice == "6":
                switch_between_tabs(driver)
                
            elif choice == "7":
                # اختيار موقع لفتحه باستخدام Ctrl+T
                print("\n🎯 اختر موقعاً لفتحه باستخدام Ctrl+T:")
                print("   1. Google")
                print("   2. GitHub")
                print("   3. الموقع المستهدف")
                shortcut_choice = input("   أدخل رقم الموقع: ").strip()
                
                if shortcut_choice == "1":
                    open_with_shortcut(driver, "https://www.google.com", "Google")
                elif shortcut_choice == "2":
                    open_with_shortcut(driver, "https://github.com", "GitHub")
                elif shortcut_choice == "3":
                    open_with_shortcut(driver, "https://import-dep.mega-sy.com/registration", "الموقع المستهدف")
                else:
                    print("❌ اختيار غير صحيح.")
                    
            else:
                print("❌ اختيار غير صحيح، حاول مرة أخرى.")
            
            # عرض حالة التبويبات
            tabs_count = len(driver.window_handles)
            print(f"\n📌 الحالة الحالية: {tabs_count} تبويب{'ات' if tabs_count > 1 else ''} مفتوح{'ة' if tabs_count > 1 else ''}")
            
            # انتظار قصير
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  تم إيقاف البرنامج بواسطة المستخدم (Ctrl+C)")
            print(f"💡 لا يزال لديك {len(driver.window_handles)} تبويب مفتوح.")
            break
            
        except Exception as e:
            print(f"\n❌ حدث خطأ: {e}")
            continue
    
    # رسالة ختامية
    print("\n" + "="*60)
    print("🎯 انتهى تنفيذ البرنامج")
    print("="*60)
    print(f"📝 عدد التبويبات المتبقية: {len(driver.window_handles)}")
    print("💡 أغلق نافذة Chrome يدوياً عندما تنتهي.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ حدث خطأ غير متوقع: {e}")
