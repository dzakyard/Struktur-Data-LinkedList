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

    def insert(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node


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
    if st.button("Tambah Node"):
        if data_input:
            st.session_state.linked_list.insert(data_input)
            st.success(f"Node '{data_input}' ditambahkan!")

# Tampilkan Visualisasi
st.subheader("Struktur Memory (Pointer Visual)")
if st.session_state.linked_list.head:
    graph = generate_viz(st.session_state.linked_list.head)
    st.graphviz_chart(graph)
else:
    st.info("List masih kosong. Tambahkan Node Melalui Sidebar")
