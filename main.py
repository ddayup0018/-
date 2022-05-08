import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mbox
import sqlite3
import datetime
import webbrowser
from sqlite3 import OperationalError
import os

# def conn(func):
#     def inner():
#         conn = sqlite3.connect('goods.db')
#         cur = conn.cursor()
#         print(1)
#         func()
#         # cur.execute(sql, data)
#         # conn.commit()
#         cur.close()
#         print(2)
#         conn.close()
#     return inner

def win():
    global window,text_my
    window = tk.Tk()
    window.title('个人型货物管理系统')
    window.geometry('1280x600')

    # 菜单模块
    menu_top=tk.Menu(window)
    window.config(menu=menu_top)

    top_admin=tk.Menu(menu_top,tearoff=0)
    menu_top.add_cascade(label='管理员',menu=top_admin)
    top_admin.add_command(label='清空数据',command=menu_admin)

    top_help = tk.Menu(menu_top, tearoff=0)
    menu_top.add_cascade(label='使用说明', menu=top_help)
    top_help.add_command(label='阅读使用说明', command=menu_read)
    top_help.add_command(label='下载sqlite3数据库', command=menu_downloadsqlite3)

    # 功能模块
    tk.Label(window, text='功能模块',width=30).grid(row=0,column=0)
    tk.Label(window, text='信息模块',width=30).grid(row=1,column=0)
    btn_house=tk.Button(window,text='库存信息',command=goods_info,height=2,width=20)
    btn_house.grid(row=2,column=0)
    btn_insert_info = tk.Button(window, text='入库信息', command=insert_info, height=2, width=20)
    btn_insert_info.grid(row=3, column=0)
    btn_out_info = tk.Button(window, text='出库信息', command=out_info, height=2, width=20)
    btn_out_info.grid(row=4, column=0)

    tk.Label(window, text='管理模块', width=30).grid(row=5, column=0)
    btn_goods = tk.Button(window, text='货物管理', command=goods_manager, height=2, width=20)
    btn_goods.grid(row=6, column=0)
    btn_insert = tk.Button(window, text='入库管理', command=insert_manager,height=2,width=20)
    btn_insert.grid(row=7,column=0)
    btn_out = tk.Button(window, text='出库管理', command=out_manager, height=2, width=20)
    btn_out.grid(row=8,column=0)

    tk.Label(window, text='借还模块', width=30).grid(row=9, column=0)
    tk.Button(window, text='借还信息', command=bor_info, height=2, width=20).grid(row=10, column=0)
    tk.Button(window, text='借货', command=bor_manager, height=2, width=20).grid(row=11, column=0)
    tk.Button(window, text='归还', command=lend_manager, height=2, width=20).grid(row=12, column=0)

    # 默认显示信息
    goods_info()

    window.mainloop()

def goods_info():
    tk.Label(window, text='库存信息', width=60).grid(row=0, column=1)
    goods_show = ttk.Treeview(window, show='headings', columns=('货物编码','货物型号','货物名称', '单位','库存数量'))
    # 表头设置
    goods_show.heading('货物编码', text='货物编码')
    goods_show.heading('货物型号', text='货物型号')
    goods_show.heading('货物名称', text='货物名称')
    goods_show.heading('单位', text='单位')
    goods_show.heading('库存数量', text='库存数量')

    # 列设置
    goods_show.column('货物编码', anchor='center', width=200)
    goods_show.column('货物型号', anchor='center', width=200)
    goods_show.column('货物名称', anchor='center', width=200)
    goods_show.column('单位', anchor='center', width=200)
    goods_show.column('库存数量', anchor='center', width=200)

    # 数据库操作
    conn = sqlite3.connect('goods.db')
    cur = conn.cursor()
    try:
        sql = "select * from goods_table"
        cur.execute(sql)
        rows=cur.fetchall()
        for row in rows:
            goods_show.insert('',tk.END,values=row)
        conn.commit()
    except OperationalError as m:
        if str(m)=='no such table: goods_table':
            sqlite_create()
    finally:
        cur.close()
        conn.close()

    goods_show.grid(row=1, column=1, rowspan=8)
    # insert_show.grid_forget()
    # out_show.grid_forget()

