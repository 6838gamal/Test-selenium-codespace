# إنشاء ملف setup.sh
cat > setup.sh << 'EOF'
#!/bin/bash

# ==============================================
# 🔧 ملف تهيئة GitHub Codespace لـ Selenium
# ==============================================

echo "=============================================="
echo "🚀 بدء تهيئة بيئة Codespace لـ Selenium"
echo "=============================================="

# الألوان للرسائل
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# دالة لعرض رسائل النجاح
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# دالة لعرض رسائل التحذير
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# دالة لعرض رسائل الخطأ
error() {
    echo -e "${RED}❌ $1${NC}"
}

# دالة لعرض رسائل المعلومات
info() {
    echo -e "${BLUE}🔹 $1${NC}"
}

# ==============================================
# 1. تحديث النظام
# ==============================================
echo -e "\n📦 ${BLUE}1. تحديث النظام وحزم apt...${NC}"
sudo apt-get update
sudo apt-get upgrade -y
success "تم تحديث النظام"

# ==============================================
# 2. تثبيت المتصفحات
# ==============================================
echo -e "\n🌐 ${BLUE}2. تثبيت المتصفحات...${NC}"

# تثبيت Chromium (أخف وأسرع للبيئات الحاوية)
info "تثبيت Chromium..."
sudo apt-get install -y chromium-browser chromium-chromedriver

# التحقق من التثبيت
if command -v chromium-browser &> /dev/null; then
    CHROMIUM_VERSION=$(chromium-browser --version | head -n1)
    success "تم تثبيت Chromium: $CHROMIUM_VERSION"
else
    warning "Chromium لم يتم تثبته بشكل صحيح"
fi

# محاولة تثبيت Google Chrome (اختياري)
echo -e "\n${YELLOW}هل تريد تثبيت Google Chrome أيضاً؟ (نعم/لا)${NC}"
read -p "👉 أدخل الاختيار: " INSTALL_CHROME

if [[ "$INSTALL_CHROME" == "نعم" || "$INSTALL_CHROME" == "yes" || "$INSTALL_CHROME" == "y" ]]; then
    info "تثبيت Google Chrome..."
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
    sudo apt-get update
    sudo apt-get install -y google-chrome-stable
    
    if command -v google-chrome &> /dev/null; then
        CHROME_VERSION=$(google-chrome --version)
        success "تم تثبيت Google Chrome: $CHROME_VERSION"
    else
        warning "Google Chrome لم يتم تثبته بشكل صحيح"
    fi
else
    info "تخطي تثبيت Google Chrome"
fi

# ==============================================
# 3. تثبيت أدوات Python
# ==============================================
echo -e "\n🐍 ${BLUE}3. تثبيت أدوات Python...${NC}"

# قائمة الحزم المطلوبة
PYTHON_PACKAGES=(
    "selenium"
    "webdriver-manager"
    "chromedriver-autoinstaller"
    "requests"
    "beautifulsoup4"
    "lxml"
    "html5lib"
)

info "تثبيت حزم Python المطلوبة..."
for package in "${PYTHON_PACKAGES[@]}"; do
    info "جاري تثبيت $package..."
    pip install "$package" --quiet
    if pip show "$package" &> /dev/null; then
        VERSION=$(pip show "$package" | grep Version | cut -d' ' -f2)
        success "تم تثبيت $package ($VERSION)"
    else
        warning "فشل تثبيت $package"
    fi
done

# ==============================================
# 4. إعداد بيئة Selenium
# ==============================================
echo -e "\n🔧 ${BLUE}4. إعداد بيئة Selenium للعمل في Codespace...${NC}"

# إنشاء مجلد للإعدادات
SELENIUM_DIR="$HOME/.selenium-config"
mkdir -p "$SELENIUM_DIR"

# إنشاء ملف إعدادات Chrome للعمل في Codespace
cat > "$SELENIUM_DIR/chrome_options.py" << 'PYEOF'
"""
إعدادات Chrome مخصصة للعمل في GitHub Codespace
"""

