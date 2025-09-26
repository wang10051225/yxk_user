import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QCheckBox,
                             QMessageBox, QLabel, QHeaderView)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QBrush, QColor

# ---------------------- 原爬虫逻辑模块 ----------------------
base_url = "https://www.youxiake.com/mytravel"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': 'pingtaiw=0; yxk_auth=30f0bfHaklud1x0ycEYoQOlu2coLkx1BM3gIp4bjHBlL4c9gFLfKVu3qYFC17ZgQX91NwAjy%2BQ2U9qCYZjSms7dtX3mPjg; access_token=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvd3d3LnlvdXhpYWtlLmNvbVwvbG9naW5cL3ZlcmlmeSIsImlhdCI6MTczMDk3NzExMywiZXhwIjoxNzMwOTgwNzEzLCJuYmYiOjE3MzA5NzcxMTMsImp0aSI6IjUyM2FnaVRITVBmUURxMnAiLCJzdWIiOjEwNTk4MDgxLCJwcnYiOiIwYmMzYTRmYmEzYTExOTllY2MwNjU3ODg4MGEzZWJhZTQwZTJlOWFjIn0.0BMT3YHiVazbsBw9jlK9s0IXdTMBWKsn97yPwNeIzXY; sitecode=1; site=1; gr_user_id=b3782b24-f4d6-479b-911a-a575b18aeed5; a147ace5a8874284_gr_session_id=39672af5-5914-4b87-b50e-9894ef07d516; a147ace5a8874284_gr_last_sent_sid_with_cs1=39672af5-5914-4b87-b50e-9894ef07d516; a147ace5a8874284_gr_last_sent_cs1=10598081; _ga=GA1.2.908587001.1732030045; _gid=GA1.2.1785569538.1732030045; a147ace5a8874284_gr_session_id_sent_vst=39672af5-5914-4b87-b50e-9894ef07d516; sideMuenShop=1; Hm_lvt_4668967a6a0541a2a7cb9bf90df08bdd=1730976938,1732030046; HMACCOUNT=4C9682343569D7D4; PHPSESSID=4161b011b073c6e452d3cfd0b30f4a17; _gat=1; a147ace5a8874284_gr_cs1=10598081; yxk_session=eyJpdiI6InB3Zk9PdEQ0clZQUHFYeDlIeGNSN3c9PSIsInZhbHVlIjoiUGNiaFNhZlZUcG5Yc2JKakxYbjh1dWJhSyszd3RmbkxrajNWdHVXWHFoT3ZxdU1vMURaRWdRbVJId0x1dXRzUVFmTVNIMXJCekZXNVVSY09NU0h4WkJ1QUVQTnVuK081bWk2Smp1SlhYWHlUNHhCRUpKaWE3d0h1OVBhK0RPMmIiLCJtYWMiOiIyNDJjMDNiMDQ3OWRmNWM0YmU3NWJmMDhmMjYwMTNjMWE0Y2Y1MDA4NGNiMzMxNjJiZmQxZDJkODA3YzdhYzViIn0%3D; yxk_last_visit=1732030566; Hm_lpvt_4668967a6a0541a2a7cb9bf90df08bdd=1732030567',
    'Host': 'www.youxiake.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    'Sec-Ch-Ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"'
}


def query_all_user_info():
    """查询所有用户信息"""
    user_list = []
    url = f'{base_url}/tourist'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', class_='m-table')
            if not table:
                return user_list

            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')
                if len(cols) < 9:
                    continue

                user_info = {
                    "m_id": cols[8].find_all('a')[0]['href'].split("id=")[1],
                    "username": cols[0].get_text(strip=True),
                    "sex": cols[1].get_text(strip=True),
                    "m_type": cols[2].get_text(strip=True),
                    "id_number": cols[4].get_text(strip=True),
                    "phone_number": cols[5].get_text(strip=True),
                    "status": "已存在"
                }
                user_list.append(user_info)
    except Exception as e:
        print(f"查询用户异常: {e}")
    return user_list


