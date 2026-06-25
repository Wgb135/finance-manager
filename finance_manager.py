import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

st.set_page_config(
    page_title="财务管理系统",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_session_state():
    if 'transactions' not in st.session_state:
        st.session_state.transactions = []
    if 'budgets' not in st.session_state:
        st.session_state.budgets = {}
    if 'currency' not in st.session_state:
        st.session_state.currency = 'CNY'
    # 1. 删除主题相关的session_state初始化，直接固定为light主题
    if 'show_success' not in st.session_state:
        st.session_state.show_success = False
    if 'success_message' not in st.session_state:
        st.session_state.success_message = ''
    if 'sample_data_loaded' not in st.session_state:
        st.session_state.sample_data_loaded = False

def get_sample_data():
    if not st.session_state.sample_data_loaded:
        sample_transactions = [
            {'date': '2026-01-01', 'type': 'income', 'category': '工资', 'amount': 15000, 'description': '1月工资'},
            {'date': '2026-01-05', 'type': 'expense', 'category': '餐饮', 'amount': 500, 'description': '日常餐饮'},
            {'date': '2026-01-10', 'type': 'expense', 'category': '交通', 'amount': 300, 'description': '地铁通勤'},
            {'date': '2026-01-15', 'type': 'expense', 'category': '购物', 'amount': 2000, 'description': '日用品'},
            {'date': '2026-01-20', 'type': 'income', 'category': '奖金', 'amount': 5000, 'description': '项目奖金'},
            {'date': '2026-01-25', 'type': 'expense', 'category': '娱乐', 'amount': 800, 'description': '电影和聚餐'},
            {'date': '2026-02-01', 'type': 'income', 'category': '工资', 'amount': 15000, 'description': '2月工资'},
            {'date': '2026-02-05', 'type': 'expense', 'category': '餐饮', 'amount': 600, 'description': '日常餐饮'},
            {'date': '2026-02-10', 'type': 'expense', 'category': '交通', 'amount': 350, 'description': '地铁通勤'},
            {'date': '2026-02-15', 'type': 'expense', 'category': '购物', 'amount': 1500, 'description': '日用品'},
            {'date': '2026-02-20', 'type': 'expense', 'category': '医疗', 'amount': 1200, 'description': '体检'},
            {'date': '2026-02-25', 'type': 'expense', 'category': '娱乐', 'amount': 1000, 'description': '周末活动'},
            {'date': '2026-03-01', 'type': 'income', 'category': '工资', 'amount': 15000, 'description': '3月工资'},
            {'date': '2026-03-05', 'type': 'expense', 'category': '餐饮', 'amount': 550, 'description': '日常餐饮'},
            {'date': '2026-03-10', 'type': 'expense', 'category': '交通', 'amount': 320, 'description': '地铁通勤'},
            {'date': '2026-03-15', 'type': 'expense', 'category': '购物', 'amount': 1800, 'description': '日用品'},
        ]
        st.session_state.transactions = sample_transactions
        st.session_state.budgets = {
            '餐饮': 2000,
            '交通': 1000,
            '购物': 3000,
            '娱乐': 1500,
            '医疗': 2000
        }
        st.session_state.sample_data_loaded = True

# 2. 简化主题颜色函数，仅保留浅色主题
def get_theme_colors():
    return {
        'bg': '#ffffff',
        'card_bg': '#f8f9fa',
        'text': '#1f2937',
        'primary': '#3b82f6',
        'success': '#10b981',
        'warning': '#f59e0b',
        'danger': '#ef4444',
        'border': '#e5e7eb'
    }

def apply_theme():
    colors = get_theme_colors()
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {colors['bg']};
    }}
    .metric-card {{
        background-color: {colors['card_bg']};
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid {colors['border']};
    }}
    .stMetric {{
        background-color: {colors['card_bg']};
        padding: 15px;
        border-radius: 10px;
        border: 1px solid {colors['border']};
    }}
    .stDataFrame {{
        background-color: {colors['card_bg']};
    }}
    .css-1d391kg {{
        background-color: {colors['card_bg']};
    }}
    .stSelectbox > div > div {{
        background-color: {colors['card_bg']};
    }}
    .stTextInput > div > div > input {{
        background-color: {colors['card_bg']};
        color: {colors['text']};
    }}
    .stNumberInput > div > div > input {{
        background-color: {colors['card_bg']};
        color: {colors['text']};
    }}
    .stDateInput > div > div > input {{
        background-color: {colors['card_bg']};
        color: {colors['text']};
    }}
    .stTextArea > div > div > textarea {{
        background-color: {colors['card_bg']};
        color: {colors['text']};
    }}
    </style>
    """, unsafe_allow_html=True)

def show_success_message(message):
    st.session_state.show_success = True
    st.session_state.success_message = message
    st.success(message)
    st.session_state.show_success = False

def calculate_metrics():
    df = pd.DataFrame(st.session_state.transactions)
    if df.empty:
        return 0, 0, 0, 0, 0, {}
    
    df['date'] = pd.to_datetime(df['date'])
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    month_df = df[(df['date'].dt.month == current_month) & (df['date'].dt.year == current_year)]
    
    total_income = df[df['type'] == 'income']['amount'].sum()
    total_expense = df[df['type'] == 'expense']['amount'].sum()
    balance = total_income - total_expense
    
    month_income = month_df[month_df['type'] == 'income']['amount'].sum()
    month_expense = month_df[month_df['type'] == 'expense']['amount'].sum()
    
    expense_by_category = df[df['type'] == 'expense'].groupby('category')['amount'].sum().to_dict()
    
    return total_income, total_expense, balance, month_income, month_expense, expense_by_category

def render_metric_card(title, value, delta=None, color='blue'):
    colors = get_theme_colors()
    color_map = {
        'blue': colors['primary'],
        'green': colors['success'],
        'red': colors['danger'],
        'yellow': colors['warning']
    }
    
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid {color_map[color]};">
        <h4 style="margin: 0; color: {colors['text']}; font-size: 14px;">{title}</h4>
        <h2 style="margin: 10px 0 0 0; color: {colors['text']}; font-size: 28px;">{value}</h2>
        {f'<p style="margin: 5px 0 0 0; color: {colors["success"]}; font-size: 14px;">{delta}</p>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)

def render_overview_page():
    st.header("📊 财务总览")
    
    total_income, total_expense, balance, month_income, month_expense, expense_by_category = calculate_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card("总收入", f"¥{total_income:,.2f}", color='green')
    
    with col2:
        render_metric_card("总支出", f"¥{total_expense:,.2f}", color='red')
    
    with col3:
        render_metric_card("净资产", f"¥{balance:,.2f}", color='blue')
    
    with col4:
        render_metric_card("本月支出", f"¥{month_expense:,.2f}", color='yellow')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 收支趋势")
        df = pd.DataFrame(st.session_state.transactions)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.to_period('M')
            
            monthly_data = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
            monthly_data.index = monthly_data.index.astype(str)
            
            fig = go.Figure()
            if 'income' in monthly_data.columns:
                fig.add_trace(go.Scatter(
                    x=monthly_data.index,
                    y=monthly_data['income'],
                    name='收入',
                    line=dict(color='#10b981', width=3),
                    fill='tozeroy'
                ))
            if 'expense' in monthly_data.columns:
                fig.add_trace(go.Scatter(
                    x=monthly_data.index,
                    y=monthly_data['expense'],
                    name='支出',
                    line=dict(color='#ef4444', width=3),
                    fill='tozeroy'
                ))
            
            fig.update_layout(
                template='plotly_white',
                hovermode='x unified',
                height=400,
                margin=dict(l=0, r=0, t=20, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🥧 支出分类")
        if expense_by_category:
            fig = px.pie(
                values=list(expense_by_category.values()),
                names=list(expense_by_category.keys()),
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                height=400,
                margin=dict(l=0, r=0, t=20, b=0),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("暂无支出数据")

def render_transactions_page():
    st.header("💰 收支明细")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("添加记录")
        with st.form("add_transaction", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("日期", datetime.now())
            with col2:
                trans_type = st.selectbox("类型", ["收入", "支出"])
            
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("分类", ["工资", "奖金", "餐饮", "交通", "购物", "娱乐", "医疗", "其他"])
            with col2:
                amount = st.number_input("金额", min_value=0.01, step=0.01)
            
            description = st.text_input("备注")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("添加记录", use_container_width=True)
            with col2:
                if st.form_submit_button("重置", use_container_width=True):
                    st.rerun()
            
            if submitted:
                new_transaction = {
                    'date': date.strftime('%Y-%m-%d'),
                    'type': 'income' if trans_type == '收入' else 'expense',
                    'category': category,
                    'amount': amount,
                    'description': description
                }
                st.session_state.transactions.append(new_transaction)
                show_success_message("记录添加成功！")
    
    with col2:
        st.subheader("筛选")
        filter_type = st.selectbox("类型筛选", ["全部", "收入", "支出"])
        filter_category = st.selectbox("分类筛选", ["全部"] + ["工资", "奖金", "餐饮", "交通", "购物", "娱乐", "医疗", "其他"])
        
        start_date = st.date_input("开始日期", datetime.now() - timedelta(days=30))
        end_date = st.date_input("结束日期", datetime.now())
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("交易记录")
    
    df = pd.DataFrame(st.session_state.transactions)
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        
        if filter_type != "全部":
            df = df[df['type'] == ('income' if filter_type == '收入' else 'expense')]
        
        if filter_category != "全部":
            df = df[df['category'] == filter_category]
        
        df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
        
        df = df.sort_values('date', ascending=False)
        
        if not df.empty:
            display_df = df.copy()
            display_df['type'] = display_df['type'].map({'income': '收入', 'expense': '支出'})
            display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
            display_df['amount'] = display_df['amount'].apply(lambda x: f"¥{x:,.2f}")
            
            for idx, row in display_df.iterrows():
                with st.expander(f"📅 {row['date']} - {row['category']} - {row['amount']}", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    col1.write(f"**类型**: {row['type']}")
                    col2.write(f"**分类**: {row['category']}")
                    col3.write(f"**金额**: {row['amount']}")
                    st.write(f"**备注**: {row['description']}")
                    
                    if st.button(f"删除", key=f"delete_{idx}", type="secondary"):
                        st.session_state.transactions.pop(idx)
                        show_success_message("记录删除成功！")
                        st.rerun()
        else:
            st.info("没有符合条件的记录")
    else:
        st.info("暂无交易记录")

def render_budget_page():
    st.header("📋 预算管理")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("设置预算")
        with st.form("set_budget", clear_on_submit=True):
            category = st.selectbox("分类", ["餐饮", "交通", "购物", "娱乐", "医疗", "其他"])
            amount = st.number_input("预算金额", min_value=0.01, step=100.0)
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("设置预算", use_container_width=True)
            with col2:
                if st.form_submit_button("重置", use_container_width=True):
                    st.rerun()
            
            if submitted:
                st.session_state.budgets[category] = amount
                show_success_message(f"{category}预算设置为 ¥{amount:,.2f}")
    
    with col2:
        st.subheader("预算概览")
        total_budget = sum(st.session_state.budgets.values())
        st.metric("总预算", f"¥{total_budget:,.2f}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("预算执行情况")
    
    if st.session_state.budgets:
        df = pd.DataFrame(st.session_state.transactions)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            month_df = df[(df['date'].dt.month == current_month) & (df['date'].dt.year == current_year)]
            month_expenses = month_df[month_df['type'] == 'expense'].groupby('category')['amount'].sum().to_dict()
            
            for category, budget in st.session_state.budgets.items():
                spent = month_expenses.get(category, 0)
                remaining = budget - spent
                percentage = (spent / budget * 100) if budget > 0 else 0
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{category}**")
                    progress_color = 'green' if percentage < 50 else 'yellow' if percentage < 80 else 'red'
                    st.progress(min(percentage / 100, 1.0))
                with col2:
                    st.write(f"¥{spent:,.2f} / ¥{budget:,.2f}")
                    st.write(f"剩余: ¥{remaining:,.2f}")
                
                st.markdown("---")
        else:
            st.info("暂无支出数据")
    else:
        st.info("请先设置预算")

def render_analysis_page():
    st.header("📊 数据分析")
    
    df = pd.DataFrame(st.session_state.transactions)
    if df.empty:
        st.info("暂无数据可供分析")
        return
    
    df['date'] = pd.to_datetime(df['date'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("月度收支对比")
        monthly_data = df.groupby([df['date'].dt.to_period('M'), 'type'])['amount'].sum().unstack(fill_value=0)
        monthly_data.index = monthly_data.index.astype(str)
        
        fig = go.Figure()
        if 'income' in monthly_data.columns:
            fig.add_trace(go.Bar(
                name='收入',
                x=monthly_data.index,
                y=monthly_data['income'],
                marker_color='#10b981'
            ))
        if 'expense' in monthly_data.columns:
            fig.add_trace(go.Bar(
                name='支出',
                x=monthly_data.index,
                y=monthly_data['expense'],
                marker_color='#ef4444'
            ))
        
        fig.update_layout(
            barmode='group',
            template='plotly_white',
            height=400,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("支出分类排行")
        expense_df = df[df['type'] == 'expense']
        if not expense_df.empty:
            category_expenses = expense_df.groupby('category')['amount'].sum().sort_values(ascending=True)
            
            fig = go.Figure(go.Bar(
                x=category_expenses.values,
                y=category_expenses.index,
                orientation='h',
                marker_color='#3b82f6'
            ))
            fig.update_layout(
                template='plotly_white',
                height=400,
                margin=dict(l=0, r=0, t=20, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("财务健康度")
        total_income = df[df['type'] == 'income']['amount'].sum()
        total_expense = df[df['type'] == 'expense']['amount'].sum()
        savings_rate = ((total_income - total_expense) / total_income * 100) if total_income > 0 else 0
        
        health_score = min(100, max(0, savings_rate))
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health_score,
            title={'text': "储蓄率 (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#3b82f6"},
                'steps': [
                    {'range': [0, 30], 'color': "#fee2e2"},
                    {'range': [30, 50], 'color': "#fef3c7"},
                    {'range': [50, 70], 'color': "#d1fae5"},
                    {'range': [70, 100], 'color': "#10b981"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        if health_score >= 70:
            st.success("🎉 财务状况优秀！")
        elif health_score >= 50:
            st.info("👍 财务状况良好")
        elif health_score >= 30:
            st.warning("⚠️ 需要注意支出")
        else:
            st.error("🚨 建议重新规划预算")
    
    with col2:
        st.subheader("统计摘要")
        st.metric("总交易数", len(df))
        st.metric("收入笔数", len(df[df['type'] == 'income']))
        st.metric("支出笔数", len(df[df['type'] == 'expense']))
        
        avg_income = df[df['type'] == 'income']['amount'].mean() if len(df[df['type'] == 'income']) > 0 else 0
        avg_expense = df[df['type'] == 'expense']['amount'].mean() if len(df[df['type'] == 'expense']) > 0 else 0
        
        st.metric("平均收入", f"¥{avg_income:,.2f}")
        st.metric("平均支出", f"¥{avg_expense:,.2f}")

def render_settings():
    st.sidebar.header("⚙️ 设置")
    
    # 3. 删除主题设置相关的侧边栏选项
    st.sidebar.subheader("货币设置")
    currency = st.sidebar.selectbox(
        "货币单位",
        ["CNY", "USD", "EUR", "GBP"],
        index=["CNY", "USD", "EUR", "GBP"].index(st.session_state.currency)
    )
    st.session_state.currency = currency
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("数据管理")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("导出数据", use_container_width=True):
            data = {
                'transactions': st.session_state.transactions,
                'budgets': st.session_state.budgets
            }
            st.sidebar.download_button(
                label="下载JSON",
                data=json.dumps(data, ensure_ascii=False, indent=2),
                file_name=f"finance_data_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    with col2:
        if st.button("清空数据", use_container_width=True, type="secondary"):
            if st.sidebar.checkbox("确认清空所有数据", key="confirm_clear"):
                st.session_state.transactions = []
                st.session_state.budgets = {}
                show_success_message("数据已清空")
                st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("关于")
    st.sidebar.info("💰 财务管理系统 v1.0\n\n📅 版本: 2026.03.18\n\n🔒 所有数据仅保存在本地浏览器会话中")

def main():
    init_session_state()
    apply_theme()
    
    with st.sidebar:
        st.title("💰 财务管理")
        st.markdown("---")
        
        page = st.radio(
            "导航",
            ["📊 总览", "💰 收支明细", "📋 预算管理", "📊 数据分析"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("📥 加载示例数据", use_container_width=True):
            get_sample_data()
            show_success_message("示例数据加载成功！")
            st.rerun()
        
        if st.button("🔄 刷新页面", use_container_width=True):
            st.rerun()
    
    render_settings()
    
    page_map = {
        "📊 总览": render_overview_page,
        "💰 收支明细": render_transactions_page,
        "📋 预算管理": render_budget_page,
        "📊 数据分析": render_analysis_page
    }
    
    page_map[page]()

if __name__ == "__main__":
    main()