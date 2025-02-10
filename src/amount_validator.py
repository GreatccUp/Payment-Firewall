"""
支付金额校验工具v0.1（适配中小系统）
功能：拦截常见金额处理漏洞 
"""
import re 
from decimal import Decimal, InvalidOperation 
 
class AmountValidator:
    @staticmethod 
    def validate(amount):
        """
        金额校验核心逻辑 
        返回：(is_valid, error_msg)
        """
        # 规则1：允许格式检查 
        if not re.match(r'^-?\d+(\.\d{1,2})?$', str(amount)):
            return False, "ERR_AMOUNT_FORMAT"
 
        # 规则2：精度转换验证 
        try:
            decimal_amount = Decimal(str(amount))
            if abs(decimal_amount.as_tuple().exponent) > 2:
                return False, "ERR_DECIMAL_PRECISION"
        except InvalidOperation:
            return False, "ERR_CONVERT_FAILED"
 
        # 规则3：边界值控制（适用于64位系统）
        max_amount = Decimal('92233720368547758.07')
        if abs(decimal_amount) > max_amount:
            return False, "ERR_AMOUNT_OVERFLOW"
 
        return True, "SUCCESS"
 
# 快速测试用例 
if __name__ == "__main__":
    tests = [
        "12.345",    # 错误：超过两位小数 
        "1e5",       # 错误：科学计数法 
        "99999999999999999.99",  # 溢出 
        "-500.00",   # 合法负数 
        "100.0",     # 合法 
    ]
    
    for amt in tests:
        valid, msg = AmountValidator.validate(amt)
        print(f"输入：{amt.ljust(15)} 结果：{'有效' if valid else '无效'} → {msg}")
