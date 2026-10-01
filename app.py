import streamlit as st
from datetime import datetime
from io import BytesIO

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Ứng dụng tính hóa đơn trà sữa",
    page_icon="🧋",
    layout="centered"
)

st.title("🧋 HỆ THỐNG THANH TOÁN QUÁN TRÀ SỮA")
st.markdown("---")

# =========================
# DỮ LIỆU MENU
# =========================
MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa trân châu đường đen": 35000,
    "Trà sữa matcha": 38000,
    "Trà đào": 28000,
    "Trà vải": 28000,
    "Trà chanh": 25000,
    "Matcha Latte": 42000,
    "Matcha Latte Kem Cheese": 48000
}

TOPPINGS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 7000,
    "Pudding": 8000,
    "Kem cheese": 10000
}

# =========================
# FORM NHẬP LIỆU
# =========================
st.subheader("Thông tin đơn hàng")

phone = st.text_input(
    "📱 Số điện thoại khách hàng (tích điểm)",
    max_chars=10
)

drink = st.selectbox(
    "🥤 Chọn thức uống",
    list(MENU.keys())
)

quantity = st.number_input(
    "🔢 Số lượng",
    min_value=1,
    value=1,
    step=1
)

sugar = st.selectbox(
    "🍬 Mức độ đường",
    ["100%", "70%", "50%", "0%"]
)

ice = st.selectbox(
    "🧊 Mức độ đá",
    ["Đá riêng", "Không đá"]
)

selected_toppings = st.multiselect(
    "➕ Chọn topping",
    list(TOPPINGS.keys())
)

# =========================
# TÍNH TIỀN
# =========================
drink_price = MENU[drink]

topping_price = 0
for topping in selected_toppings:
    topping_price += TOPPINGS[topping]

unit_price = drink_price + topping_price
total = unit_price * quantity

# =========================
# TÍCH ĐIỂM
# =========================
points = total // 10000

# =========================
# HIỂN THỊ HÓA ĐƠN
# =========================
st.markdown("---")
st.subheader("📋 Chi tiết hóa đơn")

st.write(f"**Khách hàng:** {phone if phone else 'Chưa nhập'}")
st.write(f"**Thức uống:** {drink}")
st.write(f"**Số lượng:** {quantity}")
st.write(f"**Mức đường:** {sugar}")
st.write(f"**Mức đá:** {ice}")

if selected_toppings:
    st.write("**Topping:**")
    for tp in selected_toppings:
        st.write(f"- {tp} ({TOPPINGS[tp]:,} VNĐ)")
else:
    st.write("**Topping:** Không")

st.write(f"**Đơn giá:** {unit_price:,} VNĐ")
st.write(f"**Tổng thanh toán:** {total:,} VNĐ")

if phone:
    st.success(f"⭐ Điểm tích lũy nhận được: {points} điểm")

# =========================
# TẠO FILE HÓA ĐƠN
# =========================
invoice_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

invoice_text = f"""
=====================================
         HOA DON TRA SUA
=====================================

Thoi gian: {invoice_time}

So dien thoai: {phone}

Thuc uong: {drink}
So luong: {quantity}

Muc duong: {sugar}
Muc da: {ice}

Topping:
"""

if selected_toppings:
    for tp in selected_toppings:
        invoice_text += f"- {tp}: {TOPPINGS[tp]:,} VND\n"
else:
    invoice_text += "Khong co\n"

invoice_text += f"""

Don gia: {unit_price:,} VND

Tong thanh toan: {total:,} VND

Diem tich luy: {points}

=====================================
Cam on quy khach!
=====================================
"""

# =========================
# THANH TOÁN
# =========================
st.markdown("---")

if st.button("💳 Thanh toán"):
    st.success("Thanh toán thành công!")

    file_data = BytesIO()
    file_data.write(invoice_text.encode("utf-8"))
    file_data.seek(0)

    st.download_button(
        label="📄 Tải hóa đơn",
        data=file_data,
        file_name=f"hoa_don_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

    st.balloons()
