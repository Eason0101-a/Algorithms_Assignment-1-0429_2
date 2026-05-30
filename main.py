from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

try:
    from graphviz import Digraph
    HAS_GRAPHVIZ = True
except ImportError:
    HAS_GRAPHVIZ = False


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
        # 維持紅黑樹性質的調整
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
        # 維持紅黑樹性質的調整
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

    def print_tree(self):
        if self.root == self.nil:
            print("(空樹)")
            return
        
        # 收集每層的節點
        levels = []
        q = deque([(self.root, 0)])
        
        while q:
            node, level = q.popleft()
            
            # 擴展 levels 列表
            while len(levels) <= level:
                levels.append([])
            
            levels[level].append(node)
            
            if node.left != self.nil:
                q.append((node.left, level + 1))
            if node.right != self.nil:
                q.append((node.right, level + 1))
        
        # 打印樹結構
        max_level = len(levels)
        
        for level, nodes in enumerate(levels):
            # 計算縮進和間距
            indent = " " * (4 * (max_level - level - 1))
            spacing = " " * (8 * (max_level - level))
            
            line = indent
            for i, node in enumerate(nodes):
                if i > 0:
                    line += spacing
                # 顯示鍵值和顏色
                color_abbr = "🔴" if node.color == RED else "⚫"
                line += f"[{node.key}:{color_abbr}]"
            
            print(f"第 {level} 層: {line}")
        
        # 打印樹的詳細結構
        self._print_tree_structure()
    
    def _print_tree_structure(self):
        """使用遞迴打印樹的詳細結構（帶連接線）"""
        if self.root == self.nil:
            return
        
        print("\n樹的詳細結構:")
        self._print_tree_recursive(self.root, "", True)
    
    def _print_tree_recursive(self, node, prefix, is_tail):
        """遞迴打印樹節點及連接線"""
        if node == self.nil:
            return
        
        # 打印當前節點
        color_abbr = "🔴" if node.color == RED else "⚫"
        print(prefix + ("└── " if is_tail else "├── ") + f"{node.key}({color_abbr})")
        
        # 準備下一層的前綴
        extension = "    " if is_tail else "│   "
        
        # 計算子節點
        children = []
        if node.left != self.nil:
            children.append(node.left)
        if node.right != self.nil:
            children.append(node.right)
        
        # 遞迴打印子節點
        for i, child in enumerate(children):
            is_last = (i == len(children) - 1)
            self._print_tree_recursive(child, prefix + extension, is_last)
    
    def generate_tree_image(self, filename="red_black_tree"):
        """使用 matplotlib 生成紅黑樹的 PNG 圖片"""
        if self.root == self.nil:
            print("錯誤: 樹是空的，無法生成圖片")
            return False
        
        try:
            fig, ax = plt.subplots(1, 1, figsize=(14, 10))
            ax.set_xlim(-1, 20)
            ax.set_ylim(-1, 12)
            ax.axis('off')
            
            # 計算節點位置
            positions = {}
            self._calculate_positions(self.root, positions, x=10, y=10, offset=5)
            
            # 繪製邊
            self._draw_edges(ax, self.root, positions)
            
            # 繪製節點
            self._draw_nodes(ax, self.root, positions)
            
            # 添加標題
            plt.title('紅黑樹結構', fontsize=16, fontweight='bold', pad=20)
            
            # 添加圖例
            red_patch = patches.Patch(facecolor='red', edgecolor='black', label='紅色節點')
            black_patch = patches.Patch(facecolor='black', edgecolor='white', label='黑色節點')
            ax.legend(handles=[red_patch, black_patch], loc='upper right', fontsize=12)
            
            # 保存圖片
            output_file = f"{filename}.png"
            plt.tight_layout()
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            print(f"✓ 圖片已生成: {output_file}")
            plt.close()
            return True
        except Exception as e:
            print(f"生成圖片出錯: {e}")
            return False
    
    def _calculate_positions(self, node, positions, x, y, offset):
        """計算樹中每個節點的座標位置"""
        if node == self.nil:
            return
        
        positions[id(node)] = (x, y)
        
        # 計算左右子樹的位置
        if node.left != self.nil:
            self._calculate_positions(node.left, positions, x - offset, y - 2, offset / 2)
        if node.right != self.nil:
            self._calculate_positions(node.right, positions, x + offset, y - 2, offset / 2)
    
    def _draw_edges(self, ax, node, positions):
        """繪製樹的邊"""
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
        """遞迴繪製樹的節點"""
        if node == self.nil:
            return
        
        x, y = positions[id(node)]
        
        # 確定節點顏色
        node_color = 'red' if node.color == RED else 'black'
        text_color = 'white'
        
        # 繪製圓形節點
        circle = patches.Circle((x, y), 0.4, facecolor=node_color, 
                               edgecolor='black', linewidth=2)
        ax.add_patch(circle)
        
        # 添加文字標籤
        ax.text(x, y, str(node.key), fontsize=11, fontweight='bold',
               ha='center', va='center', color=text_color)
        
        # 遞迴繪製子樹
        if node.left != self.nil:
            self._draw_nodes(ax, node.left, positions)
        if node.right != self.nil:
            self._draw_nodes(ax, node.right, positions)