def del_tourist(user_id):
    """删除单个用户"""
    url = f"https://www.youxiake.com/mytravel/deltourist?id={user_id}"
    try:
        response = requests.get(url, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f"删除用户{user_id}异常: {e}")
        return False


def read_user_info_from_xlsx(file_path):
    """从Excel读取用户信息"""
    user_infos = []
    try:
        df = pd.read_excel(file_path, header=1)
        column_mapping = {}
        for col in df.columns:
            if '姓名' in col:
                column_mapping[col] = '姓名'
            if '手机号' in col:
                column_mapping[col] = '手机号'
            if '身份证' in col:
                column_mapping[col] = '身份证号'
            if '性别' in col:
                column_mapping[col] = '性别'
            if '类型' in col:
                column_mapping[col] = '类型'

        df.rename(columns=column_mapping, inplace=True)
        if '类型' not in df.columns:
            df['类型'] = '成人'

        required_cols = ['姓名', '手机号', '身份证号', '性别', '类型']
        for col in required_cols:
            if col not in df.columns:
                QMessageBox.warning(None, "警告", f"Excel缺少必要列: {col}")
                return []

        for _, row in df.iterrows():
            if pd.isna(row['姓名']) or pd.isna(row['身份证号']):
                continue

            sex_map = {'男': '1', '女': '2'}
            type_map = {'成人': '1', '儿童': '2'}

            user_info = {
                'realname': str(row['姓名']).strip(),
                'cardno': str(row['身份证号']).strip(),
                'phone': str(row['手机号']).strip() if not pd.isna(row['手机号']) else '',
                'sex': sex_map.get(str(row['性别']).strip(), ''),
                'type': type_map.get(str(row['类型']).strip(), '1'),
                'cardtype': '1',
                'cardexp': '',
                'cardexp_hk': '',
                'typepassport': '1',
                'passport_china': '1',
                'passport_out': '3575',
                'birthday': '',
                'mid': '',
                'status': "待添加"
            }
            user_infos.append(user_info)
    except Exception as e:
        QMessageBox.critical(None, "错误", f"读取Excel异常: {str(e)}")
    return user_infos


def add_user(user_info):
    """添加单个用户"""
    url = f'{base_url}/tourist'
    try:
        response = requests.post(url, data=user_info, headers=headers)
        time.sleep(1)  # 避免请求过快
        return response.status_code == 200 and "添加常用游客成功" in response.text
    except Exception as e:
        print(f"添加用户{user_info['realname']}异常: {e}")
        return False


# ---------------------- 线程模块（避免界面卡顿） ----------------------
class WorkerThread(QThread):
    """后台任务线程"""
    signal = pyqtSignal(dict)  # 传递结果信号

    def __init__(self, task_type, data=None):
        super().__init__()
        self.task_type = task_type  # 'add'/'delete'/'query'
        self.data = data  # 任务数据

    def run(self):
        if self.task_type == 'query':
            # 查询用户列表
            user_list = query_all_user_info()
            self.signal.emit({'type': 'query_done', 'data': user_list})

        elif self.task_type == 'add':
            # 添加用户
            success_count = 0
            fail_list = []
            for user in self.data:
                result = add_user(user)
                if result:
                    success_count += 1
                else:
                    fail_list.append(user['realname'])
                self.signal.emit({'type': 'add_progress', 'success': success_count, 'fail': len(fail_list)})
            self.signal.emit({'type': 'add_done', 'success': success_count, 'fail': fail_list})

        elif self.task_type == 'delete':
            # 删除用户
            success_count = 0
            for user_id in self.data:
                if del_tourist(user_id):
                    success_count += 1
                self.signal.emit({'type': 'delete_progress', 'count': success_count})
            self.signal.emit({'type': 'delete_done', 'success': success_count})