def get_chrome_options(headless=True):
    """إرجاع إعدادات Chrome المناسبة لـ Codespace"""
    from selenium.webdriver.chrome.options import Options
    
    chrome_options = Options()
    
    # إعدادات أساسية لبيئة الحاوية
    if headless:
        chrome_options.add_argument("--headless=new")
    
    # إعدادات ضرورية لـ Docker/Codespace
    chrome_options.add_argument("--no-sandbox")  # ضروري للبيئات الحاوية
    chrome_options.add_argument("--disable-dev-shm-usage")  # مهم للذاكرة
    chrome_options.add_argument("--disable-gpu")  # تعطيل GPU في headless
    
    # إعدادات النافذة
    chrome_options.add_argument("--window-size=1920,1080")
    
    # تجنب مشاكل DevToolsActivePort
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--remote-debugging-address=0.0.0.0")
    
    # User-Agent واقعي
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # إعدادات لمكافحة الكشف
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # خيارات إضافية للاستقرار
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-software-rasterizer")
    
    return chrome_options


def setup_driver():
    """إعداد وتشغيل متصفح Chrome"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        import chromedriver_autoinstaller
        
        # تثبيت ChromeDriver تلقائياً
        chromedriver_path = chromedriver_autoinstaller.install()
        
        # الحصول على إعدادات Chrome
        chrome_options = get_chrome_options(headless=True)
        
        # إنشاء Service
        service = Service(chromedriver_path)
        
        # إنشاء Driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return driver
        
    except Exception as e:
        print(f"❌ خطأ في إعداد المتصفح: {e}")
        return None
PYEOF

success "تم إنشاء ملف إعدادات Selenium"

# ==============================================
# 5. إنشاء ملفات البرنامج
# ==============================================
echo -e "\n📁 ${BLUE}5. إنشاء ملفات البرنامج...${NC}"

# ملف Python الرئيسي
cat > selenium_app.py << 'PYEOF'
#!/usr/bin/env python3
"""
تطبيق Selenium للعمل في GitHub Codespace
"""

import os
import sys
import time
from datetime import datetime

# إضافة مجلد الإعدادات إلى المسار
sys.path.append(os.path.expanduser("~/.selenium-config"))

try:
    from chrome_options import setup_driver
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False
    print("⚠️  مكتبات Selenium غير مثبتة. قم بتشغيل setup.sh أولاً")

def test_selenium():
    """اختبار Selenium"""
    print("🧪 جاري اختبار Selenium...")
    
    if not HAS_SELENIUM:
        print("❌ Selenium غير متوفر")
        return False
    
    try:
        driver = setup_driver()
        if not driver:
            print("❌ فشل في تهيئة المتصفح")
            return False
        
        print("🌐 جاري فتح موقع اختبار...")
        driver.get("https://www.google.com")
        
        title = driver.title
        print(f"✅ تم فتح: {title}")
        print(f"📏 حجم الصفحة: {len(driver.page_source):,} حرف")
        
        # اختبار بسيط
        search_box = driver.find_element("name", "q")
        search_box.send_keys("GitHub Codespace")
        search_box.submit()
        
        time.sleep(2)
        print(f"🔍 نتائج البحث: {driver.title}")
        
        # التقاط لقطة شاشة
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_file = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_file)
        print(f"📸 تم حفظ لقطة الشاشة: {screenshot_file}")
        
        # إغلاق المتصفح
        driver.quit()
        print("👋 تم إغلاق المتصفح")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار Selenium: {e}")
        return False

def test_requests():
    """اختبار الاتصال باستخدام requests"""
    print("\n🔗 اختبار الاتصال باستخدام requests...")
    
    try:
        import requests
        from bs4 import BeautifulSoup
        
        response = requests.get("https://httpbin.org/get", timeout=10)
        
        if response.status_code == 200:
            print(f"✅ الاتصال ناجح (كود: {response.status_code})")
            return True
        else:
            print(f"⚠️  كود استجابة غير متوقع: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ فشل اختبار requests: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("="*60)
    print("🚀 تطبيق Selenium للعمل في Codespace")
    print("="*60)
    
    # عرض معلومات النظام
    print(f"\n💻 معلومات النظام:")
    print(f"  • المسار: {os.getcwd()}")
    print(f"  • Python: {sys.version}")
    print(f"  • Selenium: {'✅ متوفر' if HAS_SELENIUM else '❌ غير متوفر'}")
    
    # اختبارات
    print("\n" + "="*60)
    print("🧪 جاري تشغيل الاختبارات...")
    print("="*60)
    
    tests_passed = 0
    tests_total = 2
    
    # اختبار 1: Selenium
    if test_selenium():
        tests_passed += 1
    
    # اختبار 2: Requests
    if test_requests():
        tests_passed += 1
    
    # النتيجة
    print("\n" + "="*60)
    print("📊 نتائج الاختبارات:")
    print("="*60)
    print(f"  • اجتاز {tests_passed} من أصل {tests_total} اختبار")
    
    if tests_passed == tests_total:
        print("🎉 جميع الاختبارات نجحت! البيئة جاهزة للاستخدام.")
    elif tests_passed >= 1:
        print("⚠️  بعض الاختبارات فشلت، لكن البيئة شبه جاهزة.")
    else:
        print("❌ فشلت جميع الاختبارات. يرجى التحقق من الإعدادات.")
    
    # إنشاء مثال بسيط
    print("\n" + "="*60)
    print("📝 مثال للاستخدام:")
    print("="*60)
    
    example_code = '''import sys
sys.path.append(os.path.expanduser("~/.selenium-config"))

from chrome_options import setup_driver

# استخدام المتصفح
driver = setup_driver()
driver.get("https://www.example.com")
print(f"الصفحة: {driver.title}")
driver.quit()'''
    
    print(example_code)

if __name__ == "__main__":
    main()
PYEOF

chmod +x selenium_app.py
success "تم إنشاء selenium_app.py"

# ملف تهيئة المشروع
cat > requirements.txt << 'TXTEOF'
# متطلبات مشروع Selenium للعمل في Codespace
selenium>=4.15.0
webdriver-manager>=4.0.1
chromedriver-autoinstaller>=0.6.0
requests>=2.31.0
beautifulsoup4>=4.12.2
lxml>=4.9.3
html5lib>=1.1
TXTEOF

success "تم إنشاء requirements.txt"

# ملف إعدادات Codespace
cat > .devcontainer/devcontainer.json << 'JSONEOF'
{
    "name": "Python Selenium Environment",
    "image": "mcr.microsoft.com/devcontainers/python:1-3.12-bullseye",
    
    "features": {
        "ghcr.io/devcontainers/features/chrome:1": {
            "version": "stable"
        },
        "ghcr.io/devcontainers/features/python:1": {
            "installTools": true,
            "version": "3.12"
        }
    },
    
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python",
                "ms-python.vscode-pylance",
                "ms-toolsai.jupyter",
                "formulahendry.code-runner"
            ],
            "settings": {
                "python.defaultInterpreterPath": "/usr/local/bin/python",
                "python.linting.enabled": true,
                "python.linting.pylintEnabled": true,
                "python.formatting.autopep8Path": "/usr/local/py-utils/bin/autopep8",
                "python.formatting.blackPath": "/usr/local/py-utils/bin/black",
                "python.formatting.yapfPath": "/usr/local/py-utils/bin/yapf",
                "python.linting.banditPath": "/usr/local/py-utils/bin/bandit",
                "python.linting.flake8Path": "/usr/local/py-utils/bin/flake8",
                "python.linting.mypyPath": "/usr/local/py-utils/bin/mypy",
                "python.linting.pycodestylePath": "/usr/local/py-utils/bin/pycodestyle",
                "python.linting.pydocstylePath": "/usr/local/py-utils/bin/pydocstyle",
                "python.linting.pylintPath": "/usr/local/py-utils/bin/pylint"
            }
        }
    },
    
    "postCreateCommand": "pip install -r requirements.txt && chmod +x setup.sh && ./setup.sh",
    
    "forwardPorts": [9222],
    
    "remoteUser": "codespace"
}
JSONEOF

mkdir -p .devcontainer
success "تم إنشاء إعدادات devcontainer"

# ==============================================
# 6. اختبار التثبيت
# ==============================================
echo -e "\n🧪 ${BLUE}6. اختبار التثبيت...${NC}"

# اختبار Python
info "اختبار Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    success "Python: $PYTHON_VERSION"
else
    error "Python غير مثبت"
fi

# اختبار pip
info "اختبار pip..."
if command -v pip &> /dev/null; then
    PIP_VERSION=$(pip --version | cut -d' ' -f2)
    success "pip: $PIP_VERSION"
else
    warning "pip غير مثبت، جاري التثبيت..."
    sudo apt-get install -y python3-pip
fi

# اختبار المتصفح
info "اختبار Chromium..."
if command -v chromium-browser &> /dev/null; then
    success "Chromium مثبت"
else
    error "Chromium غير مثبت"
fi

# اختبار ChromeDriver
info "اختبار ChromeDriver..."
if command -v chromedriver &> /dev/null; then
    CHROMEDRIVER_VERSION=$(chromedriver --version | head -n1)
    success "ChromeDriver: $CHROMEDRIVER_VERSION"
else
    warning "ChromeDriver غير مثبت"
fi

# ==============================================
# 7. إنشاء أمثلة استخدام
# ==============================================
echo -e "\n📚 ${BLUE}7. إنشاء أمثلة استخدام...${NC}"

# مثال 1: فتح موقع
cat > example_simple.py << 'PYEOF'
#!/usr/bin/env python3
"""
مثال بسيط لاستخدام Selenium في Codespace
"""

import sys
import os

# إضافة مسار الإعدادات
sys.path.append(os.path.expanduser("~/.selenium-config"))

try:
    from chrome_options import setup_driver
    
    print("🚀 بدء تشغيل المتصفح...")
    
    # تهيئة المتصفح
    driver = setup_driver()
    
    if driver:
        # فتح موقع
        driver.get("https://www.github.com")
        print(f"🌐 تم فتح: {driver.title}")
        print(f"📏 الرابط: {driver.current_url}")
        
        # انتظار قليلاً
        import time
        time.sleep(2)
        
        # التقاط لقطة شاشة
        driver.save_screenshot("github_homepage.png")
        print("📸 تم حفظ لقطة شاشة: github_homepage.png")
        
        # إغلاق المتصفح
        driver.quit()
        print("👋 تم إنهاء الجلسة")
    else:
        print("❌ فشل في تهيئة المتصفح")
        
except ImportError as e:
    print(f"❌ خطأ في الاستيراد: {e}")
    print("💡 تأكد من تشغيل setup.sh أولاً")
except Exception as e:
    print(f"❌ خطأ غير متوقع: {e}")
PYEOF

chmod +x example_simple.py
success "تم إنشاء example_simple.py"

# مثال 2: ملء نموذج
cat > example_form.py << 'PYEOF'
#!/usr/bin/env python3
"""
مثال لملء نموذج باستخدام Selenium
"""

import sys
import os
import time

# إضافة مسار الإعدادات
sys.path.append(os.path.expanduser("~/.selenium-config"))

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from chrome_options import get_chrome_options
    
    print("📝 مثال لملء نموذج...")
    
    # الحصول على إعدادات Chrome
    chrome_options = get_chrome_options(headless=False)  # يمكن تغييرها لـ True
    
    # إنشاء driver
    driver = webdriver.Chrome(options=chrome_options)
    
    # فتح موقع اختبار للنماذج
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")
    print(f"🌐 تم فتح: {driver.title}")
    
    # ملء الحقول
    print("🖊️  جاري ملء الحقول...")
    
    # حقل النص
    text_input = driver.find_element(By.NAME, "my-text")
    text_input.send_keys("هذا نص اختبار من Codespace")
    print("✅ تم ملء حقل النص")
    
    # كلمة المرور
    password_input = driver.find_element(By.NAME, "my-password")
    password_input.send_keys("test123")
    print("✅ تم ملء حقل كلمة المرور")
    
    # textarea
    textarea = driver.find_element(By.NAME, "my-textarea")
    textarea.send_keys("هذا نص طويل للاختبار\\nسطر ثاني\\nسطر ثالث")
    print("✅ تم ملء Textarea")
    
    # تحديد من القائمة
    dropdown = driver.find_element(By.NAME, "my-select")
    dropdown.click()
    time.sleep(0.5)
    option = driver.find_element(By.CSS_SELECTOR, "option[value='2']")
    option.click()
    print("✅ تم اختيار من القائمة")
    
    # اختيار من dropdown
    from selenium.webdriver.support.ui import Select
    dropdown2 = Select(driver.find_element(By.NAME, "my-datalist"))
    dropdown2.select_by_visible_text("New York")
    print("✅ تم اختيار من dropdown")
    
    # اختيار ملف
    file_input = driver.find_element(By.NAME, "my-file")
    file_input.send_keys(os.path.abspath(__file__))
    print("✅ تم اختيار ملف")
    
    # color picker
    color_input = driver.find_element(By.NAME, "my-colors")
    color_input.send_keys("#FF5733")
    print("✅ تم اختيار لون")
    
    # تاريخ
    date_input = driver.find_element(By.NAME, "my-date")
    date_input.send_keys("01/01/2024")
    print("✅ تم اختيار تاريخ")
    
    # range
    range_input = driver.find_element(By.NAME, "my-range")
    driver.execute_script("arguments[0].value = '5';", range_input)
    print("✅ تم ضبط المدى")
    
    # انتظار لرؤية النتيجة
    time.sleep(2)
    
    # التقاط لقطة شاشة
    driver.save_screenshot("form_filled.png")
    print("📸 تم حفظ لقطة شاشة: form_filled.png")
    
    # يمكنك إضافة إرسال النموذج هنا
    # submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    # submit_button.click()
    
    print("✨ المثال اكتمل بنجاح!")
    
    # إبقاء المتصفح مفتوحاً لمشاهدة النتيجة
    print("\\n⏳ المتصفح سيبقى مفتوحاً لمدة 10 ثواني...")
    time.sleep(10)
    
    # إغلاق المتصفح
    driver.quit()
    print("👋 تم إغلاق المتصفح")
    
except ImportError as e:
    print(f"❌ خطأ في الاستيراد: {e}")
except Exception as e:
    print(f"❌ خطأ غير متوقع: {e}")
    if 'driver' in locals():
        driver.quit()
PYEOF

chmod +x example_form.py
success "تم إنشاء example_form.py"

# ==============================================
# 8. تخصيص البيئة
# ==============================================
echo -e "\n⚙️  ${BLUE}8. تخصيص بيئة العمل...${NC}"

# إنشاء ملف .bashrc مخصص
BASHRC_ADDITIONS='
# ==============================================
# إعدادات Selenium لـ Codespace
# ==============================================

export SELENIUM_HOME="$HOME/.selenium-config"
export PATH="$SELENIUM_HOME:$PATH"

# ألوان للمحطة
alias ls="ls --color=auto"
alias grep="grep --color=auto"

# أوامر مساعدة
alias selenium-test="python3 selenium_app.py"
alias selenium-example="python3 example_simple.py"
alias selenium-form="python3 example_form.py"

# معلومات النظام
sysinfo() {
    echo "=============================================="
    echo "💻 معلومات نظام Codespace"
    echo "=============================================="
    echo "• التاريخ: $(date)"
    echo "• المسار: $(pwd)"
    echo "• Python: $(python3 --version 2>/dev/null || echo غير مثبت)"
    echo "• Chromium: $(chromium-browser --version 2>/dev/null | head -n1 || echo غير مثبت)"
    echo "• ChromeDriver: $(chromedriver --version 2>/dev/null | head -n1 || echo غير مثبت)"
    echo "=============================================="
}

# اختبار سريع
test-env() {
    echo "🔍 جاري اختبار البيئة..."
    python3 -c "import selenium; print(f\"✅ Selenium: {selenium.__version__}\")" 2>/dev/null || echo "❌ Selenium غير مثبت"
    python3 -c "import requests; print(f\"✅ Requests: {requests.__version__}\")" 2>/dev/null || echo "❌ Requests غير مثبت"
    which chromedriver >/dev/null && echo "✅ ChromeDriver: مثبت" || echo "❌ ChromeDriver: غير مثبت"
}

# عرض هذه الرسالة عند الدخول
echo "✨ بيئة Selenium جاهزة في Codespace!"
echo "💡 الأوامر المتاحة: selenium-test, selenium-example, selenium-form, sysinfo, test-env"
echo "🔗 لمزيد من المعلومات: https://github.com/SeleniumHQ/selenium"
'

# إضافة إلى .bashrc
echo "$BASHRC_ADDITIONS" >> ~/.bashrc
success "تم تخصيص .bashrc"

# ==============================================
# 9. التنظيف النهائي
# ==============================================
echo -e "\n🧹 ${BLUE}9. تنظيف الملفات المؤقتة...${NC}"
sudo apt-get autoremove -y
sudo apt-get clean

# ==============================================
# 10. رسالة النجاح
# ==============================================
echo -e "\n${GREEN}==============================================${NC}"
echo -e "${GREEN}🎉 اكتملت التهيئة بنجاح!${NC}"
echo -e "${GREEN}==============================================${NC}"
echo -e "\n${YELLOW}📋 الخطوات التالية:${NC}"
echo -e "1. ${BLUE}أعد تشغيل المحطة${NC} لتفعيل الإعدادات:"
echo -e "   ${GREEN}exec bash${NC}"
echo -e "2. ${BLUE}اختر البيئة${NC} باستخدام:"
echo -e "   ${GREEN}python3 selenium_app.py${NC}"
echo -e "3. ${BLUE}جرب الأمثلة${NC}:"
echo -e "   ${GREEN}./example_simple.py${NC}"
echo -e "   ${GREEN}./example_form.py${NC}"
echo -e "\n${YELLOW}💡 أوامر مفيدة:${NC}"
echo -e "   • ${GREEN}sysinfo${NC} - عرض معلومات النظام"
echo -e "   • ${GREEN}test-env${NC} - اختبار البيئة"
echo -e "   • ${GREEN}selenium-test${NC} - اختبار Selenium"
echo -e "\n${YELLOW}🔗 روابط مفيدة:${NC}"
echo -e "   • ${BLUE}https://selenium-python.readthedocs.io/${NC}"
echo -e "   • ${BLUE}https://github.com/SeleniumHQ/selenium${NC}"
echo -e "   • ${BLUE}https://docs.github.com/codespaces${NC}"

# جعل الملف قابلاً للتنفيذ
chmod +x setup.sh

echo -e "\n${GREEN}✅ تم إنشاء setup.sh بنجاح!${NC}"
echo -e "${YELLOW}👉 لتشغيله: ./setup.sh${NC}"
EOF

# جعل الملف قابلاً للتنفيذ
chmod +x setup.sh

# عرض معلومات الملف
echo "✅ تم إنشاء setup.sh"
echo "📏 حجم الملف: $(wc -l setup.sh | cut -d' ' -f1) سطر"
echo "🔧 الصلاحيات: $(ls -la setup.sh | cut -d' ' -f1)"
echo ""
echo "🚀 لتشغيل ملف التهيئة:"
echo "./setup.sh"
