import streamlit as st
from datetime import datetime
import html
# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Trà Sữa POS",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# =========================================================
# CSS GIAO DIỆN
# =========================================================
st.markdown("""
<style>
    .main {
        background-color: #fff8f5;
    }
    .title {
        text-align: center;
        color: #8B4513;
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #777;
        font-size: 16px;
        margin-bottom: 25px;
    }
    .price-box {
        background: #fff;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #eee;
        margin-bottom: 10px;
    }
    .total-box {
        background: linear-gradient(135deg, #8B4513, #C96F45);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-top: 15px;
    }
    .total-price {
        font-size: 32px;
        font-weight: 800;
    }
    .invoice {
        background: white;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #ddd;
        color: #222;
    }
    .invoice-title {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #8B4513;
    }
    .invoice-center {
        text-align: center;
    }
    .invoice-line {
        border-top: 1px dashed #999;
        margin: 15px 0;
    }
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)
# =========================================================
# DỮ LIỆU MENU
# =========================================================
MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa chocolate": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa khoai môn": 38000,
    "Trà sữa socola": 38000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
    "Trà tắc": 25000,
}
SIZES = {
    "Size M": 0,
    "Size L": 10000,
    "Size XL": 15000,
}
TOPPINGS = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch dừa": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
    "Trân châu hoàng kim": 7000,
}
SUGAR_LEVELS = [
    "0% - Không đường",
    "30% - Ít đường",
    "50% - Bình thường",
    "70% - Ngọt",
    "100% - Rất ngọt",
]
ICE_LEVELS = [
    "0% - Không đá",
    "30% - Ít đá",
    "50% - Bình thường",
    "70% - Nhiều đá",
    "100% - Rất nhiều đá",
]
# =========================================================
# HÀM TIỆN ÍCH
# =========================================================
def format_currency(number):
    """Định dạng tiền Việt Nam."""
    return f"{number:,.0f} đ".replace(",", ".")
def calculate_item_price(drink, size, topping):
    """Tính giá một món."""
    return MENU[drink] + SIZES[size] + TOPPINGS[topping]
def generate_invoice_number():
    """Tạo mã hóa đơn theo thời gian."""
    return datetime.now().strftime("HD%Y%m%d%H%M%S")
def create_invoice_html(customer_name, invoice_number, items, total):
    """Tạo HTML hóa đơn để người dùng có thể in/lưu PDF."""
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    rows = ""
    for index, item in enumerate(items, start=1):
        rows += f"""
        <tr>
            <td>{index}</td>
            <td>
                <b>{html.escape(item['drink'])}</b><br>
                <small>
                    {html.escape(item['size'])} |
                    {html.escape(item['topping'])}<br>
                    Đường: {html.escape(item['sugar'])}<br>
                    Đá: {html.escape(item['ice'])}
                </small>
            </td>
            <td style="text-align:center;">{item['quantity']}</td>
            <td style="text-align:right;">{format_currency(item['unit_price'])}</td>
            <td style="text-align:right;">
                {format_currency(item['total_price'])}
            </td>
        </tr>
        """
    invoice_html = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Hóa đơn {invoice_number}</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background: #f4f4f4;
    padding: 20px;
}}
.invoice {{
    max-width: 800px;
    margin: auto;
    background: white;
    padding: 35px;
    border-radius: 10px;
}}
h1 {{
    text-align: center;
    color: #8B4513;
    margin-bottom: 5px;
}}
.center {{
    text-align: center;
}}
.info {{
    margin-top: 20px;
    margin-bottom: 20px;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}}
th {{
    background: #8B4513;
    color: white;
    padding: 10px;
}}
td {{
    border-bottom: 1px solid #ddd;
    padding: 10px;
    vertical-align: top;
}}
.total {{
    text-align: right;
    font-size: 22px;
    font-weight: bold;
    color: #8B4513;
    margin-top: 20px;
}}
.footer {{
    text-align: center;
    margin-top: 30px;
    color: #777;
}}
@media print {{
    body {{
        background: white;
        padding: 0;
    }}
    .invoice {{
        box-shadow: none;
        border: none;
    }}
}}
</style>
</head>
<body>
<div class="invoice">
    <h1>🧋 TRÀ SỮA</h1>
    <div class="center">
        <b>HÓA ĐƠN THANH TOÁN</b>
    </div>
    <hr>
    <div class="info">
        <b>Mã hóa đơn:</b> {invoice_number}<br>
        <b>Khách hàng:</b>
        {html.escape(customer_name)}<br>
        <b>Thời gian:</b> {now}
    </div>
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Món</th>
                <th>Số lượng</th>
                <th>Đơn giá</th>
                <th>Thành tiền</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    <div class="total">
        TỔNG THANH TOÁN: {format_currency(total)}
    </div>
    <div class="footer">
        Cảm ơn quý khách và hẹn gặp lại! ❤️
    </div>
</div>
<script>
    window.onload = function() {{
        window.print();
    }}
</script>
</body>
</html>
"""
    return invoice_html
# =========================================================
# SESSION STATE
# =========================================================
if "cart" not in st.session_state:
    st.session_state.cart = []
if "paid" not in st.session_state:
    st.session_state.paid = False
if "invoice_number" not in st.session_state:
    st.session_state.invoice_number = None
if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""
# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="title">🧋 TRÀ SỮA POS</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Hệ thống tính tiền & quản lý hóa đơn</div>',
    unsafe_allow_html=True
)
st.divider()
# =========================================================
# THÔNG TIN KHÁCH HÀNG
# =========================================================
st.subheader("👤 Thông tin khách hàng")
customer_name = st.text_input(
    "Tên khách hàng",
    value=st.session_state.customer_name,
    placeholder="Nhập tên khách hàng..."
)
st.session_state.customer_name = customer_name
# =========================================================
# KHU VỰC THÊM MÓN
# =========================================================
st.subheader("🧋 Chọn món")
col1, col2 = st.columns(2)
with col1:
    drink = st.selectbox(
        "Loại trà sữa / nước",
        list(MENU.keys())
    )
    size = st.selectbox(
        "Size",
        list(SIZES.keys())
    )
    topping = st.selectbox(
        "Topping",
        list(TOPPINGS.keys())
    )
