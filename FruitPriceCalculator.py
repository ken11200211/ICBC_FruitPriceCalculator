class Fruit:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def calculate_price(self, weight, discount=1.0):
        return self.price * weight * discount

class ShoppingSystem:
    def __init__(self):
        self.fruits = {
            'apple': Fruit('蘋果', 8),
            'strawberry': Fruit('草莓', 13),
            'mango': Fruit('芒果', 20)
        }
    
    def calculate_price(self, apple_weight=0, strawberry_weight=0, mango_weight=0, 
                       strawberry_discount=1.0, discount_threshold=0, discount_amount=0):
        # 計算總價
        apple_price = self.fruits['apple'].calculate_price(apple_weight)
        strawberry_price = self.fruits['strawberry'].calculate_price(strawberry_weight, strawberry_discount)
        mango_price = self.fruits['mango'].calculate_price(mango_weight)
        
        total = apple_price + strawberry_price + mango_price
        
        # 應用滿減
        if discount_threshold > 0 and total >= discount_threshold:
            total -= discount_amount
        return total
    
    def calculate_customer_a(self, apple_weight, strawberry_weight):
        """顧客A：只買蘋果和草莓，無促銷"""
        return self.calculate_price(apple_weight, strawberry_weight)
    
    def calculate_customer_b(self, apple_weight, strawberry_weight, mango_weight):
        """顧客B：買三種水果，無促銷"""
        return self.calculate_price(apple_weight, strawberry_weight, mango_weight)
    
    def calculate_customer_c(self, apple_weight, strawberry_weight, mango_weight):
        """顧客C：買三種水果，草莓8折"""
        return self.calculate_price(apple_weight, strawberry_weight, mango_weight, strawberry_discount=0.8)
    
    def calculate_customer_d(self, apple_weight, strawberry_weight, mango_weight):
        """顧客D：買三種水果，草莓8折，滿100減10"""
        return self.calculate_price(apple_weight, strawberry_weight, mango_weight, 
                                   strawberry_discount=0.8, discount_threshold=100, discount_amount=10)
    
    def print_receipt(self, apple_weight, strawberry_weight, mango_weight, 
                     strawberry_discount=1.0, discount_threshold=0, discount_amount=0, customer_name=""):
        """打印購物小票"""
        print(f"\n{'='*30}")
        if customer_name:
            print(f"顧客{customer_name}的購物小票")
        else:
            print("購物小票")
        print('-'*30)
        
        # 計算各項價格
        apple_price = self.fruits['apple'].calculate_price(apple_weight)
        strawberry_price = self.fruits['strawberry'].calculate_price(strawberry_weight, strawberry_discount)
        mango_price = self.fruits['mango'].calculate_price(mango_weight)
        
        if apple_weight > 0:
            print(f"蘋果: {apple_weight}斤 × {self.fruits['apple'].price}元/斤 = {apple_price:.1f}元")
        if strawberry_weight > 0:
            discount_text = f" ({strawberry_discount:.1%}折)" if strawberry_discount != 1.0 else ""
            print(f"草莓: {strawberry_weight}斤 × {self.fruits['strawberry'].price}元/斤{discount_text} = {strawberry_price:.1f}元")
        if mango_weight > 0:
            print(f"芒果: {mango_weight}斤 × {self.fruits['mango'].price}元/斤 = {mango_price:.1f}元")
        subtotal = apple_price + strawberry_price + mango_price
        print('-'*30)
        total = subtotal
        if discount_threshold > 0 and subtotal >= discount_threshold:
            print(f"小計: {subtotal:.1f}元")
            print(f"滿減優惠: -{discount_amount}元 (滿{discount_threshold}減{discount_amount})")
            total -= discount_amount
        
        print(f"總計: {total:.1f}元")
        print('='*30)
        return total

def get_user_input(fruit_name, allow_zero=True):
    """獲取用戶輸入的水果斤數"""
    while True:
        try:
            weight_input = input(f"請輸入{fruit_name}的斤數（整數）: ").strip()
            weight = int(weight_input)
            
            # 檢查是否為負數
            if weight < 0:
                print("錯誤: 水果斤數不能為負數，請重新輸入")
                continue
                
            return weight
        except ValueError:
            print("錯誤: 請輸入整數，請重新輸入")

def validate_weights(apple_weight, strawberry_weight, mango_weight, customer_type):
    """驗證輸入的水果斤數"""
    # 檢查是否全為零
    if apple_weight == 0 and strawberry_weight == 0 and mango_weight == 0:
        print("錯誤: 所有水果斤數不能都為零，請至少購買一種水果")
        return False
    
    # 檢查顧客A是否購買了芒果
    if customer_type == 'A' and mango_weight > 0:
        print("錯誤: 顧客A方案不支持購買芒果")
        return False
    
    # 檢查是否為負數（在get_user_input中已經檢查，這裡再次確認）
    if apple_weight < 0 or strawberry_weight < 0 or mango_weight < 0:
        print("錯誤: 水果斤數不能為負數")
        return False
    
    return True

def interactive_mode():
    system = ShoppingSystem()
    while True:
        print("請選擇顧客類型:")
        print("A: 只買蘋果和草莓，無促銷")
        print("B: 買三種水果，無促銷")
        print("C: 買三種水果，草莓8折")
        print("D: 買三種水果，草莓8折，滿100減10")
        print("Q: 退出系統")
        choice = input("請輸入選擇 (A/B/C/D/Q): ").strip().upper()
        
        if choice == 'Q':
            print("\n感謝使用，再見！")
            break
            
        if choice not in ['A', 'B', 'C', 'D']:
            print("錯誤: 請輸入 A, B, C, D 或 Q")
            continue
        
        if choice == 'A':
            while True:
                apple_weight = get_user_input("蘋果")
                strawberry_weight = get_user_input("草莓")
                mango_weight = 0
                
                # 驗證輸入
                if validate_weights(apple_weight, strawberry_weight, mango_weight, choice):
                    break
                else:
                    print("請重新輸入...")
                    
            # 計算並顯示結果
            total = system.print_receipt(
                apple_weight, strawberry_weight, mango_weight, 
                customer_name=choice
            )
            
        else:  # B, C, D 顧客
            while True:
                apple_weight = get_user_input("蘋果")
                strawberry_weight = get_user_input("草莓")
                mango_weight = get_user_input("芒果")
                
                # 驗證輸入
                if validate_weights(apple_weight, strawberry_weight, mango_weight, choice):
                    break
                else:
                    print("請重新輸入...")
            
            # 根據顧客類型設置參數
            if choice in ['C', 'D']:
                strawberry_discount = 0.8
            else:
                strawberry_discount = 1.0

            discount_threshold = 100 if choice == 'D' else 0
            discount_amount = 10 if choice == 'D' else 0
            
            # 計算並顯示結果
            total = system.print_receipt(
                apple_weight, strawberry_weight, mango_weight,
                strawberry_discount=strawberry_discount,
                discount_threshold=discount_threshold,
                discount_amount=discount_amount,
                customer_name=choice
            )

if __name__ == "__main__":
    interactive_mode()