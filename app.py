# app.py
import json
from anytree import Node, RenderTree, AsciiStyle
from anytree.exporter import DotExporter
import streamlit as st
from PIL import Image
import os

# -----------------------------
# 1. Загрузка базы знаний
# -----------------------------
def load_knowledge(file_path="decision_tree.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------
# 2. Построение дерева
# -----------------------------
def build_tree(data, parent=None):
    node = Node(data["condition"], parent=parent, **data.get("parameters", {}))
    for action in data.get("actions", []):
        Node(
            f'{action["description"]} (Вероятность успеха: {action["success_probability"]})',
            parent=node,
            instrument=action.get("instrument", ""),
            warning=action.get("warning", "")
        )
    return node

# -----------------------------
# 3. Визуализация дерева
# -----------------------------
def render_tree(root_node):
    try:
        DotExporter(root_node).to_picture("decision_tree.png")
        return "decision_tree.png"
    except Exception as e:
        st.error(f"Ошибка генерации дерева: {e}")
        return None

# -----------------------------
# 4. Streamlit UI
# -----------------------------
st.title("Дерево решений по ликвидации аварий на бурении")

# Загружаем базу знаний
knowledge = load_knowledge()

# Выбор типа аварии
types_of_incidents = [d["condition"] for d in knowledge]
selected_incident = st.selectbox("Выберите тип аварии", types_of_incidents)

# Строим дерево для выбранного типа
data = next(d for d in knowledge if d["condition"] == selected_incident)
root = build_tree(data)
st.subheader("Текстовая структура дерева:")
st.text(RenderTree(root, style=AsciiStyle()).by_attr())

# Визуализация графической схемы
image_path = render_tree(root)
if image_path and os.path.exists(image_path):
    st.image(Image.open(image_path), caption="Дерево решений")
else:
    st.warning("Дерево не удалось визуализировать")