def insert_info():
    tk.Label(window, text='入库信息', width=60).grid(row=0, column=1)
    insert_show = ttk.Treeview(window, show='headings', columns=('序号','货物编码', '货物型号','货物名称' , '单位','入库数量',
                                                               '办理人','货物来源','入库时间'))
    # 表头设置
    insert_show.heading('序号', text='序号')
    insert_show.heading('货物编码', text='货物编码')
    insert_show.heading('货物型号', text='货物型号')
    insert_show.heading('货物名称', text='货物名称')
    insert_show.heading('单位', text='单位')
    insert_show.heading('入库数量', text='入库数量')
    insert_show.heading('办理人', text='办理人')
    insert_show.heading('货物来源', text='货物来源')
    insert_show.heading('入库时间', text='入库时间')
    # 列设置
    insert_show.column('序号', anchor='center', width=100)
    insert_show.column('货物编码', anchor='center', width=100)
    insert_show.column('货物型号', anchor='center', width=100)
    insert_show.column('货物名称', anchor='center', width=100)
    insert_show.column('单位', anchor='center', width=100)
    insert_show.column('入库数量', anchor='center', width=100)
    insert_show.column('办理人', anchor='center', width=100)
    insert_show.column('货物来源', anchor='center', width=200)
    insert_show.column('入库时间', anchor='center', width=100)

    # 数据库操作
    conn = sqlite3.connect('goods.db')
    cur = conn.cursor()
    sql = "select * from insert_table"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        insert_show.insert('', tk.END, values=row)
    conn.commit()
    cur.close()
    conn.close()

    insert_show.grid(row=1, column=1, rowspan=8)
    # goods_show.grid_forget()
    # out_show.grid_forget()

def out_info():
    tk.Label(window, text='出库信息', width=60).grid(row=0, column=1)
    out_show = ttk.Treeview(window, show='headings', columns=('序号','货物编码', '货物型号', '货物名称', '单位','出库数量',
                                                               '办理人', '领用人','领用事由', '出库时间'))
    # 表头设置
    out_show.heading('序号', text='序号')
    out_show.heading('货物编码', text='货物编码')
    out_show.heading('货物型号', text='货物型号')
    out_show.heading('货物名称', text='货物名称')
    out_show.heading('单位', text='单位')
    out_show.heading('出库数量', text='出库数量')
    out_show.heading('办理人', text='办理人')
    out_show.heading('领用人', text='领用人')
    out_show.heading('领用事由', text='领用事由')
    out_show.heading('出库时间', text='出库时间')
    # 列设置
    out_show.column('序号', anchor='center', width=100)
    out_show.column('货物编码', anchor='center', width=100)
    out_show.column('货物型号', anchor='center', width=100)
    out_show.column('货物名称', anchor='center', width=100)
    out_show.column('单位', anchor='center', width=100)
    out_show.column('出库数量', anchor='center', width=100)
    out_show.column('办理人', anchor='center', width=100)
    out_show.column('领用人', anchor='center', width=100)
    out_show.column('领用事由', anchor='center', width=100)
    out_show.column('出库时间', anchor='center', width=100)

    # 数据库操作
    conn = sqlite3.connect('goods.db')
    cur = conn.cursor()
    sql = "select * from out_table"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        out_show.insert('', tk.END, values=row)
    conn.commit()
    cur.close()
    conn.close()

    # goods_show.grid_forget()
    # insert_show.grid_forget()
    out_show.grid(row=1, column=1, rowspan=8)

def bor_info():
    tk.Label(window, text='借还信息', width=60).grid(row=0, column=1)
    bor_show = ttk.Treeview(window, show='headings', columns=('借货编码','货物编码', '货物型号', '货物名称', '单位','借货数量',
                                                               '办理人', '借货人','借货事由', '借货时间','处理结果','归还编码'))
    # 表头设置
    bor_show.heading('借货编码', text='借货编码')
    bor_show.heading('货物编码', text='货物编码')
    bor_show.heading('货物型号', text='货物型号')
    bor_show.heading('货物名称', text='货物名称')
    bor_show.heading('单位', text='单位')
    bor_show.heading('借货数量', text='借货数量')
    bor_show.heading('办理人', text='办理人')
    bor_show.heading('借货人', text='借货人')
    bor_show.heading('借货事由', text='借货事由')
    bor_show.heading('借货时间', text='借货时间')
    bor_show.heading('处理结果', text='处理结果')
    bor_show.heading('归还编码', text='归还编码')
    # 列设置
    bor_show.column('借货编码', anchor='center', width=100)
    bor_show.column('货物编码', anchor='center', width=75)
    bor_show.column('货物型号', anchor='center', width=75)
    bor_show.column('货物名称', anchor='center', width=75)
    bor_show.column('单位', anchor='center', width=50)
    bor_show.column('借货数量', anchor='center', width=75)
    bor_show.column('办理人', anchor='center', width=75)
    bor_show.column('借货人', anchor='center', width=75)
    bor_show.column('借货事由', anchor='center', width=100)
    bor_show.column('借货时间', anchor='center', width=100)
    bor_show.column('处理结果', anchor='center', width=100)
    bor_show.column('归还编码', anchor='center', width=100)

    # 数据库操作
    conn = sqlite3.connect('goods.db')
    cur = conn.cursor()
    sql = "select * from bor_table"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        bor_show.insert('', tk.END, values=row)
    conn.commit()
    cur.close()
    conn.close()

    # goods_show.grid_forget()
    # insert_show.grid_forget()
    bor_show.grid(row=1, column=1, rowspan=8)

