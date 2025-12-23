import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class Fruit:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def calculate_price(self, weight, discount=1.0):
        """計算該水果的總價"""
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
        """
        通用計算方法
        參數:
            apple_weight: 蘋果斤數
            strawberry_weight: 草莓斤數
            mango_weight: 芒果斤數
            strawberry_discount: 草莓折扣，默認為1.0（無折扣）
            discount_threshold: 滿減門檻，默認為0（無滿減）
            discount_amount: 滿減金額，默認為0（無滿減）
        """
        # 計算總價
        apple_price = self.fruits['apple'].calculate_price(apple_weight)
        strawberry_price = self.fruits['strawberry'].calculate_price(strawberry_weight, strawberry_discount)
        mango_price = self.fruits['mango'].calculate_price(mango_weight)
        
        total = apple_price + strawberry_price + mango_price
        
        # 應用滿減
        if discount_threshold > 0 and total >= discount_threshold:
            total -= discount_amount
        return total
    
    def get_detailed_calculation(self, apple_weight, strawberry_weight, mango_weight, 
                                strawberry_discount=1.0, discount_threshold=0, discount_amount=0):
        """獲取詳細的計算明細"""
        # 計算各項價格
        apple_price = self.fruits['apple'].calculate_price(apple_weight)
        strawberry_price = self.fruits['strawberry'].calculate_price(strawberry_weight, strawberry_discount)
        mango_price = self.fruits['mango'].calculate_price(mango_weight)
        
        subtotal = apple_price + strawberry_price + mango_price
        discount_applied = False
        discount_info = ""
        final_total = subtotal
        
        # 應用滿減
        if discount_threshold > 0 and subtotal >= discount_threshold:
            discount_applied = True
            discount_info = f"滿{discount_threshold}減{discount_amount}"
            final_total -= discount_amount
        
        return {
            'apple_price': apple_price,
            'strawberry_price': strawberry_price,
            'mango_price': mango_price,
            'subtotal': subtotal,
            'discount_applied': discount_applied,
            'discount_amount': discount_amount if discount_applied else 0,
            'discount_info': discount_info,
            'final_total': final_total,
            'strawberry_discount': strawberry_discount,
            'strawberry_original': strawberry_weight * 13.0
        }

class FruitPriceCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("水果價格試算系統 - 全功能版")
        
        # 設定全螢幕
        self.root.attributes('-fullscreen', True)
        
        # 綁定退出全螢幕快捷鍵
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        
        # 設定應用程式主題顏色
        self.root.configure(bg='#f5f7fa')
        
        # 創建水果價格試算系統實例
        self.shopping_system = ShoppingSystem()
        
        # 顧客方案資料
        self.customer_options = {
            "顧客A - 蘋果草莓，無促銷": {
                "code": "A",
                "description": "只買蘋果和草莓，無促銷",
                "has_mango": False,
                "strawberry_discount": 1.0,
                "discount_threshold": 0,
                "discount_amount": 0
            },
            "顧客B - 三種水果，無促銷": {
                "code": "B",
                "description": "買三種水果，無促銷",
                "has_mango": True,
                "strawberry_discount": 1.0,
                "discount_threshold": 0,
                "discount_amount": 0
            },
            "顧客C - 三種水果，草莓8折": {
                "code": "C",
                "description": "買三種水果，草莓8折",
                "has_mango": True,
                "strawberry_discount": 0.8,
                "discount_threshold": 0,
                "discount_amount": 0
            },
            "顧客D - 草莓8折，滿100減10": {
                "code": "D",
                "description": "草莓8折，滿100減10",
                "has_mango": True,
                "strawberry_discount": 0.8,
                "discount_threshold": 100,
                "discount_amount": 10
            }
        }
        
        # 水果重量變數
        self.apple_weight = tk.IntVar(value=0)
        self.strawberry_weight = tk.IntVar(value=0)
        self.mango_weight = tk.IntVar(value=0)
        
        # 顧客類型變數
        self.selected_customer = tk.StringVar(value=list(self.customer_options.keys())[0])
        
        # 芒果輸入框框架引用
        self.mango_frame = None
        
        # 建立應用程式框架
        self.create_main_layout()
        
        # 初始更新芒果輸入框狀態
        self.on_customer_changed()
    
    def create_main_layout(self):
        """建立主佈局"""
        # 主容器框架
        main_container = tk.Frame(self.root, bg='#f5f7fa')
        main_container.pack(expand=True, fill=tk.BOTH, padx=15, pady=10)
        
        # 頂部標題欄
        self.create_header(main_container)
        
        # 主內容區域（使用grid佈局）
        content_frame = tk.Frame(main_container, bg='#f5f7fa')
        content_frame.pack(expand=True, fill=tk.BOTH, pady=(10, 5))
        
        # 配置grid佈局權重
        content_frame.grid_columnconfigure(0, weight=1)  # 左側面板
        content_frame.grid_columnconfigure(1, weight=0)  # 分隔線
        content_frame.grid_columnconfigure(2, weight=1)  # 右側面板
        content_frame.grid_rowconfigure(0, weight=1)
        
        # 左側面板：顧客選擇和輸入（調整寬度）
        left_panel = self.create_left_panel(content_frame)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # 分隔線
        separator = tk.Frame(content_frame, bg='#e0e5ec', width=2)
        separator.grid(row=0, column=1, sticky="ns")
        
        # 右側面板：結果顯示
        right_panel = self.create_right_panel(content_frame)
        right_panel.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        
        # 底部按鈕欄
        self.create_footer(main_container)
    
    def create_header(self, parent):
        """建立頂部標題欄"""
        header_frame = tk.Frame(parent, bg='#2c3e50', height=70)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # 標題文字
        title_label = tk.Label(
            header_frame,
            text=" 水果價格試算系統 ",
            font=('Microsoft JhengHei', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(side=tk.LEFT, padx=25)
        
        # 全螢幕切換按鈕
        fullscreen_btn = tk.Button(
            header_frame,
            text="⛶",
            font=('Arial', 12),
            bg='#34495e',
            fg='white',
            command=self.toggle_fullscreen,
            relief=tk.FLAT,
            width=2,
            height=1,
            cursor="hand2"
        )
        fullscreen_btn.pack(side=tk.RIGHT, padx=15)
        
        # 退出按鈕
        exit_btn = tk.Button(
            header_frame,
            text="✕",
            font=('Arial', 12),
            bg='#e74c3c',
            fg='white',
            command=self.root.quit,
            relief=tk.FLAT,
            width=2,
            height=1,
            cursor="hand2"
        )
        exit_btn.pack(side=tk.RIGHT, padx=5)
    
    def create_left_panel(self, parent):
        """建立左側面板：顧客選擇和輸入"""
        left_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        left_frame.pack_propagate(False)
        
        # 顧客選擇區域
        customer_frame = tk.Frame(left_frame, bg='white')
        customer_frame.pack(fill=tk.X, padx=20, pady=(20, 15))
        
        tk.Label(
            customer_frame,
            text="選擇顧客方案：",
            font=('Microsoft JhengHei', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 8))
        
        # 下拉選擇框
        customer_combo = ttk.Combobox(
            customer_frame,
            textvariable=self.selected_customer,
            values=list(self.customer_options.keys()),
            font=('Microsoft JhengHei', 10),
            state='readonly',
            width=30
        )
        customer_combo.pack(fill=tk.X, pady=(0, 10))
        customer_combo.bind('<<ComboboxSelected>>', self.on_customer_changed)
        
        # 方案描述
        self.customer_desc_label = tk.Label(
            customer_frame,
            text=self.customer_options[list(self.customer_options.keys())[0]]["description"],
            font=('Microsoft JhengHei', 9),
            bg='white',
            fg='#7f8c8d',
            wraplength=350,
            justify=tk.LEFT
        )
        self.customer_desc_label.pack(anchor='w', pady=(0, 5))
        
        # 分隔線
        tk.Frame(left_frame, bg='#ecf0f1', height=2).pack(fill=tk.X, padx=20, pady=10)
        
        # 水果輸入區域
        input_frame = tk.Frame(left_frame, bg='white')
        input_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        tk.Label(
            input_frame,
            text="輸入購買斤數：",
            font=('Microsoft JhengHei', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 15))
        
        # 水果輸入表單
        self.fruit_entries = {}
        
        # 蘋果輸入框
        apple_frame = self.create_fruit_input(
            input_frame, " 蘋果", "8元/斤", self.apple_weight, "#e74c3c"
        )
        apple_frame.pack(fill=tk.X, pady=8)
        
        # 草莓輸入框
        strawberry_frame = self.create_fruit_input(
            input_frame, " 草莓", "13元/斤", self.strawberry_weight, "#e91e63"
        )
        strawberry_frame.pack(fill=tk.X, pady=8)
        
        # 芒果輸入框（保留引用）
        self.mango_frame = self.create_fruit_input(
            input_frame, " 芒果", "20元/斤", self.mango_weight, "#f39c12"
        )
        self.mango_frame.pack(fill=tk.X, pady=8)
        
        return left_frame
    
    def create_fruit_input(self, parent, fruit_name, price_info, weight_var, color):
        """創建水果輸入框"""
        fruit_frame = tk.Frame(parent, bg='white')
        
        # 水果名稱和價格
        name_frame = tk.Frame(fruit_frame, bg='white')
        name_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(
            name_frame,
            text=fruit_name,
            font=('Microsoft JhengHei', 12, 'bold'),
            bg='white',
            fg=color,
            width=10,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        tk.Label(
            name_frame,
            text=price_info,
            font=('Microsoft JhengHei', 10),
            bg='white',
            fg='#7f8c8d'
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # 輸入框和調整按鈕
        input_row = tk.Frame(fruit_frame, bg='white')
        input_row.pack(fill=tk.X)
        
        # 斤數標籤和輸入框
        tk.Label(
            input_row,
            text="斤數：",
            font=('Microsoft JhengHei', 11),
            bg='white',
            width=6,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        entry = tk.Entry(
            input_row,
            font=('Microsoft JhengHei', 11),
            width=12,
            justify='center',
            textvariable=weight_var,
            bd=1,
            relief=tk.SOLID,
            bg='#ecf0f1'
        )
        entry.pack(side=tk.LEFT, padx=(0, 5))
        self.fruit_entries[fruit_name] = entry
        
        tk.Label(
            input_row,
            text="斤",
            font=('Microsoft JhengHei', 11),
            bg='white'
        ).pack(side=tk.LEFT)
        
        # 快速調整按鈕
        btn_frame = tk.Frame(input_row, bg='white')
        btn_frame.pack(side=tk.LEFT, padx=(15, 0))
        
        tk.Button(
            btn_frame,
            text="-",
            font=('Microsoft JhengHei', 9),
            width=3,
            command=lambda var=weight_var: self.adjust_weight(var, -1),
            bg='#ecf0f1',
            relief=tk.RAISED,
            bd=1,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 3))
        
        tk.Button(
            btn_frame,
            text="+",
            font=('Microsoft JhengHei', 9),
            width=3,
            command=lambda var=weight_var: self.adjust_weight(var, 1),
            bg='#ecf0f1',
            relief=tk.RAISED,
            bd=1,
            cursor="hand2"
        ).pack(side=tk.LEFT)
        
        return fruit_frame
    
    def create_right_panel(self, parent):
        """建立右側面板：結果顯示"""
        right_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        right_frame.pack_propagate(False)
        
        # 結果面板標題
        title_frame = tk.Frame(right_frame, bg='#2ecc71')
        title_frame.pack(fill=tk.X)
        
        tk.Label(
            title_frame,
            text="購物小票與計算結果",
            font=('Microsoft JhengHei', 14, 'bold'),
            bg='#2ecc71',
            fg='white',
            pady=15
        ).pack()
        
        # 結果顯示區域
        display_frame = tk.Frame(right_frame, bg='#f8f9fa')
        display_frame.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)
        
        # 文字顯示區域
        self.result_text = tk.Text(
            display_frame,
            font=('Microsoft JhengHei', 11),
            bg='#f8f9fa',
            wrap=tk.WORD,
            relief=tk.FLAT,
            state=tk.DISABLED,
            padx=15,
            pady=15
        )
        
        # 滾動條
        scrollbar = tk.Scrollbar(display_frame, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 初始提示文字
        self.update_result("請選擇顧客方案並輸入水果斤數，然後點擊「計算價格」按鈕。")
        
        return right_frame
    
    def create_footer(self, parent):
        """建立底部按鈕欄"""
        footer_frame = tk.Frame(parent, bg='#34495e', height=60)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        footer_frame.pack_propagate(False)
        
        # 按鈕容器
        button_container = tk.Frame(footer_frame, bg='#34495e')
        button_container.place(relx=0.5, rely=0.5, anchor='center')
        
        # 計算按鈕
        calc_button = tk.Button(
            button_container,
            text=" 計算價格",
            font=('Microsoft JhengHei', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.calculate_price,
            width=18,
            height=1,
            relief=tk.RAISED,
            bd=1,
            cursor="hand2",
            activebackground='#219955'
        )
        calc_button.pack(side=tk.LEFT, padx=8)
        
        # 清除按鈕
        clear_button = tk.Button(
            button_container,
            text=" 清除重填",
            font=('Microsoft JhengHei', 11, 'bold'),
            bg='#e67e22',
            fg='white',
            command=self.clear_entries,
            width=18,
            height=1,
            relief=tk.RAISED,
            bd=1,
            cursor="hand2",
            activebackground='#d35400'
        )
        clear_button.pack(side=tk.LEFT, padx=8)
        
        # 退出按鈕
        quit_button = tk.Button(
            button_container,
            text=" 退出系統",
            font=('Microsoft JhengHei', 11, 'bold'),
            bg='#e74c3c',
            fg='white',
            command=self.root.quit,
            width=18,
            height=1,
            relief=tk.RAISED,
            bd=1,
            cursor="hand2",
            activebackground='#c0392b'
        )
        quit_button.pack(side=tk.LEFT, padx=8)
    
    def toggle_fullscreen(self, event=None):
        """切換全螢幕模式"""
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
    
    def exit_fullscreen(self, event=None):
        """退出全螢幕模式"""
        self.root.attributes('-fullscreen', False)
    
    def adjust_weight(self, weight_var, delta):
        """調整斤數"""
        current = weight_var.get()
        new_value = max(0, current + delta)
        weight_var.set(new_value)
    
    def on_customer_changed(self, event=None):
        """顧客方案改變時的處理"""
        selected = self.selected_customer.get()
        if selected in self.customer_options:
            customer_info = self.customer_options[selected]
            
            # 更新方案描述
            self.customer_desc_label.config(text=customer_info["description"])
            
            # 根據方案顯示/隱藏芒果輸入
            if not customer_info["has_mango"]:
                # 方案A：隱藏芒果輸入框
                self.mango_frame.pack_forget()
                self.mango_weight.set(0)  # 重置芒果重量為0
            else:
                # 方案B、C、D：顯示芒果輸入框
                self.mango_frame.pack(fill=tk.X, pady=8)
    
    def validate_inputs(self):
        """驗證輸入"""
        try:
            apple = self.apple_weight.get()
            strawberry = self.strawberry_weight.get()
            mango = self.mango_weight.get()
            
            # 檢查是否全為零
            if apple == 0 and strawberry == 0 and mango == 0:
                messagebox.showwarning("警告", "請至少購買一種水果！所有水果斤數不能都為零。")
                return False
            
            # 檢查是否為負數
            if apple < 0 or strawberry < 0 or mango < 0:
                messagebox.showerror("輸入錯誤", "水果斤數不能為負數！")
                return False
            
            return True
        except tk.TclError:
            messagebox.showerror("輸入錯誤", "請輸入有效的整數！")
            return False
    
    def calculate_price(self):
        """計算價格"""
        if not self.validate_inputs():
            return
        
        apple = self.apple_weight.get()
        strawberry = self.strawberry_weight.get()
        mango = self.mango_weight.get()
        
        selected = self.selected_customer.get()
        if selected not in self.customer_options:
            messagebox.showerror("錯誤", "請選擇有效的顧客方案！")
            return
        
        customer_info = self.customer_options[selected]
        
        # 檢查顧客A是否購買了芒果
        if not customer_info["has_mango"] and mango > 0:
            messagebox.showwarning("方案限制", "顧客A方案不支持購買芒果！")
            return
        
        # 計算價格
        total = self.shopping_system.calculate_price(
            apple_weight=apple,
            strawberry_weight=strawberry,
            mango_weight=mango if customer_info["has_mango"] else 0,
            strawberry_discount=customer_info["strawberry_discount"],
            discount_threshold=customer_info["discount_threshold"],
            discount_amount=customer_info["discount_amount"]
        )
        
        # 獲取詳細計算結果
        details = self.shopping_system.get_detailed_calculation(
            apple_weight=apple,
            strawberry_weight=strawberry,
            mango_weight=mango if customer_info["has_mango"] else 0,
            strawberry_discount=customer_info["strawberry_discount"],
            discount_threshold=customer_info["discount_threshold"],
            discount_amount=customer_info["discount_amount"]
        )
        
        # 顯示結果
        self.display_result(customer_info, details, total)
    
    def display_result(self, customer_info, details, total):
        """顯示計算結果"""
        apple = self.apple_weight.get()
        strawberry = self.strawberry_weight.get()
        mango = self.mango_weight.get()
        
        result = "=" * 40 + "\n"
        result += f"顧客{customer_info['code']} 購物小票\n"
        result += "=" * 40 + "\n\n"
        
        # 顯示購買清單
        result += "【購買清單】\n"
        result += "-" * 30 + "\n"
        
        if apple > 0:
            result += f" 蘋果: {apple}斤 × 8元/斤 = {details['apple_price']:.1f}元\n"
        
        if strawberry > 0:
            discount_text = ""
            if customer_info["strawberry_discount"] != 1.0:
                discount_text = f" ({(1-customer_info['strawberry_discount'])*100:.0f}折)"
            
            result += f" 草莓: {strawberry}斤 × 13元/斤{discount_text} = {details['strawberry_price']:.1f}元\n"
        
        if mango > 0 and customer_info["has_mango"]:
            result += f" 芒果: {mango}斤 × 20元/斤 = {details['mango_price']:.1f}元\n"
        
        result += "-" * 30 + "\n\n"
        
        # 顯示小計
        result += f"【小計】 {details['subtotal']:.1f}元\n\n"
        
        # 顯示優惠信息（簡化版）
        if details['discount_applied']:
            result += f"滿減優惠: -{details['discount_amount']}元\n\n"
        
        # 顯示總計
        result += "=" * 40 + "\n"
        result += f"【應付總額】 {details['final_total']:.1f}元\n"
        result += "=" * 40
        
        self.update_result(result)
    
    def update_result(self, text):
        """更新結果顯示區域"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # 設定不同文字的樣式
        self.result_text.tag_configure('title', font=('Microsoft JhengHei', 12, 'bold'), foreground='#2c3e50')
        self.result_text.tag_configure('normal', font=('Microsoft JhengHei', 10), foreground='#34495e')
        self.result_text.tag_configure('highlight', font=('Microsoft JhengHei', 11, 'bold'), foreground='#e74c3c')
        self.result_text.tag_configure('discount', font=('Microsoft JhengHei', 10), foreground='#27ae60')
        
        # 插入格式化文字
        lines = text.split('\n')
        for line in lines:
            if '顧客' in line and '購物小票' in line:
                self.result_text.insert(tk.END, line + '\n', 'title')
            elif '【' in line and '】' in line:
                self.result_text.insert(tk.END, line + '\n', 'title')
            elif '滿減優惠:' in line:
                self.result_text.insert(tk.END, line + '\n', 'discount')
            elif '=' in line or '-' in line:
                self.result_text.insert(tk.END, line + '\n', 'normal')
            elif '應付總額' in line:
                self.result_text.insert(tk.END, line + '\n', 'highlight')
            else:
                self.result_text.insert(tk.END, line + '\n', 'normal')
        
        self.result_text.config(state=tk.DISABLED)
    
    def clear_entries(self):
        """清除所有輸入框"""
        self.apple_weight.set(0)
        self.strawberry_weight.set(0)
        self.mango_weight.set(0)
        self.selected_customer.set(list(self.customer_options.keys())[0])
        self.on_customer_changed()  # 更新界面狀態
        self.update_result("請選擇顧客方案並輸入水果斤數，然後點擊「計算價格」按鈕。")

def main():
    """主函數 - 啟動應用程式"""
    root = tk.Tk()
    
    # 設定視窗圖標
    try:
        root.iconbitmap('fruit_icon.ico')
    except:
        pass
    
    # 建立應用程式
    app = FruitPriceCalculatorGUI(root)
    
    # 啟動主迴圈
    root.mainloop()

if __name__ == "__main__":
    main()