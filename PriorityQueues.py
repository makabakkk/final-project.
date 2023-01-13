from line_profiler import LineProfiler
from graphviz import Digraph

class Node:
	def __init__(self, key=None,next=None):
		self.key = key
		self.next = next

class PriorityQueues:
	def __init__(self):
		self.head = None
		self.size = 0

	# 获取链表中下标为idx的元素
	def getNode(self,idx):
		if idx < 0 or idx >= self.size:
			return None
		p = self.head
		for i in range(0,idx):
			p = p.next
		return p
	# 获取链表中下标为idx的父亲元素
	def getParent(self,idx):
		return self.getNode((idx-1)//2)

	# 获取链表中下标为idx的左孩子元素
	def getLeftChild(self,idx):
		return self.getNode(2*idx+1)

	# 获取链表中下标为idx的右孩子元素
	def getRightChild(self,idx):
		return self.getNode(2*idx+2)

	# 将元素key放入链表尾
	# @profile
	def pushBack(self,key):
		node = Node(key)
		if self.head == None:
			self.head = node
		else:
			p = self.getNode(self.size-1)
			p.next = node
		self.size += 1

	# 指定下标元素进行上浮
	# @profile
	def swim(self,idx):
		curNode = self.getNode(idx)
		if curNode == None:
			return;

		parent = self.getParent(idx)
		tmpValue = curNode.key
		while idx > 0 and tmpValue < parent.key:
			curNode.key = parent.key # 上浮

			idx = (idx-1)//2
			curNode = parent
			parent = self.getParent(idx)
		curNode.key = tmpValue

	# 删除队头元素，并将队尾元素值放到队头
	# @profile
	def popFirst(self):
		if self.size > 1:
			lastTwo = self.getNode(self.size-2) # 获取队列尾结点的前一个
			self.head.key =  lastTwo.next.key # 队列尾值放到队列头
			lastTwo.next = None # 删掉最后一个节点
		else:
			self.head = None
		self.size -= 1 # 长度减一

	# 指定下标元素进行下沉
	# @profile
	def sink(self,idx):
		curNode = self.getNode(idx)
		if curNode == None:
			return;

		tmpValue = curNode.key
		while 2*idx+1 < self.size:
			node = self.getLeftChild(idx)
			right = self.getRightChild(idx)
			idx = idx*2 + 1
			# node指向左右孩子值较小的一个
			if right != None and right.key < node.key :
				node = right
				idx = idx*2 + 2

			if tmpValue > node.key:
				curNode.key = node.key
				curNode = node
			else:
				break
		curNode.key = tmpValue

	# @profile
	def insert(self,key):
		self.pushBack(key)
		self.swim(self.size-1)

	# @profile
	def delMin(self):
		if self.size <= 0:
			return -1

		top = self.head.key
		self.popFirst()
		self.sink(0)
		return top

	def makeTree(self):
		g = Digraph('Q5', filename='Q5.gv',format='png')

		for idx in range(0,self.size//2):
			root = self.getNode(idx)
			left = self.getLeftChild(idx)
			right = self.getRightChild(idx)

			if left != None:
				g.edge(str(root.key),str(left.key))
			if right != None:
				g.edge(str(root.key),str(right.key))

		g.view()

pq = PriorityQueues()

for key in [47,79,56,38,40,80,95,24]:
	pq.insert(key)

pq.makeTree()

for i in range(0,8):
	print(pq.delMin(),end=" ")
print()