class goods_manager:
    def __init__(self):
        self.goods = tk.Toplevel()
        self.goods.title('货物录入')
        self.goods.geometry('400x400')
        self.hwxh=tk.StringVar()
        self.hwmc=tk.StringVar()
        self.dw=tk.StringVar()
        self.openpage()

    def openpage(self):
        tk.Label(self.goods, text='货物编码', height=3, width=20).grid(row=0, column=0)
        tk.Entry(self.goods, width=30,state='disable').grid(row=0, column=1)

        tk.Label(self.goods, text='货物型号', height=3, width=20).grid(row=1, column=0)
        tk.Entry(self.goods, textvariable=self.hwxh, width=30).grid(row=1, column=1)

        tk.Label(self.goods, text='货物名称', height=3, width=20).grid(row=2, column=0)
        tk.Entry(self.goods, textvariable=self.hwmc, width=30).grid(row=2, column=1)

        tk.Label(self.goods, text='单位', height=3, width=20).grid(row=3, column=0)
        tk.Entry(self.goods, textvariable=self.dw, width=30).grid(row=3, column=1)

        tk.Button(self.goods, text='提交', command=self.goods_sub, height=2, width=20).grid(row=4, column=0)
        tk.Button(self.goods, text='返回', command=self.goods_cal, height=2, width=20).grid(row=4, column=1)

    def goods_sub(self):
        if self.hwxh.get() != '' and self.hwmc.get() != '':
            self.data = (self.hwxh.get(), self.hwmc.get(), self.dw.get())
            # print(self.data)
            self.sql = "insert into goods_table(hwxh,hwmc,dw) values (?,?,?)"
            # print(self.sql)

            # 数据库操作
            conn = sqlite3.connect('goods.db')
            cur = conn.cursor()
            cur.execute(self.sql, self.data)
            conn.commit()
            cur.close()
            conn.close()

            mbox.showinfo('提示信息', '录入成功!')
            self.goods.destroy()
            goods_info()
        else:
            mbox.showerror('错误信息', '货物型号和货物名称不能为空!')
            return

    def goods_cal(self):
        self.goods.destroy()

class insert_manager:
    def __init__(self):
        self.insert = tk.Toplevel()
        self.insert.title('入库管理')
        self.insert.geometry('400x600')

        self.hwbm=tk.IntVar()
        self.hwxh = tk.StringVar()
        self.hwmc= tk.StringVar()
        self.dw = tk.StringVar()
        self.rksl= tk.IntVar()
        self.blr= tk.StringVar()
        self.hwly= tk.StringVar()

        self.openpage()

    def openpage(self):
        tk.Label(self.insert, text='货物编码', height=3, width=20).grid(row=0, column=0)
        tk.Entry(self.insert, textvariable=self.hwbm, width=30).grid(row=0, column=1)

        tk.Label(self.insert, text='货物型号', height=3, width=20).grid(row=1, column=0)
        tk.Entry(self.insert, textvariable=self.hwxh, width=30,state='disable').grid(row=1, column=1)

        tk.Label(self.insert,text='货物名称',height=3,width=20).grid(row=2,column=0)
        tk.Entry(self.insert,textvariable=self.hwmc,width=30,state='disable').grid(row=2,column=1)

        tk.Label(self.insert, text='单位', height=3, width=20).grid(row=3, column=0)
        tk.Entry(self.insert, textvariable=self.dw, width=30,state='disable').grid(row=3, column=1)

        tk.Label(self.insert, text='入库数量', height=3, width=20).grid(row=4, column=0)
        tk.Entry(self.insert, textvariable=self.rksl,width=30).grid(row=4, column=1)

        tk.Label(self.insert, text='办理人', height=3, width=20).grid(row=5, column=0)
        tk.Entry(self.insert, textvariable=self.blr,width=30).grid(row=5, column=1)

        tk.Label(self.insert, text='货物来源', height=3, width=20).grid(row=6, column=0)
        tk.Entry(self.insert, textvariable=self.hwly,width=30).grid(row=6, column=1)

        inset_sub=tk.Button(self.insert,text='提交',command=self.insert_sub, height=2, width=20)
        inset_sub.grid(row=7, column=0)
        inset_cal=tk.Button(self.insert,text='返回',command=self.insert_cal, height=2, width=20)
        inset_cal.grid(row=7, column=1)

    def insert_sub(self):
        if self.hwbm.get() != '' and self.rksl.get() >0 and self.blr.get() != '':
            # 数据库操作
            conn = sqlite3.connect('goods.db')
            cur = conn.cursor()

            # 取货物编码对应货物信息
            data_hwbm = self.hwbm.get()
            # print(data_hwbm)
            sql_goods = f"select * from goods_table where hwbm={data_hwbm}"
            # print(sql_goods)
            cur.execute(sql_goods)

            temp=cur.fetchall()
            if temp == []:
                mbox.showerror('错误信息', '货物编码不存在')
                return
            # print(temp)
            # print(temp[0][0])
            data=temp[0][:4]     #不要库存数量
            rksj=datetime.date.today()     #取当前日期

            # 插入到入库信息表
            data = data +(self.rksl.get(),self.blr.get(),self.hwly.get(),rksj)
            # print(data)
            sql_insert="insert into insert_table(hwbm,hwxh,hwmc,dw,rksl,blr,hwly,rksj) values (?,?,?,?,?,?,?,?)"
            cur.execute(sql_insert,data)
            conn.commit()

            # 修改货物信息表库存数量
            kcsl=int(temp[0][4:][0])+self.rksl.get()
            # print(kcsl)
            # print(type(kcsl))
            cur.execute("update goods_table set kcsl=? where hwbm=?",(kcsl,data_hwbm))
            conn.commit()
            cur.close()
            conn.close()

            mbox.showinfo('提示信息', '入库成功!')
            self.insert.destroy()
            goods_info()
        else:
            mbox.showerror('错误信息', '货物编码,入库数量,办理人不能为空!')
            return

    def insert_cal(self):
        self.insert.destroy()

