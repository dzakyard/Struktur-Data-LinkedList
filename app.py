from ast import TypeVarTuple
import streamlit as st
from graphviz import Digraph

# 1. Definisi Struktur Data
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.length += 1

    def pop(self):
        if self.length == 0:
            return None
        pre = self.head
        temp = self.head
        while temp.next:
            pre = temp
            temp = temp.next
        self.tail = pre
        self.tail.next = None
        self.length -= 1
        if self.length == 0:
            self.head = None
            self.tail = None
        return temp.value

    def prepend(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.length += 1
        return True

    def pop_first(self):
        if self.length == 0:
            return None
        if self.length == 1:
            self.head = None
            self.tail = None
        temp = self.head
        self.head = self.head.next
        self.length -= 1
        return temp.value

    def get(self, index):
        if index < 0 and index >= self.length:
            return False
        temp = self.head
        for _ in range(1, index):
            temp = temp.next
        return temp
        return True

    def set_value(self, index, value):
        temp = self.get(index)
        if temp:
            temp.value = value
            return True
        return False

    def insert(self, index, value):
        if index < 0 and index > self.length:
            return False
        if index == 0:
            return self.prepend(value) 
        if index == self.length:
            return self.append(value)
        new_node = Node(value)
        temp = self.get(index - 1)
        new_node.next = temp.next
        temp.next = new_node
        self.length += 1
        return True
    
    def remove(self, index):
        if index < 0 and index >= self.length:
            return False
        if index == 0:
            return self.pop_first()
        if index == self.length - 1:
            return self.pop()
        pre = self.get(index - 1)
        temp = pre.next
        pre.next = temp.next
        temp.next = None
        self.length -= 1
        return temp.value
        return True


# 2. Fungsi Visualisasi Web
def generate_viz(head):
    dot = Digraph()
    dot.attr(rankdir="LR")
    dot.attr("node", shape="record", style="filled", color="lightgreen")

    current = head
    while current:
        node_id = str(id(current))
        dot.node(node_id, f"{{  {current.value} |   <next>  }}")
        if current.next:
            dot.edge(f"{node_id}:next", str(id(current.next)))
        current = current.next
    return dot


# 3. UI Streamlit
st.title("Visualizer Stuktur Data Interaktif")

# init state agar tidak hilang saat refresh
if "linked_list" not in st.session_state:
    st.session_state.linked_list = LinkedList()

# Input User
with st.sidebar:
    data_input = st.text_input("Masukkan Data Node:")
    if st.button("Append"):
        if data_input:
            st.session_state.linked_list.append(data_input)
            st.success(f"Node '{data_input}' ditambahkan!")

    if st.button("Pop"):
        pop_value = st.session_state.linked_list.pop()
        st.success(f"{pop_value} berhasil dihapus")

    if st.button("Prepend"):
        if data_input:
            st.session_state.linked_list.prepend(data_input)
            st.success(f"{data_input} berhasil ditambahkan di depan")

    if st.button("Pop First"):
        pop_value = st.session_state.linked_list.pop_first()
        st.success(f"{pop_value} berhasil dihapus")

    index_input = st.number_input("Masukkan Nomor Node:", min_value=1, key="n1")
    if st.button("Get"):
        temp = st.session_state.linked_list.get(index_input)
        st.success(f"Data ke-{index_input} adalah {temp.value}")

    index_input = st.number_input("Masukkan Nomor Node:", min_value=1, key="n2")
    value_input = st.text_input("Masukkan data:")
    if st.button("Set"):
        temp = st.session_state.linked_list.get(index_input)
        st.session_state.linked_list.set_value(index_input, value_input)

    if st.button("Insert"):
        st.session_state.linked_list.insert(index_input, value_input)
        st.success(f"{value_input} berhasil ditambahkan")

    index_input = st.number_input("Masukkan Nomor Node:", min_value=1, key="n3")
    if st.button("Remove"):
        temp = st.session_state.linked_list.remove(index_input)
        st.success(f"{temp} berhasil dihapus")




# Tampilkan Visualisasi
st.subheader("LinkedList")
if st.session_state.linked_list.head:
    graph = generate_viz(st.session_state.linked_list.head)
    st.graphviz_chart(graph)
else:
    st.info("List masih kosong. Tambahkan Node Melalui Sidebar")
