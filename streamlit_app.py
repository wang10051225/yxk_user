import streamlit as st
import pandas as pd
import time
from youxiake_tourist import (
    query_all_user_info, 
    add_user, 
    del_tourist, 
    read_user_info_from_xlsx,
    add_all_user,
    del_all_user
)

# 页面配置
st.set_page_config(
    page_title="游侠客游客管理工具",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 标题
st.title("🏔️ 游侠客游客管理工具")
st.markdown("---")

# 侧边栏
st.sidebar.title("📋 操作面板")

# 初始化session state
if 'current_users' not in st.session_state:
    st.session_state.current_users = []
if 'excel_users' not in st.session_state:
    st.session_state.excel_users = []
if 'selected_users' not in st.session_state:
    st.session_state.selected_users = []

# 功能按钮
st.sidebar.markdown("### 🔍 数据查询")
if st.sidebar.button("🔄 刷新用户列表", use_container_width=True):
    with st.spinner("正在查询用户列表..."):
        st.session_state.current_users = query_all_user_info()
    st.success(f"查询完成！找到 {len(st.session_state.current_users)} 个用户")

st.sidebar.markdown("### 📁 文件操作")
uploaded_file = st.sidebar.file_uploader(
    "选择Excel文件", 
    type=['xlsx', 'xls'],
    help="请上传包含游客信息的Excel文件"
)

# 自动读取Excel文件
if uploaded_file:
    try:
        # 保存上传的文件
        with open("temp_upload.xlsx", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 自动读取Excel数据
        with st.spinner("正在读取Excel文件..."):
            st.session_state.excel_users = read_user_info_from_xlsx("temp_upload.xlsx")
        
        st.success(f"✅ Excel读取成功！共 {len(st.session_state.excel_users)} 个用户")
        
        # 显示Excel数据预览
        if st.session_state.excel_users:
            df_preview = pd.DataFrame(st.session_state.excel_users)
            st.sidebar.markdown("### 📊 Excel数据预览")
            st.sidebar.dataframe(df_preview[['realname', 'phone', 'cardno', 'sex', 'type']], 
                               use_container_width=True, height=200)
    except Exception as e:
        st.error(f"❌ 读取Excel失败: {str(e)}")

st.sidebar.markdown("### ⚡ 批量操作")
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("➕ 批量添加", use_container_width=True):
        if st.session_state.excel_users:
            with st.spinner("正在批量添加用户..."):
                success_count = 0
                fail_list = []
                progress_bar = st.progress(0)
                
                for i, user in enumerate(st.session_state.excel_users):
                    if add_user(user):
                        success_count += 1
                    else:
                        fail_list.append(user['realname'])
                    progress_bar.progress((i + 1) / len(st.session_state.excel_users))
                
                # 批量添加完成后自动刷新用户列表
                if success_count > 0:
                    st.success(f"✅ 添加完成！成功: {success_count} 个")
                    # 自动刷新用户列表
                    with st.spinner("正在刷新用户列表..."):
                        st.session_state.current_users = query_all_user_info()
                    st.info("🔄 用户列表已自动刷新")
                if fail_list:
                    st.error(f"❌ 失败用户: {', '.join(fail_list)}")
        else:
            st.warning("⚠️ 请先上传Excel文件")

with col2:
    if st.button("🗑️ 清空所有", use_container_width=True):
        st.session_state.show_clear_all_confirm = True
        st.rerun()

if st.session_state.get('show_clear_all_confirm', False):
    st.sidebar.warning("⚠️ 危险操作！这将删除系统中的所有用户！")
    col_confirm1, col_confirm2 = st.sidebar.columns(2)
    with col_confirm1:
        if st.button("⚠️ 我确认要清空所有用户", type="primary", use_container_width=True):
            with st.spinner("正在清空所有用户..."):
                del_all_user()
            st.success("✅ 所有用户已清空")
            # 刷新用户列表
            with st.spinner("正在刷新用户列表..."):
                st.session_state.current_users = query_all_user_info()
            st.info("🔄 用户列表已自动刷新")
            st.session_state.show_clear_all_confirm = False
            st.rerun()
    with col_confirm2:
        if st.button("❌ 取消", use_container_width=True):
            st.session_state.show_clear_all_confirm = False
            st.rerun()

# 主界面内容
tab1, tab2, tab3 = st.tabs(["📋 用户列表", "➕ 添加用户", "📊 数据对比"])

with tab1:
    st.markdown("### 📋 当前用户列表")
    
    if st.session_state.current_users:
        # 转换为DataFrame显示
        df = pd.DataFrame(st.session_state.current_users)
        
        # 初始化选中用户列表
        if 'selected_users' not in st.session_state:
            st.session_state.selected_users = []
        
        # 操作面板
        st.markdown("### 🛠️ 操作面板")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 刷新列表", use_container_width=True):
                st.session_state.current_users = query_all_user_info()
                st.session_state.selected_users = []
                st.rerun()
        
        with col2:
            if st.button("📋 全选", key="select_all_btn", use_container_width=True):
                st.session_state.selected_users = list(df.index)
                st.rerun()
        
        with col3:
            if st.button("🗑️ 清空选择", key="clear_all_btn", use_container_width=True):
                st.session_state.selected_users = []
                st.rerun()
        
        # 显示用户统计和选择信息
        total_users = len(df)
        selected_count = len(st.session_state.selected_users)
        st.markdown(f"### 📊 统计信息")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("总用户数", total_users)
        with col2:
            st.metric("已选择", selected_count)
        
        # 显示用户列表（使用表格形式，更整齐）
        st.markdown("### 📋 用户列表详情")
        
        # 创建表格数据
        table_data = []
        for i, user in enumerate(df.iterrows()):
            idx, row = user
            is_selected = idx in st.session_state.selected_users
            
            table_data.append({
                "序号": f"{i+1}",
                "选择": "✅" if is_selected else "⬜",
                "姓名": row['username'],
                "性别": row['sex'],
                "类型": row['m_type'],
                "身份证号": row['id_number'],
                "手机号": row['phone_number']
            })
        
        # 显示表格
        if table_data:
            df_display = pd.DataFrame(table_data)
            
            # 添加复选框列
            for i, row in df_display.iterrows():
                idx = df.index[i]
                col_check, col_info = st.columns([0.5, 15])
                
                with col_check:
                    is_selected = st.checkbox("", key=f"user_{idx}", value=idx in st.session_state.selected_users, label_visibility="collapsed")
                    if is_selected and idx not in st.session_state.selected_users:
                        st.session_state.selected_users.append(idx)
                    elif not is_selected and idx in st.session_state.selected_users:
                        st.session_state.selected_users.remove(idx)
                
                with col_info:
                    # 使用等宽字体和对齐格式
                    st.markdown(f"**{row['序号']}.** **{row['姓名']}** | {row['性别']} | {row['类型']} | {row['身份证号']} | {row['手机号']}")
        
        # 显示选中用户操作按钮
        selected_count = len(st.session_state.selected_users)
        if selected_count > 0:
            st.markdown("### 🎯 选中用户操作")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"🗑️ 删除选中的 {selected_count} 个用户", type="primary", use_container_width=True):
                    with st.spinner(f"正在删除 {selected_count} 个用户..."):
                        success_count = 0
                        for idx in st.session_state.selected_users:
                            user_id = df.iloc[idx]['m_id']
                            if del_tourist(user_id):
                                success_count += 1
                        st.success(f"✅ 删除完成！成功删除 {success_count} 个用户")
                        # 刷新列表
                        st.session_state.current_users = query_all_user_info()
                        st.session_state.selected_users = []
                        st.rerun()
            
            with col2:
                if st.button("📋 清除选择", use_container_width=True):
                    st.session_state.selected_users = []
                    st.rerun()
    else:
        st.info("暂无用户数据，请点击侧边栏的'刷新用户列表'按钮")

with tab2:
    st.markdown("### ➕ 手动添加用户")
    
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("姓名 *", placeholder="请输入姓名")
            phone = st.text_input("手机号", placeholder="请输入手机号")
            id_card = st.text_input("身份证号 *", placeholder="请输入身份证号")
        
        with col2:
            sex = st.selectbox("性别", ["男", "女"])
            user_type = st.selectbox("类型", ["成人", "儿童"])
        
        submitted = st.form_submit_button("➕ 添加用户", type="primary")
        
        if submitted:
            if not name or not id_card:
                st.error("姓名和身份证号为必填项！")
            else:
                # 构建用户信息
                user_info = {
                    'realname': name,
                    'phone': phone,
                    'cardno': id_card,
                    'sex': '1' if sex == '男' else '2',
                    'type': '1' if user_type == '成人' else '2',
                    'cardtype': '1',
                    'cardexp': '',
                    'cardexp_hk': '',
                    'typepassport': '1',
                    'passport_china': '1',
                    'passport_out': '3575',
                    'birthday': '',
                    'mid': ''
                }
                
                with st.spinner("正在添加用户..."):
                    if add_user(user_info):
                        st.success(f"用户 {name} 添加成功！")
                        # 刷新用户列表
                        st.session_state.current_users = query_all_user_info()
                    else:
                        st.error(f"用户 {name} 添加失败！")

with tab3:
    st.markdown("### 📊 数据对比分析")
    
    if st.session_state.current_users and st.session_state.excel_users:
        st.markdown("**对比Excel文件与当前系统中的用户数据**")
        
        # 当前系统用户
        current_df = pd.DataFrame(st.session_state.current_users)
        current_df['来源'] = '系统'
        
        # Excel用户
        excel_df = pd.DataFrame(st.session_state.excel_users)
        excel_df['来源'] = 'Excel'
        excel_df['username'] = excel_df['realname']
        excel_df['id_number'] = excel_df['cardno']
        excel_df['phone_number'] = excel_df['phone']
        
        # 合并数据
        comparison_data = []
        
        # 检查Excel中的用户在系统中是否存在
        for _, excel_user in excel_df.iterrows():
            found = False
            for _, current_user in current_df.iterrows():
                if excel_user['cardno'] == current_user['id_number']:
                    comparison_data.append({
                        '姓名': excel_user['realname'],
                        '身份证号': excel_user['cardno'],
                        '手机号': excel_user['phone'],
                        '性别': excel_user['sex'],
                        '类型': excel_user['type'],
                        '状态': '✅ 已存在',
                        '系统ID': current_user['m_id']
                    })
                    found = True
                    break
            
            if not found:
                comparison_data.append({
                    '姓名': excel_user['realname'],
                    '身份证号': excel_user['cardno'],
                    '手机号': excel_user['phone'],
                    '性别': excel_user['sex'],
                    '类型': excel_user['type'],
                    '状态': '❌ 未添加',
                    '系统ID': ''
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # 统计信息
        total_users = len(comparison_df)
        added_users = len(comparison_df[comparison_df['状态'] == '✅ 已存在'])
        pending_users = len(comparison_df[comparison_df['状态'] == '❌ 未添加'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总用户数", total_users)
        with col2:
            st.metric("已添加", added_users, delta=f"{added_users/total_users*100:.1f}%")
        with col3:
            st.metric("待添加", pending_users, delta=f"{pending_users/total_users*100:.1f}%")
        
        # 显示对比结果
        st.dataframe(comparison_df, use_container_width=True, height=400)
        
        # 下载对比结果
        csv = comparison_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 下载对比结果",
            data=csv,
            file_name=f"用户对比结果_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
    elif st.session_state.excel_users:
        st.warning("请先刷新用户列表以进行对比")
    else:
        st.info("请先上传Excel文件并刷新用户列表")

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🏔️ 游侠客游客管理工具 | 基于Streamlit开发</p>
</div>
""", unsafe_allow_html=True)