class out_manager:
    def __init__(self):
        self.out = tk.Toplevel()
        self.out.title('出库管理')
        self.out.geometry('400x600')

        self.hwbm = tk.IntVar()
        self.hwxh = tk.StringVar()
        self.hwmc= tk.StringVar()
        self.dw= tk.StringVar()

        self.cksl= tk.IntVar()
        self.blr= tk.StringVar()
        self.lyr= tk.StringVar()
        self.lysy= tk.StringVar()
        self.openpage()

    def openpage(self):
        tk.Label(self.out, text='货物编码', height=3, width=20).grid(row=0, column=0)
        tk.Entry(self.out, textvariable=self.hwbm, width=30).grid(row=0, column=1)

        tk.Label(self.out, text='货物型号', height=3, width=20).grid(row=1, column=0)
        tk.Entry(self.out, textvariable=self.hwxh, width=30,state='disable').grid(row=1, column=1)

        tk.Label(self.out,text='货物名称',height=3,width=20).grid(row=2,column=0)
        tk.Entry(self.out,textvariable=self.hwmc,width=30,state='disable').grid(row=2,column=1)

        tk.Label(self.out,text='单位',height=3,width=20).grid(row=3,column=0)
        tk.Entry(self.out,textvariable=self.dw,width=30,state='disable').grid(row=3,column=1)

        tk.Label(self.out, text='出库数量', height=3, width=20).grid(row=4, column=0)
        tk.Entry(self.out, textvariable=self.cksl,width=30).grid(row=4, column=1)

        tk.Label(self.out, text='办理人', height=3, width=20).grid(row=5, column=0)
        tk.Entry(self.out, textvariable=self.blr,width=30).grid(row=5, column=1)

        tk.Label(self.out, text='领用人', height=3, width=20).grid(row=6, column=0)
        tk.Entry(self.out, textvariable=self.lyr, width=30).grid(row=6, column=1)

        tk.Label(self.out, text='领用事由', height=3, width=20).grid(row=7, column=0)
        tk.Entry(self.out, textvariable=self.lysy, width=30).grid(row=7, column=1)

        out_sub=tk.Button(self.out,text='提交',command=self.out_sub, height=2, width=20)
        out_sub.grid(row=8, column=0)
        out_cal=tk.Button(self.out,text='返回',command=self.out_cal, height=2, width=20)
        out_cal.grid(row=8, column=1)

    def out_sub(self):
        if self.hwbm.get() != '' and self.cksl.get() >0 and self.blr.get() != '' and self.lyr.get() != '':
            # 数据库操作
            conn = sqlite3.connect('goods.db')
            cur = conn.cursor()

            # 取货物编码对应货物信息
            data_hwbm = self.hwbm.get()
            # print(data_hwbm)
            sql_goods = "select * from goods_table where hwbm=%d" % (data_hwbm)
            # print(sql_goods)
            cur.execute(sql_goods)
            temp = cur.fetchall()

            if temp == []:
                mbox.showerror('错误信息', '货物编码不存在')
                return
            # print(temp[0][0])
            data = temp[0][:4]  # 不要库存数量
            cksj = datetime.date.today()  # 取当前日期

            kcsl = int(temp[0][4:][0]) - self.cksl.get()
            if kcsl >= 0:
            # 插入到出库信息表
                data = data + (self.cksl.get(), self.blr.get(), self.lyr.get(),self.lysy.get(), cksj)
                # print(data)
                sql_out = "insert into out_table(hwbm,hwxh,hwmc,dw,cksl,blr,lyr,lysy,cksj) values (?,?,?,?,?,?,?,?,?)"
                cur.execute(sql_out, data)
                conn.commit()
                # 修改货物信息表库存数量
                cur.execute("update goods_table set kcsl=? where hwbm=?", (kcsl, data_hwbm))
                conn.commit()
                cur.close()
                conn.close()
                mbox.showinfo('提示信息', '出库成功!')
                self.out.destroy()
                goods_info()
            else:
                mbox.showinfo('警告','货不够了老表!')
                return
        else:
            mbox.showerror('错误信息', '货物编码,出库数量,办理人,领用人不能为空!')
            return

    def out_cal(self):
        self.out.destroy()

