#!/usr/bin/env python3
"""
اختبار Selenium مع متصفح مفتوح
يتم فتح المتصفح ويبقى مفتوحاً حتى يتم إغلاقه يدوياً من قبل المستخدم
"""

import os
import sys
import time

print("="*60)
print("🧪 اختبار Selenium - المتصفح يبقى مفتوحاً")
print("="*60)

# إضافة مسار الإعدادات
config_path = os.path.expanduser("~/.selenium-config")
if os.path.exists(config_path):
    sys.path.append(config_path)
    print(f"✅ تم إضافة مسار الإعدادات: {config_path}")
else:
    print(f"⚠️  مسار الإعدادات غير موجود: {config_path}")
    print("💡 تأكد من تشغيل setup.sh أولاً")

print("\n📦 جاري استيراد المكتبات...")
try:
    from selenium import webdriver
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

def open_website(driver, url, name):
    """فتح موقع مع رسائل توضيحية"""
    try:
        print(f"\n{'='*40}")
        print(f"🌐 جاري فتح {name}...")
        print(f"🔗 الرابط: {url}")
        
        driver.get(url)
        time.sleep(3)  # انتظار تحميل الصفحة
        
        print(f"\n✅ تم فتح {name} بنجاح!")
        print(f"📝 العنوان: {driver.title}")
        print(f"📍 الرابط الحالي: {driver.current_url}")
        
        # عرض معلومات مفيدة
        print(f"\n💡 معلومات الصفحة:")
        print(f"   - حجم الصفحة: {len(driver.page_source):,} حرف")
        print(f"   - معرف النافذة: {driver.current_window_handle}")
        
        # حفظ لقطة شاشة إذا كان الموقع المستهدف
        if "import-dep" in url:
            screenshot_path = "target_site_open.png"
            driver.save_screenshot(screenshot_path)
            print(f"\n📸 تم حفظ لقطة شاشة: {screenshot_path}")
            
        return True
        
    except Exception as e:
        print(f"\n❌ فشل في فتح {name}: {e}")
        return False

def interactive_menu():
    """عرض قائمة تفاعلية للمواقع"""
    print("\n" + "="*60)
    print("📋 قائمة المواقع المتاحة للاختبار:")
    print("="*60)
    
    sites = [
        ("1️⃣", "https://www.google.com", "Google"),
        ("2️⃣", "https://github.com", "GitHub"),
        ("3️⃣", "https://www.python.org", "Python"),
        ("4️⃣", "https://www.example.com", "Example"),
        ("5️⃣", "https://import-dep.mega-sy.com/registration", "الموقع المستهدف"),
        ("6️⃣", "أدخل رابطاً يدوياً", "رابط مخصص"),
        ("0️⃣", "إغلاق المتصفح", "إنهاء الاختبار")
    ]
    
    for num, url, name in sites:
        if url.startswith("أدخل"):
            print(f"{num} {name}")
        elif url.startswith("إغلاق"):
            print(f"{num} {name}")
        else:
            print(f"{num} {name} - {url}")

def main():
    """الدالة الرئيسية"""
    print("\n🔧 جاري تهيئة المتصفح...")
    
    try:
        driver = setup_driver()
        print("✅ تم تهيئة المتصفح بنجاح!")
        print(f"\n🖥️  تم فتح نافذة المتصفح، يمكنك رؤيتها الآن.")
        print("💡 سيتم التحكم يدوياً من قبلك.")
        print("🔒 لن يتم إغلاق المتصفح تلقائياً.")
        
    except Exception as e:
        print(f"❌ فشل في تهيئة المتصفح: {e}")
        print("💡 تأكد من تثبيت Chrome وتنزيل ChromeDriver المناسب")
        return
    
    # عرض التعليمات
    print("\n" + "="*60)
    print("📖 التعليمات:")
    print("="*60)
    print("1. ستفتح نافذة Chrome جديدة")
    print("2. اختر موقعاً من القائمة لفتحه")
    print("3. يمكنك استخدام المتصفح يدوياً كما تشاء")
    print("4. عند الانتهاء، اختر الخيار 0 لإغلاق البرنامج")
    print("5. يمكنك أيضاً إغلاق نافذة المتصفح يدوياً")
    print("="*60)
    
    # انتظار قليل لرؤية المتصفح
    time.sleep(2)
    
    while True:
        interactive_menu()
        
        try:
            choice = input("\n🎯 اختر رقم الموقع (أو 0 للإغلاق): ").strip()
            
            if choice == "0":
                print("\n👋 جاري إنهاء البرنامج...")
                print("💡 يمكنك إغلاق نافذة المتصفح يدوياً الآن.")
                print("   أو انتظر 10 ثوانٍ ليتم الإغلاق تلقائياً.")
                
                # خيار للمستخدم
                auto_close = input("   هل تريد إغلاق المتصفح تلقائياً؟ (ن/لا): ").strip().lower()
                
                if auto_close in ['ن', 'yes', 'y']:
                    try:
                        driver.quit()
                        print("✅ تم إغلاق المتصفح تلقائياً.")
                    except:
                        print("⚠️  تعذر إغلاق المتصفح تلقائياً.")
                
                print("\n✅ تم إنهاء البرنامج. وداعاً!")
                break
                
            elif choice == "1":
                open_website(driver, "https://www.google.com", "Google")
                
            elif choice == "2":
                open_website(driver, "https://github.com", "GitHub")
                
            elif choice == "3":
                open_website(driver, "https://www.python.org", "Python")
                
            elif choice == "4":
                open_website(driver, "https://www.example.com", "Example")
                
            elif choice == "5":
                success = open_website(driver, "https://import-dep.mega-sy.com/registration", "الموقع المستهدف")
                if success:
                    print("\n🎯 هذا هو الموقع المستهدف!")
                    print("💡 يمكنك الآن اختباره يدوياً في المتصفح المفتوح.")
                    
            elif choice == "6":
                custom_url = input("\n🔗 أدخل الرابط الكامل (مع https://): ").strip()
                if custom_url:
                    site_name = custom_url.split('//')[-1].split('/')[0]
                    open_website(driver, custom_url, f"المخصص ({site_name})")
                else:
                    print("❐ لم يتم إدخال رابط.")
                    
            else:
                print("❌ اختيار غير صحيح، حاول مرة أخرى.")
                
            # إعطاء وقت للمستخدم لرؤية النتائج
            input("\n↵ اضغط Enter للعودة للقائمة...")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  تم إيقاف البرنامج بواسطة المستخدم (Ctrl+C)")
            print("💡 نافذة المتصفح لا تزال مفتوحة.")
            print("   يمكنك إغلاقها يدوياً عندما تنتهي.")
            break
            
        except Exception as e:
            print(f"\n❌ حدث خطأ: {e}")
            continue
    
    # إعطاء خيار أخير قبل الخروج
    try:
        if driver.service.is_connectable():
            print("\n" + "="*60)
            print("⚠️  نافذة المتصفح لا تزال مفتوحة!")
            print("="*60)
            print("يمكنك:")
            print("1. إغلاق النافذة يدوياً الآن")
            print("2. الاستمرار في استخدام المتصفح")
            print("3. الرجوع للبرنامج والاختيار 0 للإغلاق")
            print("="*60)
    except:
        pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ حدث خطأ غير متوقع: {e}")
        print("💡 قد يكون هناك مشكلة في اتصال ChromeDriver")
    finally:
        print("\n🎯 تم تنفيذ البرنامج.")
        print("📝 تذكر: نافذة Chrome قد لا تزال مفتوحة.")
        print("   أغلقها يدوياً عندما تنتهي من الاختبار.")
