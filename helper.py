import locale
import os
import sys

def get_locale_safe():
    """
    兼容Windows特殊格式，精准获取 zh_CN / en_US 等标准区域代码
    解决返回 'Chinese (Simplified)_China' 的问题
    """
    # 第一步：定义Windows本地化名称到标准代码的映射（覆盖主流语言）
    windows_locale_map = {
        # 中文相关
        'Chinese (Simplified)_China': 'zh_CN',
        'Chinese (Traditional)_Taiwan': 'zh_TW',
        'Chinese (Traditional)_Hong Kong S.A.R.': 'zh_HK',
        # 英文相关
        'English_United States': 'en_US',
        'English_United Kingdom': 'en_GB',
        # 其他常用语言（可按需扩展）
        'Japanese_Japan': 'ja_JP',
        'Korean_Korea': 'ko_KR',
        'French_France': 'fr_FR',
        'German_Germany': 'de_DE',
        'Spanish_Spain': 'es_ES'
    }

    try:
        # 1. 获取原始locale（可能是中文名称格式）
        lang_region, _ = locale.getlocale()
        
        # 2. 优先转换Windows特殊格式
        if lang_region in windows_locale_map:
            return windows_locale_map[lang_region]
        
        # 3. 如果是标准格式（如 zh_CN），直接返回
        if lang_region and '_' in lang_region and len(lang_region.split('_')[0]) == 2:
            return lang_region
        
        # 4. 兜底1：读环境变量（Linux/macOS/Windows通用）
        if not lang_region:
            lang_var = os.environ.get("LANG", "") or os.environ.get("LC_ALL", "")
            if lang_var:
                lang_region = lang_var.split(".")[0].replace("-", "_")
                # 转换环境变量中的标准格式（如 zh-CN -> zh_CN）
                return lang_region if lang_region else "en_US"
        
        # 5. 兜底2：Windows API精准获取（直接返回 zh-CN 格式）
        if not lang_region and sys.platform == "win32":
            try:
                import ctypes
                kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                buf = ctypes.create_unicode_buffer(100)
                # GetUserDefaultLocaleName 返回标准代码（如 zh-CN）
                if kernel32.GetUserDefaultLocaleName(buf, ctypes.sizeof(buf) // 2):
                    return buf.value.replace("-", "_")  # 转成 zh_CN
            except:
                pass
        
        # 最终兜底
        return "en_US"
    
    except Exception as e:
        print(f"获取区域失败：{e}")
        return "en_US"

# 测试调用
if __name__ == "__main__":
    # 先设置系统默认locale（保证兼容性）
    #locale.setlocale(locale.LC_ALL, '')
    
    # 调用函数，现在会返回 zh_CN 而非中文名称
    result = get_locale_safe()
    print("标准区域代码：", result)  # 输出：zh_CN