class bor_manager:
    def __init__(self):
        self.bor = tk.Toplevel()
        self.bor.title('借货管理')
        self.bor.geometry('400x600')

        self.hwbm = tk.IntVar()
        self.hwxh = tk.StringVar()
        self.hwmc= tk.StringVar()
        self.dw= tk.StringVar()

        self.jhsl= tk.IntVar()
        self.blr= tk.StringVar()
        self.jhr= tk.StringVar()
        self.jhsy= tk.StringVar()
        self.openpage()

    def openpage(self):
        tk.Label(self.bor, text='货物编码', height=3, width=20).grid(row=0, column=0)
        tk.Entry(self.bor, textvariable=self.hwbm, width=30).grid(row=0, column=1)

        tk.Label(self.bor, text='货物型号', height=3, width=20).grid(row=1, column=0)
        tk.Entry(self.bor, textvariable=self.hwxh, width=30,state='disable').grid(row=1, column=1)

        tk.Label(self.bor,text='货物名称',height=3,width=20).grid(row=2,column=0)
        tk.Entry(self.bor,textvariable=self.hwmc,width=30,state='disable').grid(row=2,column=1)

        tk.Label(self.bor,text='单位',height=3,width=20).grid(row=3,column=0)
        tk.Entry(self.bor,textvariable=self.dw,width=30,state='disable').grid(row=3,column=1)

        tk.Label(self.bor, text='借货数量', height=3, width=20).grid(row=4, column=0)
        tk.Entry(self.bor, textvariable=self.jhsl,width=30).grid(row=4, column=1)

        tk.Label(self.bor, text='办理人', height=3, width=20).grid(row=5, column=0)
        tk.Entry(self.bor, textvariable=self.blr,width=30).grid(row=5, column=1)

        tk.Label(self.bor, text='借货人', height=3, width=20).grid(row=6, column=0)
        tk.Entry(self.bor, textvariable=self.jhr, width=30).grid(row=6, column=1)

        tk.Label(self.bor, text='借货事由', height=3, width=20).grid(row=7, column=0)
        tk.Entry(self.bor, textvariable=self.jhsy, width=30).grid(row=7, column=1)

        out_sub=tk.Button(self.bor,text='提交',command=self.bor_sub, height=2, width=20)
        out_sub.grid(row=8, column=0)
        out_cal=tk.Button(self.bor,text='返回',command=self.bor_cal, height=2, width=20)
        out_cal.grid(row=8, column=1)

    def bor_sub(self):
        if self.hwbm.get() != '' and self.jhsl.get() >0 and self.blr.get() != '' and self.jhr.get() != '':
            # 数据库操作
            conn = sqlite3.connect('goods.db')
            cur = conn.cursor()

            # 取货物编码对应货物信息
            data_hwbm = self.hwbm.get()
            # print(data_hwbm)
            sql_goods = "select * from goods_table where hwbm=%d" % (data_hwbm)
            # print(sql_goods)
            cur.execute(sql_goods)
            temp = cur.fetchall()

            if temp == []:
                mbox.showerror('错误信息', '货物编码不存在')
                return
            # print(temp[0][0])
            data = temp[0][:4]  # 不要库存数量
            jhsj = datetime.date.today()  # 取当前日期
            kcsl = int(temp[0][4:][0]) - self.jhsl.get()
            cljg='未结清'    #加入默认处理结果
            if kcsl >= 0:
            # 插入到借货信息表
                data = data + (self.jhsl.get(), self.blr.get(), self.jhr.get(),self.jhsy.get(), jhsj,cljg)
                # print(data)
                sql_bor = """insert into bor_table(hwbm,hwxh,hwmc,dw,jhsl,blr,jhr,jhsy,jhsj,cljg) 
                          values (?,?,?,?,?,?,?,?,?,?)"""
                cur.execute(sql_bor, data)
                conn.commit()
                # 修改货物信息表库存数量
                cur.execute("update goods_table set kcsl=? where hwbm=?", (kcsl, data_hwbm))
                conn.commit()
                # 查询借货编码
                temp=cur.execute("select max(jhbm) from bor_table")
                temp = temp.fetchall()
                yours=temp[0][0]
                conn.commit()
                cur.close()
                conn.close()
                mbox.showinfo('提示信息', f'借出成功!请牢记你的借货编码:{yours}')
                self.bor.destroy()
                goods_info()
            else:
                mbox.showinfo('警告','货不够了老表!')
                return
        else:
            mbox.showerror('错误信息', '货物编码,借货数量,办理人,借货人不能为空!')
            return

    def bor_cal(self):
        self.bor.destroy()