# ---------------------- PyQt界面模块 ----------------------
class YouxiakeTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("游侠客游客管理工具")
        self.setGeometry(100, 100, 1200, 600)
        self.excel_user_list = []  # Excel导入的用户列表
        self.current_user_list = []  # 当前显示的用户列表
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 1. 顶部按钮区
        btn_layout = QHBoxLayout()

        self.import_btn = QPushButton("导入Excel")
        self.import_btn.clicked.connect(self.import_excel)
        btn_layout.addWidget(self.import_btn)

        self.add_btn = QPushButton("一键添加选中用户")
        self.add_btn.clicked.connect(self.add_selected_users)
        self.add_btn.setEnabled(False)
        btn_layout.addWidget(self.add_btn)

        self.del_btn = QPushButton("删除选中用户")
        self.del_btn.clicked.connect(self.delete_selected_users)
        btn_layout.addWidget(self.del_btn)

        self.refresh_btn = QPushButton("刷新用户列表")
        self.refresh_btn.clicked.connect(self.refresh_user_list)
        btn_layout.addWidget(self.refresh_btn)

        main_layout.addLayout(btn_layout)

        # 2. 状态显示区
        self.status_label = QLabel("状态: 就绪 | 已导入用户: 0 | 已添加用户: 0 | 待添加用户: 0")
        main_layout.addWidget(self.status_label)

        # 3. 用户列表表格
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["选择", "ID", "姓名", "性别", "类型", "身份证号", "状态"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        # 全选复选框
        self.check_all = QCheckBox()
        self.check_all.stateChanged.connect(self.check_all_changed)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem())
        self.table.setCellWidget(0, 0, self.check_all)

        main_layout.addWidget(self.table)

        # 初始化刷新用户列表
        self.refresh_user_list()

    def update_status(self):
        """更新状态显示"""
        total = len(self.excel_user_list)
        added = len([u for u in self.excel_user_list if u.get('status') == '已添加'])
        pending = len([u for u in self.excel_user_list if u.get('status') == '待添加'])
        self.status_label.setText(f"状态: 就绪 | 已导入用户: {total} | 已添加用户: {added} | 待添加用户: {pending}")

    def update_table(self):
        """更新表格数据"""
        self.table.setRowCount(0)  # 清空表格
        all_users = self.current_user_list + self.excel_user_list

        # 去重（按身份证号）
        unique_users = {}
        for user in all_users:
            id_key = user.get('id_number') or user.get('cardno')
            if id_key and id_key not in unique_users:
                unique_users[id_key] = user

        # 添加到表格
        for row_idx, user in enumerate(unique_users.values()):
            self.table.insertRow(row_idx)

            # 复选框
            check_box = QCheckBox()
            self.table.setCellWidget(row_idx, 0, check_box)

            # ID
            id_item = QTableWidgetItem(user.get('m_id') or '')
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_idx, 1, id_item)

            # 姓名
            name_item = QTableWidgetItem(user.get('username') or user.get('realname') or '')
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_idx, 2, name_item)

            # 性别
            sex_map = {'1': '男', '2': '女'}
            sex = user.get('sex')
            sex_text = sex_map.get(sex, sex) if sex else ''
            sex_item = QTableWidgetItem(sex_text)
            sex_item.setFlags(sex_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_idx, 3, sex_item)

            # 类型
            type_map = {'1': '成人', '2': '儿童'}
            type_val = user.get('m_type') or user.get('type')
            type_text = type_map.get(type_val, type_val) if type_val else ''
            type_item = QTableWidgetItem(type_text)
            type_item.setFlags(type_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_idx, 4, type_item)

            # 身份证号
            id_item = QTableWidgetItem(user.get('id_number') or user.get('cardno') or '')
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_idx, 5, id_item)

            # 状态（带颜色）
            status = user.get('status', '未知')
            status_item = QTableWidgetItem(status)
            status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)

            # 状态颜色：已添加(绿)、待添加(蓝)、已存在(灰)、未知(黑)
            color_map = {
                '已添加': QColor(0, 128, 0),
                '待添加': QColor(0, 0, 255),
                '已存在': QColor(128, 128, 128)
            }
            status_item.setForeground(QBrush(color_map.get(status, QColor(0, 0, 0))))
            self.table.setItem(row_idx, 6, status_item)

        # 重置全选框
        self.check_all.setChecked(False)

    def check_all_changed(self, state):
        """全选/取消全选"""
        for row in range(self.table.rowCount()):
            check_box = self.table.cellWidget(row, 0)
            if check_box:
                check_box.setChecked(state == Qt.Checked)

    def get_selected_users(self):
        """获取选中的用户"""
        selected = []
        for row in range(self.table.rowCount()):
            check_box = self.table.cellWidget(row, 0)
            if check_box and check_box.isChecked():
                # 获取用户数据
                id_val = self.table.item(row, 1).text()
                name = self.table.item(row, 2).text()
                id_card = self.table.item(row, 5).text()
                status = self.table.item(row, 6).text()

                # 匹配Excel用户或现有用户
                user = next((u for u in self.excel_user_list if (u.get('cardno') == id_card)), None)
                if not user:
                    user = next((u for u in self.current_user_list if
                                 (u.get('id_number') == id_card or u.get('m_id') == id_val)), None)

                if user:
                    selected.append(user)
        return selected

    # ---------------------- 功能按钮事件 ----------------------
    def import_excel(self):
        """导入Excel文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", "", "Excel Files (*.xlsx *.xls)")
        if not file_path:
            return

        self.excel_user_list = read_user_info_from_xlsx(file_path)
        self.update_status()
        self.update_table()
        self.add_btn.setEnabled(len(self.excel_user_list) > 0)
        QMessageBox.information(self, "成功", f"导入Excel成功，共{len(self.excel_user_list)}个用户")

    def refresh_user_list(self):
        """刷新用户列表（查询网页数据）"""
        self.status_label.setText("状态: 正在刷新用户列表...")
        self.worker = WorkerThread(task_type='query')
        self.worker.signal.connect(self.handle_worker_result)
        self.worker.start()

    def add_selected_users(self):
        """添加选中的用户"""
        selected_users = [u for u in self.get_selected_users() if u.get('status') == '待添加']
        if not selected_users:
            QMessageBox.warning(self, "警告", "请选择待添加的用户")
            return

        confirm = QMessageBox.question(self, "确认", f"确定要添加选中的{len(selected_users)}个用户吗？",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return

        self.status_label.setText(f"状态: 正在添加{len(selected_users)}个用户...")
        self.worker = WorkerThread(task_type='add', data=selected_users)
        self.worker.signal.connect(self.handle_worker_result)
        self.worker.start()

    def delete_selected_users(self):
        """删除选中的用户"""
        selected_users = self.get_selected_users()
        if not selected_users:
            QMessageBox.warning(self, "警告", "请选择要删除的用户")
            return

        confirm = QMessageBox.question(self, "确认", f"确定要删除选中的{len(selected_users)}个用户吗？",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return

        self.status_label.setText(f"状态: 正在删除{len(selected_users)}个用户...")
        user_ids = [u.get('m_id') for u in selected_users if u.get('m_id')]
        self.worker = WorkerThread(task_type='delete', data=user_ids)
        self.worker.signal.connect(self.handle_worker_result)
        self.worker.start()

    # ---------------------- 线程结果处理 ----------------------
    def handle_worker_result(self, result):
        """处理后台线程结果"""
        if result['type'] == 'query_done':
            # 查询完成
            self.current_user_list = result['data']
            self.update_table()
            self.update_status()
            self.status_label.setText("状态: 就绪 | 已导入用户: 0 | 已添加用户: 0 | 待添加用户: 0")

        elif result['type'] == 'add_done':
            # 添加完成
            success = result['success']
            fail_list = result['fail']

            # 更新状态
            for user in self.excel_user_list:
                if user['realname'] in fail_list:
                    user['status'] = '添加失败'
                elif user['status'] == '待添加':
                    user['status'] = '已添加'

            self.update_table()
            self.update_status()

            msg = f"添加完成！成功{success}个，失败{len(fail_list)}个"
            if fail_list:
                msg += f"\n失败用户: {', '.join(fail_list)}"
            QMessageBox.information(self, "添加结果", msg)

        elif result['type'] == 'delete_done':
            # 删除完成
            success = result['success']
            self.refresh_user_list()  # 刷新列表
            QMessageBox.information(self, "删除结果", f"删除完成！成功删除{success}个用户")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouxiakeTool()
    window.show()
    sys.exit(app.exec_())