with col2:
    sugar = st.selectbox(
        "Mức độ đường",
        SUGAR_LEVELS,
        index=2
    )
    ice = st.selectbox(
        "Mức độ đá",
        ICE_LEVELS,
        index=2
    )
    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=50,
        value=1,
        step=1
    )
# =========================================================
# GIÁ MÓN
# =========================================================
unit_price = calculate_item_price(
    drink,
    size,
    topping
)
item_total = unit_price * quantity
st.info(
    f"💰 Đơn giá: **{format_currency(unit_price)}**  |  "
    f"Thành tiền: **{format_currency(item_total)}**"
)
# =========================================================
# THÊM MÓN VÀO BILL
# =========================================================
col_add, col_clear = st.columns(2)
with col_add:
    if st.button(
        "➕ THÊM MÓN VÀO HÓA ĐƠN",
        use_container_width=True,
        type="primary"
    ):
        new_item = {
            "drink": drink,
            "size": size,
            "topping": topping,
            "sugar": sugar,
            "ice": ice,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": item_total
        }
        st.session_state.cart.append(new_item)
        # Khi thêm món mới thì hóa đơn quay lại trạng thái chưa thanh toán
        st.session_state.paid = False
        st.success("Đã thêm món vào hóa đơn!")
with col_clear:
    if st.button(
        "🗑️ XÓA TOÀN BỘ HÓA ĐƠN",
        use_container_width=True
    ):
        st.session_state.cart = []
        st.session_state.paid = False
        st.session_state.invoice_number = None
        st.rerun()
# =========================================================
# HIỂN THỊ GIỎ HÀNG
# =========================================================
st.divider()
st.subheader("🧾 Hóa đơn hiện tại")
if len(st.session_state.cart) == 0:
    st.warning(
        "Chưa có món nào trong hóa đơn. "
        "Hãy chọn món và bấm 'Thêm món vào hóa đơn'."
    )