class lend_manager:
    def __init__(self):
        self.beforepage()

        self.hwbm = tk.IntVar()
        self.hwxh = tk.StringVar()
        self.hwmc= tk.StringVar()
        self.dw= tk.StringVar()

        self.jhsl= tk.IntVar()
        self.blr= tk.StringVar()
        self.jhr= tk.StringVar()
        self.jhsy= tk.StringVar()
        self.jhsj= tk.StringVar()
        # self.jhbm =tk.IntVar()
        self.ghsl=tk.IntVar()

    def beforepage(self):
        self.before = tk.Toplevel()
        self.before.title('请输入借货编码')
        self.before.geometry('400x200')

        self.jhbm = tk.IntVar()

        tk.Label(self.before, text='借货编码', height=3, width=20).grid(row=0, column=0)
        tk.Entry(self.before, textvariable=self.jhbm, width=30).grid(row=0, column=1)

        tk.Button(self.before, text='提交', command=self.before_sub, height=2, width=20).grid(row=1, column=0)
        tk.Button(self.before, text='返回', command=self.before_cal, height=2, width=20).grid(row=1, column=1)

    def before_sub(self):
        conn=sqlite3.connect('goods.db')
        cur=conn.cursor()
        cur.execute(f"select * from bor_table where jhbm={self.jhbm.get()}")
        self.mybor=cur.fetchall()
        # print(self.mybor)
        cur.close()
        conn.close()

        if self.mybor==[]:
            mbox.showerror('错误信息','借货编码不存在')
            return

        # print(self.mybor[0][10])
        if self.mybor[0][10]=='已结清':
            mbox.showinfo('提示信息','该借货编码已结清!')
            return

        self.before.destroy()
        self.openpage()

    def before_cal(self):
        self.before.destroy()

    def openpage(self):
        self.lend = tk.Toplevel()
        self.lend.title('归还管理')
        self.lend.geometry('400x800')

        print(self.mybor)
        self.jhbm.set(self.mybor[0][0])
        self.hwbm.set(self.mybor[0][1])
        self.hwxh.set(self.mybor[0][2])
        self.hwmc.set(self.mybor[0][3])
        self.dw.set(self.mybor[0][4])
        self.jhsl.set(self.mybor[0][5])
        self.blr.set(self.mybor[0][6])
        self.jhr.set(self.mybor[0][7])
        self.jhsy.set(self.mybor[0][8])
        self.jhsj.set(self.mybor[0][9])

        tk.Label(self.lend, text='货物编码', height=3, width=20).grid(row=0, column=0)
        tk.Entry(self.lend, textvariable=self.hwbm, width=30,state='disable').grid(row=0, column=1)

        tk.Label(self.lend, text='货物型号', height=3, width=20).grid(row=1, column=0)
        tk.Entry(self.lend, textvariable=self.hwxh, width=30,state='disable').grid(row=1, column=1)

        tk.Label(self.lend,text='货物名称',height=3,width=20).grid(row=2,column=0)
        tk.Entry(self.lend,textvariable=self.hwmc,width=30,state='disable').grid(row=2,column=1)

        tk.Label(self.lend,text='单位',height=3,width=20).grid(row=3,column=0)
        tk.Entry(self.lend,textvariable=self.dw,width=30,state='disable').grid(row=3,column=1)

        tk.Label(self.lend, text='借货数量', height=3, width=20).grid(row=4, column=0)
        tk.Entry(self.lend, textvariable=self.jhsl,width=30,state='disable').grid(row=4, column=1)

        tk.Label(self.lend, text='办理人', height=3, width=20).grid(row=5, column=0)
        tk.Entry(self.lend, textvariable=self.blr,width=30,state='disable').grid(row=5, column=1)

        tk.Label(self.lend, text='借货人', height=3, width=20).grid(row=6, column=0)
        tk.Entry(self.lend, textvariable=self.jhr, width=30,state='disable').grid(row=6, column=1)

        tk.Label(self.lend, text='借货事由', height=3, width=20).grid(row=7, column=0)
        tk.Entry(self.lend, textvariable=self.jhsy, width=30,state='disable').grid(row=7, column=1)

        tk.Label(self.lend, text='借货时间', height=3, width=20).grid(row=8, column=0)
        tk.Entry(self.lend, textvariable=self.jhsj, width=30,state='disable').grid(row=8, column=1)

        tk.Label(self.lend, text='借货编码', height=3, width=20).grid(row=9, column=0)
        tk.Entry(self.lend, textvariable=self.jhbm, width=30,state='disable').grid(row=9, column=1)

        tk.Label(self.lend, text='归还数量', height=3, width=20).grid(row=10, column=0)
        tk.Entry(self.lend, textvariable=self.ghsl, width=30).grid(row=10, column=1)

        tk.Button(self.lend,text='提交',command=self.lend_sub, height=2, width=20).grid(row=11, column=0)
        tk.Button(self.lend,text='返回',command=self.lend_cal, height=2, width=20).grid(row=11, column=1)

    def lend_sub(self):
        if self.ghsl.get() >0 and self.ghsl.get() <= self.jhsl.get():
            # 数据库操作
            conn = sqlite3.connect('goods.db')
            cur = conn.cursor()

            data=self.mybor[0][:10]
            ghsj = datetime.date.today()
            print(data)

            # 插入归还信息表
            data=data+(self.ghsl.get(),ghsj)
            sql_lend = """insert into lend_table(jhbm,hwbm,hwxh,hwmc,dw,jhsl,blr,jhr,jhsy,jhsj,ghsl,ghsj)
            values (?,?,?,?,?,?,?,?,?,?,?,?)"""
            cur.execute(sql_lend,data)
            conn.commit()

            # 更新库存信息表库存数量
            mykcsl=cur.execute(f"select kcsl from goods_table where hwbm={self.hwbm.get()}")
            mykcsl=mykcsl.fetchall()
            kcsl =mykcsl[0][0]+self.ghsl.get()
            # print(kcsl)
            cur.execute(f"update goods_table set kcsl={kcsl} where hwbm={self.hwbm.get()}")
            conn.commit()

            newghbm = cur.execute("select max(ghbm) from lend_table ")
            newghbm = newghbm.fetchall()  # 查询归还编码
            print(newghbm)

            oldghbm = cur.execute(f"select ghbm from bor_table where jhbm={self.jhbm.get()}")
            oldghbm = oldghbm.fetchall()    #查询是否已经归还过
            print(oldghbm)
            if oldghbm[0][0] == None:
                myghbm = newghbm[0][0]
                print(1)
                print(myghbm)
            else:
                myghbm = oldghbm[0][0] + ',' + str(newghbm[0][0])
                print(2)
                print(myghbm)

            if self.ghsl.get() == self.jhsl.get():
                cur.execute(f"update bor_table set cljg='已结清',ghbm='{myghbm}',jhsl=0 "
                            f"where jhbm={self.jhbm.get()}")
                conn.commit()
                mbox.showinfo('提示信息', f'归还成功!本次借还已结清,归还编码为{myghbm}')
            else:
                sysl= self.jhsl.get()-self.ghsl.get()
                cur.execute(f"update bor_table set ghbm='{myghbm}',jhsl={sysl} where jhbm={self.jhbm.get()}")
                conn.commit()
                mbox.showinfo('提示信息', f'归还成功!本次归还编码为{myghbm},剩余{sysl}未归还!')

            cur.close()
            conn.close()
            self.lend.destroy()
            goods_info()
        elif self.ghsl.get() >0 and self.ghsl.get() > self.jhsl.get():
            mbox.showerror('错误信息','归还数量不能大于借货数量!')
            return
        else:
            mbox.showerror('错误信息', '归还数量不能为空!')
            return

    def lend_cal(self):
        self.lend.destroy()

