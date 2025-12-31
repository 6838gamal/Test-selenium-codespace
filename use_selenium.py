# إنشاء ملف use_selenium.py
cat > use_selenium.py << 'EOF'
#!/usr/bin/env python3
"""
استخدام Selenium للتحكم في النموذج
"""

import os
import sys
import time
from datetime import datetime

# إضافة مسار الإعدادات
sys.path.append(os.path.expanduser("~/.selenium-config"))

try:
    from chrome_options import setup_driver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    
    print("="*60)
    print("🚀 نظام التحكم في النموذج باستخدام Selenium")
    print("="*60)
    
    # 1. تهيئة المتصفح
    print("\n🔧 جاري تهيئة المتصفح...")
    driver = setup_driver()
    
    if not driver:
        print("❌ فشل في تهيئة المتصفح")
        exit(1)
    
    # 2. فتح الموقع المستهدف
    target_url = "https://import-dep.mega-sy.com/registration"
    print(f"\n🌐 جاري فتح الموقع: {target_url}")
    
    driver.get(target_url)
    time.sleep(3)  # انتظار تحميل الصفحة
    
    # 3. عرض معلومات الصفحة
    print(f"📄 العنوان: {driver.title}")
    print(f"🔗 الرابط: {driver.current_url}")
    print(f"📏 حجم الصفحة: {len(driver.page_source):,} حرف")
    
    # 4. التحليل والتسجيل
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # حفظ HTML
    with open(f"page_{timestamp}.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"💾 تم حفظ HTML في: page_{timestamp}.html")
    
    # التقاط لقطة شاشة
    driver.save_screenshot(f"screenshot_{timestamp}.png")
    print(f"📸 تم حفظ لقطة شاشة: screenshot_{timestamp}.png")
    
    # 5. تحليل النموذج
    print("\n🔍 جاري تحليل النموذج...")
    
    # البحث عن النماذج
    forms = driver.find_elements(By.TAG_NAME, "form")
    print(f"📋 عدد النماذج الموجودة: {len(forms)}")
    
    if forms:
        form = forms[0]  # النموذج الأول
        
        # البحث عن جميع الحقول
        all_inputs = form.find_elements(By.TAG_NAME, "input")
        all_selects = form.find_elements(By.TAG_NAME, "select")
        all_textareas = form.find_elements(By.TAG_NAME, "textarea")
        
        total_fields = len(all_inputs) + len(all_selects) + len(all_textareas)
        print(f"🔢 إجمالي الحقول: {total_fields}")
        
        # تصنيف الحقول
        print("\n📊 تصنيف الحقول:")
        print(f"  • حقول الإدخال (input): {len(all_inputs)}")
        print(f"  • قوائم الاختيار (select): {len(all_selects)}")
        print(f"  • مناطق النص (textarea): {len(all_textareas)}")
        
        # عرض الحقول المعطلة
        disabled_fields = []
        enabled_fields = []
        
        for element in all_inputs + all_selects + all_textareas:
            if not element.is_enabled():
                name = element.get_attribute("name") or element.get_attribute("id") or "بدون اسم"
                disabled_fields.append(name)
            else:
                name = element.get_attribute("name") or element.get_attribute("id") or "بدون اسم"
                enabled_fields.append(name)
        
        print(f"\n⚡ حالة الحقول:")
        print(f"  • الحقول المفعلة: {len(enabled_fields)}")
        print(f"  • الحقول المعطلة: {len(disabled_fields)}")
        
        if disabled_fields:
            print(f"\n📝 الحقول المعطلة ({len(disabled_fields)}):")
            for i, field in enumerate(disabled_fields[:10], 1):
                print(f"  {i}. {field}")
            if len(disabled_fields) > 10:
                print(f"  ... و{len(disabled_fields)-10} حقول أخرى")
        
        # 6. تفعيل الحقول المعطلة (اختياري)
        if disabled_fields:
            print("\n🔧 هل تريد محاولة تفعيل الحقول المعطلة؟")
            choice = input("(نعم/لا): ").strip().lower()
            
            if choice in ["نعم", "yes", "y"]:
                print("\n⚡ جاري تفعيل الحقول المعطلة...")
                
                activated_count = 0
                for element in all_inputs + all_selects + all_textareas:
                    if not element.is_enabled():
                        try:
                            # تفعيل الحقل باستخدام JavaScript
                            driver.execute_script("arguments[0].disabled = false;", element)
                            driver.execute_script("arguments[0].style.opacity = '1';", element)
                            activated_count += 1
                        except:
                            pass
                
                print(f"✅ تم تفعيل {activated_count} حقول")
                
                # التقاط لقطة بعد التفعيل
                driver.save_screenshot(f"activated_{timestamp}.png")
                print(f"📸 تم حفظ لقطة بعد التفعيل: activated_{timestamp}.png")
        
        # 7. عرض هيكل النموذج
        print("\n🏗️  هيكل النموذج:")
        
        # البحث عن الحقول المهمة
        important_fields = ["seller", "buyer", "plate", "phone", "email", "token", "_token"]
        
        for field_name in important_fields:
            elements = driver.find_elements(By.CSS_SELECTOR, f"[name*='{field_name}'], [id*='{field_name}']")
            for element in elements:
                name = element.get_attribute("name") or element.get_attribute("id")
                element_type = element.get_attribute("type") if element.tag_name == "input" else element.tag_name
                disabled = " (معطل)" if not element.is_enabled() else ""
                print(f"  • {name}: {element_type}{disabled}")
    
    else:
        print("❌ لم يتم العثور على أي نماذج في الصفحة")
    
    # 8. خيارات متقدمة
    print("\n" + "="*60)
    print("🎮 خيارات متقدمة:")
    print("="*60)
    print("1. اختبار ملء نموذج تجريبي")
    print("2. فحص جميع الروابط في الصفحة")
    print("3. حفظ ملف cookies")
    print("4. إنهاء الجلسة")
    
    choice = input("\n👉 اختر خياراً (1-4): ").strip()
    
    if choice == "1":
        test_fill_form(driver)
    elif choice == "2":
        check_links(driver)
    elif choice == "3":
        save_cookies(driver, timestamp)
    
    # 9. إغلاق المتصفح
    print("\n👋 جاري إغلاق المتصفح...")
    driver.quit()
    print("✅ تم إنهاء الجلسة بنجاح")
    
except ImportError as e:
    print(f"❌ خطأ في الاستيراد: {e}")
    print("💡 تأكد من تشغيل setup.sh أولاً")
except Exception as e:
    print(f"❌ خطأ غير متوقع: {e}")
    if 'driver' in locals():
        driver.quit()

def test_fill_form(driver):
    """اختبار ملء نموذج تجريبي"""
    print("\n📝 اختبار ملء نموذج تجريبي...")
    
    # بيانات تجريبية
    test_data = {
        "seller_name": "بائع تجريبي",
        "buyer_name": "مشتري تجريبي",
        "plate_number": "TEST123",
        "phone": "0912345678",
        "email": "test@example.com"
    }
    
    try:
        for field_name, value in test_data.items():
            # البحث عن الحقل بطرق مختلفة
            selectors = [
                f"[name*='{field_name}']",
                f"[id*='{field_name}']",
                f"[placeholder*='{field_name}']"
            ]
            
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            element.clear()
                            element.send_keys(value)
                            print(f"✅ تم ملء {field_name}: {value}")
                            break
                except:
                    continue
        
        print("\n✨ تم ملء البيانات التجريبية بنجاح")
        
        # البحث عن زر الإرسال ومحاولة النقر
        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "[id*='submit']",
            "[name*='submit']"
        ]
        
        for selector in submit_selectors:
            try:
                submit_button = driver.find_element(By.CSS_SELECTOR, selector)
                if submit_button.is_enabled():
                    print(f"\n🎯 وجدت زر الإرسال: {submit_button.get_attribute('id') or submit_button.get_attribute('name')}")
                    
                    # يمكنك تفعيل هذا إذا أردت تجربة الإرسال فعلياً
                    # submit_button.click()
                    # print("🖱️ تم النقر على زر الإرسال")
                    break
            except:
                continue
        
        # التقاط لقطة بعد الملء
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(f"filled_form_{timestamp}.png")
        print(f"📸 تم حفظ لقطة النموذج المملوء: filled_form_{timestamp}.png")
        
    except Exception as e:
        print(f"⚠️  خطأ في ملء النموذج: {e}")