else:
    total_bill = sum(
        item["total_price"]
        for item in st.session_state.cart
    )
    # ---------------------------------------------
    # Hiển thị từng món
    # ---------------------------------------------
    for index, item in enumerate(st.session_state.cart):
        col_info, col_delete = st.columns([6, 1])
        with col_info:
            st.markdown(
                f"""
                <div class="price-box">
                <b>{index + 1}. {item['drink']}</b><br>
                📏 {item['size']}
                &nbsp; | &nbsp;
                🧋 {item['topping']}
                <br>
                🍬 {item['sugar']}
                &nbsp; | &nbsp;
                🧊 {item['ice']}
                <br><br>
                Số lượng:
                <b>{item['quantity']}</b>
                &nbsp; | &nbsp;
                Đơn giá:
                <b>{format_currency(item['unit_price'])}</b>
                &nbsp; | &nbsp;
                Thành tiền:
                <b style="color:#C96F45">
                    {format_currency(item['total_price'])}
                </b>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_delete:
            if st.button(
                "❌",
                key=f"delete_{index}",
                help="Xóa món này"
            ):
                st.session_state.cart.pop(index)
                st.rerun()
    # =====================================================
    # TỔNG TIỀN
    # =====================================================
    st.markdown(
        f"""
        <div class="total-box">
            <div>TỔNG THANH TOÁN</div>
            <div class="total-price">
                {format_currency(total_bill)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("")
    # =====================================================
    # THANH TOÁN
    # =====================================================
    if not st.session_state.paid:
        if st.button(
            "💳 THANH TOÁN",
            use_container_width=True,
            type="primary"
        ):
            if not customer_name.strip():
                st.error(
                    "Vui lòng nhập tên khách hàng trước khi thanh toán."
                )
            else:
                st.session_state.invoice_number = (
                    generate_invoice_number()
                )
                st.session_state.paid = True
                st.success(
                    "Thanh toán thành công! Hóa đơn đã được tạo."
                )
                st.rerun()
# =========================================================
# HIỂN THỊ HÓA ĐƠN SAU THANH TOÁN
# =========================================================
if (
    st.session_state.paid
    and len(st.session_state.cart) > 0
):
    st.divider()
    st.subheader("✅ HÓA ĐƠN ĐÃ THANH TOÁN")
    total_bill = sum(
        item["total_price"]
        for item in st.session_state.cart
    )
    invoice_number = st.session_state.invoice_number
    now = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    # =====================================================
    # HIỂN THỊ HÓA ĐƠN TRÊN APP
    # =====================================================
    invoice_rows = ""
    for index, item in enumerate(
        st.session_state.cart,
        start=1
    ):
        invoice_rows += f"""
        <tr>
            <td>{index}</td>
            <td>
                <b>{html.escape(item['drink'])}</b><br>
                <small>
                    {html.escape(item['size'])}<br>
                    {html.escape(item['topping'])}<br>
                    Đường: {html.escape(item['sugar'])}<br>
                    Đá: {html.escape(item['ice'])}
                </small>
            </td>
            <td style="text-align:center;">
                {item['quantity']}
            </td>
            <td style="text-align:right;">
                {format_currency(item['unit_price'])}
            </td>
            <td style="text-align:right;">
                {format_currency(item['total_price'])}
            </td>
        </tr>
        """
    invoice_display = f"""
    <div class="invoice">
        <div class="invoice-title">
            🧋 TRÀ SỮA
        </div>
        <div class="invoice-center">
            <b>HÓA ĐƠN THANH TOÁN</b>
        </div>
        <div class="invoice-line"></div>
        <b>Mã hóa đơn:</b> {invoice_number}<br>
        <b>Khách hàng:</b>
        {html.escape(customer_name)}<br>
        <b>Thời gian:</b> {now}
        <div class="invoice-line"></div>
        <table style="width:100%; border-collapse:collapse;">
            <thead>
                <tr>
                    <th style="text-align:left;">#</th>
                    <th style="text-align:left;">Món</th>
                    <th>SL</th>
                    <th style="text-align:right;">Đơn giá</th>
                    <th style="text-align:right;">Thành tiền</th>
                </tr>
            </thead>
            <tbody>
                {invoice_rows}
            </tbody>
        </table>
        <div class="invoice-line"></div>
        <div style="
            text-align:right;
            font-size:24px;
            font-weight:bold;
            color:#8B4513;
        ">
            Tổng cộng: {format_currency(total_bill)}
        </div>
        <br>
        <div class="invoice-center">
            ❤️ Cảm ơn quý khách và hẹn gặp lại!
        </div>
    </div>
    """
    st.markdown(
        invoice_display,
        unsafe_allow_html=True
    )
    # =====================================================
    # XUẤT HÓA ĐƠN
    # =====================================================
    st.write("")
    invoice_html = create_invoice_html(
        customer_name,
        invoice_number,
        st.session_state.cart,
        total_bill
    )
    col_download, col_new = st.columns(2)
    with col_download:
        st.download_button(
            label="📥 XUẤT HÓA ĐƠN",
            data=invoice_html,
            file_name=f"{invoice_number}.html",
            mime="text/html",
            use_container_width=True
        )
    with col_new:
        if st.button(
            "🆕 TẠO HÓA ĐƠN MỚI",
            use_container_width=True
        ):
            st.session_state.cart = []
            st.session_state.paid = False
            st.session_state.invoice_number = None
            st.session_state.customer_name = ""
            st.rerun()
# =========================================================
# FOOTER
# =========================================================
st.divider()
st.markdown(
    """
    <div style="
        text-align:center;
        color:#999;
        padding:10px;
    ">
        🧋 Trà Sữa POS — Hệ thống tính tiền hóa đơn
    </div>
    """,
    unsafe_allow_html=True
)