class menu_admin:
    def __init__(self):
        self.clear = tk.Toplevel()
        self.clear.title('请输入管理员账号和密码')
        self.clear.geometry('400x200')

        self.glyzh = tk.StringVar()
        self.glymm = tk.StringVar()

        tk.Label(self.clear, text='管理员账号', height=3, width=20).grid(row=0, column=0)
        tk.Entry(self.clear, textvariable=self.glyzh, width=30).grid(row=0, column=1)
        tk.Label(self.clear, text='管理员密码', height=3, width=20).grid(row=1, column=0)
        tk.Entry(self.clear, textvariable=self.glymm, width=30, show='*').grid(row=1, column=1)

        tk.Button(self.clear, text='提交', command=self.admin_sub, height=2, width=20).grid(row=2, column=0)
        tk.Button(self.clear, text='返回', command=self.admin_cal, height=2, width=20).grid(row=2, column=1)

    def admin_sub(self):
        if self.glyzh.get() == 'admin' and self.glymm.get() == 'woaini':
            # 数据库操作
            conn = sqlite3.connect('goods.db')
            cur = conn.cursor()
            cur.execute("delete from goods_table")
            cur.execute("update sqlite_sequence SET seq = 0 where name ='goods_table'")
            cur.execute("delete from insert_table")
            cur.execute("update sqlite_sequence SET seq = 0 where name ='insert_table'")
            cur.execute("delete from out_table")
            cur.execute("update sqlite_sequence SET seq = 0 where name ='out_table'")
            cur.execute("delete from bor_table")
            cur.execute("update sqlite_sequence SET seq = 0 where name ='bor_table'")
            cur.execute("delete from lend_table")
            cur.execute("update sqlite_sequence SET seq = 0 where name ='lend_table'")
            conn.commit()
            cur.close()
            conn.close()

            mbox.showinfo('提示信息', '数据清空成功!')
            self.clear.destroy()
            goods_info()
        else:
            mbox.showerror('错误信息', '账号或密码错误')
            return

    def admin_cal(self):
        self.clear.destroy()

