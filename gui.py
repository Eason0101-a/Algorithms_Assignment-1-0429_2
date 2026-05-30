import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque

# 紅黑樹的定義
RED = "RED"
BLACK = "BLACK"


class Node:
    def __init__(self, key, color=RED, left=None, right=None, parent=None):
        self.key = key
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent


class RedBlackTree:
    def __init__(self):
        self.nil = Node(None, color=BLACK)
        self.root = self.nil

    def search(self, key):
        current = self.root
        while current != self.nil and current.key != key:
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return current

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.nil:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def insert(self, key):
        new_node = Node(key, color=RED, left=self.nil, right=self.nil, parent=self.nil)
        parent = self.nil
        current = self.root
        while current != self.nil:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right
        new_node.parent = parent
        if parent == self.nil:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self.insert_fixup(new_node)

    def insert_fixup(self, z):
        while z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.left_rotate(z.parent.parent)
        self.root.color = BLACK

    def transplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        current = node
        while current.left != self.nil:
            current = current.left
        return current

    def delete(self, key):
        z = self.search(key)
        if z == self.nil:
            return False
        y = z
        y_original_color = y.color
        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == BLACK:
            self.delete_fixup(x)
        return True

    def delete_fixup(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def inorder(self, node, result):
        if node != self.nil:
            self.inorder(node.left, result)
            result.append((node.key, node.color))
            self.inorder(node.right, result)

    def _calculate_positions(self, node, positions, x, y, offset):
        if node == self.nil:
            return
        positions[id(node)] = (x, y)
        if node.left != self.nil:
            self._calculate_positions(node.left, positions, x - offset, y - 2, offset / 2)
        if node.right != self.nil:
            self._calculate_positions(node.right, positions, x + offset, y - 2, offset / 2)

    def _draw_edges(self, ax, node, positions):
        if node == self.nil:
            return
        node_pos = positions[id(node)]
        if node.left != self.nil:
            left_pos = positions[id(node.left)]
            ax.plot([node_pos[0], left_pos[0]], [node_pos[1], left_pos[1]], 
                   'k-', linewidth=1.5, alpha=0.6)
            self._draw_edges(ax, node.left, positions)
        if node.right != self.nil:
            right_pos = positions[id(node.right)]
            ax.plot([node_pos[0], right_pos[0]], [node_pos[1], right_pos[1]], 
                   'k-', linewidth=1.5, alpha=0.6)
            self._draw_edges(ax, node.right, positions)

    def _draw_nodes(self, ax, node, positions):
        if node == self.nil:
            return
        x, y = positions[id(node)]
        node_color = 'red' if node.color == RED else 'black'
        text_color = 'white'
        circle = plt.Circle((x, y), 0.4, facecolor=node_color, 
                           edgecolor='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, str(node.key), fontsize=11, fontweight='bold',
               ha='center', va='center', color=text_color)
        if node.left != self.nil:
            self._draw_nodes(ax, node.left, positions)
        if node.right != self.nil:
            self._draw_nodes(ax, node.right, positions)

    def draw(self, fig):
        ax = fig.add_subplot(111)
        if self.root == self.nil:
            ax.text(0.5, 0.5, '空樹', fontsize=16, ha='center', va='center',
                   transform=ax.transAxes)
        else:
            positions = {}
            self._calculate_positions(self.root, positions, x=10, y=10, offset=5)
            self._draw_edges(ax, self.root, positions)
            self._draw_nodes(ax, self.root, positions)
            ax.set_xlim(-1, 20)
            ax.set_ylim(-1, 12)
        ax.axis('off')


class RedBlackTreeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("紅黑樹互動式管理系統")
        self.root.geometry("1000x700")
        self.rbt = RedBlackTree()
        
        # 初始數據
        self.initial_data = [10, 20, 30, 15, 25, 5, 1, 8, 12]
        for v in self.initial_data:
            self.rbt.insert(v)
        
        # 創建界面
        self.create_widgets()
        self.update_tree_display()
    
    def create_widgets(self):
        # 上方控制面板
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # 插入框
        ttk.Label(control_frame, text="插入:").grid(row=0, column=0, padx=5)
        self.insert_entry = ttk.Entry(control_frame, width=20)
        self.insert_entry.grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="插入", command=self.insert_values).grid(row=0, column=2, padx=5)
        
        # 刪除框
        ttk.Label(control_frame, text="刪除:").grid(row=0, column=3, padx=5)
        self.delete_entry = ttk.Entry(control_frame, width=20)
        self.delete_entry.grid(row=0, column=4, padx=5)
        ttk.Button(control_frame, text="刪除", command=self.delete_values).grid(row=0, column=5, padx=5)
        
        # 搜尋框
        ttk.Label(control_frame, text="搜尋:").grid(row=1, column=0, padx=5)
        self.search_entry = ttk.Entry(control_frame, width=20)
        self.search_entry.grid(row=1, column=1, padx=5)
        ttk.Button(control_frame, text="搜尋", command=self.search_value).grid(row=1, column=2, padx=5)
        
        # 其他按鈕
        ttk.Button(control_frame, text="查看排序", command=self.show_inorder).grid(row=1, column=3, padx=5)
        ttk.Button(control_frame, text="重置樹", command=self.reset_tree).grid(row=1, column=4, padx=5)
        ttk.Button(control_frame, text="儲存圖片", command=self.save_image).grid(row=1, column=5, padx=5)
        
        # 狀態標籤
        self.status_label = ttk.Label(self.root, text="", relief=tk.SUNKEN)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 圖表框架
        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def update_tree_display(self):
        # 清空舊圖表
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        # 創建新圖表
        fig = Figure(figsize=(10, 6), dpi=80)
        self.rbt.draw(fig)
        
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 更新統計信息
        ordered = []
        self.rbt.inorder(self.rbt.root, ordered)
        count = len(ordered)
        values = [str(x[0]) for x in ordered]
        self.status_label.config(
            text=f"節點數: {count} | 數據: {', '.join(values) if values else '(空樹)'}"
        )
    
    def insert_values(self):
        text = self.insert_entry.get().strip()
        if not text:
            messagebox.showwarning("警告", "請輸入要插入的數字")
            return
        
        try:
            numbers = [int(x.strip()) for x in text.split(",")]
            for num in numbers:
                self.rbt.insert(num)
            self.insert_entry.delete(0, tk.END)
            self.update_tree_display()
            messagebox.showinfo("成功", f"已插入 {len(numbers)} 個數字")
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字（用逗號分隔）")
    
    def delete_values(self):
        text = self.delete_entry.get().strip()
        if not text:
            messagebox.showwarning("警告", "請輸入要刪除的數字")
            return
        
        try:
            numbers = [int(x.strip()) for x in text.split(",")]
            success_count = 0
            for num in numbers:
                if self.rbt.delete(num):
                    success_count += 1
            self.delete_entry.delete(0, tk.END)
            self.update_tree_display()
            messagebox.showinfo("成功", f"已刪除 {success_count}/{len(numbers)} 個數字")
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字（用逗號分隔）")
    
    def search_value(self):
        text = self.search_entry.get().strip()
        if not text:
            messagebox.showwarning("警告", "請輸入要搜尋的數字")
            return
        
        try:
            num = int(text)
            result = self.rbt.search(num)
            if result != self.rbt.nil:
                messagebox.showinfo("搜尋結果", f"✓ 找到數字 {num}")
            else:
                messagebox.showinfo("搜尋結果", f"✗ 找不到數字 {num}")
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字")
    
    def show_inorder(self):
        ordered = []
        self.rbt.inorder(self.rbt.root, ordered)
        if ordered:
            values = [str(x[0]) for x in ordered]
            messagebox.showinfo("中序走訪", f"排序結果: {', '.join(values)}")
        else:
            messagebox.showinfo("中序走訪", "樹是空的")
    
    def reset_tree(self):
        if messagebox.askyesno("確認", "確定要重置樹到初始數據嗎？"):
            self.rbt = RedBlackTree()
            for v in self.initial_data:
                self.rbt.insert(v)
            self.update_tree_display()
            messagebox.showinfo("成功", "樹已重置")
    
    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            fig = Figure(figsize=(10, 6), dpi=150)
            self.rbt.draw(fig)
            fig.savefig(file_path, bbox_inches='tight')
            messagebox.showinfo("成功", f"圖片已儲存: {file_path}")


if __name__ == "__main__":
    window = tk.Tk()
    app = RedBlackTreeGUI(window)
    window.mainloop()