if __name__ == "__main__":
    rbt = RedBlackTree()
    
    # 初始數據
    initial_data = [10, 20, 30, 15, 25, 5, 1, 8, 12]
    
    # 插入初始數據
    for v in initial_data:
        rbt.insert(v)
    
    print("=" * 50)
    print("         紅黑樹互動式管理系統")
    print("=" * 50)
    print(f"初始數據已插入: {initial_data}\n")
    
    while True:
        print("\n" + "=" * 50)
        print("選擇操作:")
        print("1. 查看樹的結構")
        print("2. 插入新的數字")
        print("3. 刪除數字")
        print("4. 搜尋數字")
        print("5. 中序走訪 (排序顯示)")
        print("6. 生成樹的圖片")
        print("7. 重置樹 (回到初始數據)")
        print("8. 退出")
        print("=" * 50)
        
        choice = input("請輸入選項 (1-8): ").strip()
        
        if choice == "1":
            print("\n✓ 插入後的樹結構:")
            rbt.print_tree()
        
        elif choice == "2":
            try:
                num_input = input("請輸入要插入的數字 (可以輸入多個，用逗號分隔): ").strip()
                numbers = [int(x.strip()) for x in num_input.split(",")]
                for num in numbers:
                    rbt.insert(num)
                    print(f"  ✓ 已插入 {num}")
                print("\n插入後的樹結構:")
                rbt.print_tree()
            except ValueError:
                print("❌ 錯誤: 請輸入有效的數字")
        
        elif choice == "3":
            try:
                num_input = input("請輸入要刪除的數字 (可以輸入多個，用逗號分隔): ").strip()
                numbers = [int(x.strip()) for x in num_input.split(",")]
                for num in numbers:
                    if rbt.delete(num):
                        print(f"  ✓ 已刪除 {num}")
                    else:
                        print(f"  ✗ 找不到 {num}")
                print("\n刪除後的樹結構:")
                rbt.print_tree()
            except ValueError:
                print("❌ 錯誤: 請輸入有效的數字")
        
        elif choice == "4":
            try:
                num = int(input("請輸入要搜尋的數字: ").strip())
                result = rbt.search(num)
                if result != rbt.nil:
                    print(f"✓ 搜尋 {num}: 找到")
                else:
                    print(f"✗ 搜尋 {num}: 找不到")
            except ValueError:
                print("❌ 錯誤: 請輸入有效的數字")
        
        elif choice == "5":
            ordered = []
            rbt.inorder(rbt.root, ordered)
            if ordered:
                print("\n中序走訪結果 (已排序):")
                print(f"數字列表: {[x[0] for x in ordered]}")
                print(f"詳細資訊: {ordered}")
            else:
                print("樹是空的")
        
        elif choice == "6":
            print("\n正在生成圖片...")
            rbt.generate_tree_image("red_black_tree_current")
        
        elif choice == "7":
            print("\n正在重置樹...")
            rbt = RedBlackTree()
            for v in initial_data:
                rbt.insert(v)
            print(f"✓ 樹已重置為初始數據: {initial_data}")
            rbt.print_tree()
        
        elif choice == "8":
            print("\n感謝使用，再見！")
            break
        
        else:
            print("❌ 無效選項，請輸入 1-8 之間的數字")