def menu_read():
    read=tk.Toplevel()
    read.title('使用说明')
    read.geometry('400x300')

    text_read=tk.Text(read,width=40,height=20)
    text_read.pack()
    text="""使用说明:
    1.本程序使用sqlite3数据库执行操作,如无法打开可尝试下载sqlite,首次使用默认自动创建数据库表格;
    2.首先将所需要的商品录入到管理模块-货物管理,系统为您自动生成货物编码;
    3.利用货物编码即可对货物进行出入库操作;
    4.借货将自动生成借货编码,用于货物归还;
    5.货物归还将自动生成归还编码,全部货物归还则结清本次借还,可分多次归还货物;
    6.如遇任何bug请及时联系管理员!"""
    text_read.insert('1.0',text)

def menu_downloadsqlite3():
    webbrowser.open('https://sqlite.org/download.html',new=1,autoraise=True)

def sqlite_create():
    try:
        conn = sqlite3.connect('./goods.db')
        cur = conn.cursor()
        try:
            cur.execute("""CREATE TABLE goods_table (
                        hwbm integer primary key autoincrement,
                        hwxh varchar,
                        hwmc varchar,
                        dw varchar,
                        kcsl int default 0
                    );""")
            cur.execute("""CREATE TABLE insert_table (
                        xh integer primary key autoincrement,
                        hwbm int ,
                        hwxh varchar,
                        hwmc varchar,
                        dw varchar,
                        rksl int,
                        blr varchar,
                        hwly varchar,
                        rksj varchar 
                    );""")
            cur.execute("""CREATE TABLE out_table (
                        xh integer primary key autoincrement,
                        hwbm int ,
                        hwxh varchar,
                        hwmc varchar,
                        dw varchar,
                        cksl int,
                        blr varchar,
                        lyr varchar,
                        lysy varchar,
                        cksj varchar 
                    );""")
            cur.execute("""CREATE TABLE bor_table (
                        jhbm integer primary key autoincrement,
                        hwbm int ,
                        hwxh varchar,
                        hwmc varchar,
                        dw varchar,
                        jhsl int,
                        blr varchar,
                        jhr varchar,
                        jhsy varchar,
                        jhsj varchar ,
                        cljg varchar,
                        ghbm varchar
                    );""")
            cur.execute("""CREATE TABLE lend_table (
                        ghbm integer primary key autoincrement,
                        jhbm int,
                        hwbm int ,
                        hwxh varchar,
                        hwmc varchar,
                        dw varchar,
                        jhsl int,
                        blr varchar,
                        jhr varchar,
                        jhsy varchar,
                        jhsj varchar ,
                        ghsl int,
                        ghsj varchar
                    );""")
            mbox.showinfo('提示信息','数据库初始化成功!')
            return True
        except OperationalError as o:
            if str(o) == "table lend_table already exists":
                mbox.showinfo('提示信息', '数据库初始化已完成,无须再执行!')
                return
        except Exception as e:
            print(e)
            return
        finally:
            cur.close()
            conn.close()
    except not os.path.exists('./goods.db'):
        open('./goods.db',encoding='utf-8',mode='x')

if __name__ == '__main__':
    win()