def check_links(driver):
    """فحص جميع الروابط في الصفحة"""
    print("\n🔗 فحص الروابط في الصفحة...")
    
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"📎 عدد الروابط: {len(links)}")
        
        # عرض أول 10 روابط
        for i, link in enumerate(links[:10], 1):
            href = link.get_attribute("href")
            text = link.text.strip()[:50]
            if href:
                print(f"{i}. {text or 'بدون نص'} -> {href}")
        
        if len(links) > 10:
            print(f"... و{len(links)-10} روابط أخرى")
        
    except Exception as e:
        print(f"⚠️  خطأ في فحص الروابط: {e}")

def save_cookies(driver, timestamp):
    """حفظ cookies"""
    print("\n🍪 جاري حفظ cookies...")
    
    try:
        cookies = driver.get_cookies()
        
        if cookies:
            import json
            with open(f"cookies_{timestamp}.json", "w") as f:
                json.dump(cookies, f, indent=2)
            print(f"✅ تم حفظ {len(cookies)} cookie في: cookies_{timestamp}.json")
        else:
            print("⚠️  لا توجد cookies لحفظها")
            
    except Exception as e:
        print(f"⚠️  خطأ في حفظ cookies: {e}")
EOF

# جعله قابلاً للتنفيذ
chmod +x use_selenium.py

# تشغيله
echo "✅ تم إنشاء use_selenium.py"
echo "🚀 لتشغيله: python use_selenium.py"
