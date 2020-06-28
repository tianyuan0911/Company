# -*- coding: UTF-8 -*-

import xlrd
import xlwt

excel_path = './导入职务模板.xlsx'
# 读取excel数据文件
workbook = xlrd.open_workbook(excel_path)
sheet1 = workbook.sheets()[0]

nrows = sheet1.nrows
ncols = sheet1.ncols
# 输出行数、列数
print('nrows:',nrows,';  ncols:',ncols)

# 获取第一行说明文字
row_explain = sheet1.row_values(0)
print(row_explain)
# 获取表头
header = sheet1.row_values(1)

# 将表头存入字典
list = [0,1,2,3,4,5]
header_dict = dict(zip(header,list))

user_name_index = header_dict[u'用户名']
real_name_index = header_dict[u'姓名']
position_index = header_dict[u'职务']
grade_index = header_dict[u'年级']
class_index = header_dict[u'班级']
subject_index = header_dict[u'学科']

position_list = [u'校长',u'副校长',u'德育主任',u'总务主任',u'教导主任',u'年级主任',u'教研组长',u'备课组长',u'班主任']
position_part_list = [u'校长',u'副校长',u'德育主任',u'总务主任',u'教导主任']
subject_list = [u'语文',u'数学',u'英语',u'物理',u'化学',u'生物',u'历史',u'地理',u'政治',u'体育',u'音乐',u'美术',u'技术',u'综合']
grade_list = [u'一年级',u'二年级',u'三年级',u'四年级',u'五年级',u'六年级',u'七年级',u'八年级',u'九年级',u'高一',u'高二',u'高三']

#假设系统已有班级 -> 从数据库中取班级
class_list = [u'1班',u'2班',u'3班',u'4班']

successList = [] #存放校验通过的行
successList.append(header)

user_name_list = [] #存放用户名
real_name_list = [] #存放姓名


# 遍历excel行 -> 进行内容校验
for row_index in range(2,nrows):
    # 获取用户名
    user_name_cell_value = sheet1.cell_value(row_index,user_name_index)
    # 获取姓名
    real_name_cell_value = sheet1.cell_value(row_index,real_name_index)
    # 获取职务
    position_cell_value = sheet1.cell_value(row_index, position_index)
    # 获取年级
    grade_cell_value = sheet1.cell_value(row_index, grade_index)
    # 获取班级
    class_cell_value = sheet1.cell_value(row_index, class_index)
    # 获取学科
    subject_cell_value = sheet1.cell_value(row_index, subject_index)


    # 判断是否一人身兼多职
    if user_name_cell_value not in user_name_list:
        user_name_list.append(user_name_cell_value)
        real_name_list.append(real_name_cell_value)
    else:
        if real_name_cell_value not in real_name_list:
            print(u'校验失败 ',user_name_cell_value,u'-> 同一个用户名姓名应该相同')
            continue

    #职务校验
    if position_cell_value not in position_list or len(position_cell_value)==0:
        #职务填写错误
        print(u'校验失败 ',user_name_cell_value,u'-> 职务填写错误')
        continue

    #逻辑字段校验
    if position_cell_value == u'教研组长':
        #校验学科
        if subject_cell_value not in subject_list or len(subject_cell_value) == 0:
            print(u'校验失败  ',user_name_cell_value,u'-> 教研组长->学科必填且规范 ')
            continue
        #校验年级和班级
        if len(grade_cell_value)!=0 or len(class_cell_value)!=0:
            print(u'校验失败 ', user_name_cell_value, u'-> 教研组长->年级学科不填 ')
            continue

    if position_cell_value == u'备课组长':
        # 校验学科
        if subject_cell_value not in subject_list or len(subject_cell_value) == 0:
            print(u'校验失败 ', user_name_cell_value, u'-> 备课组长->学科必填且规范 ')
            continue
        # 校验年级
        if grade_cell_value not in grade_list or len(grade_cell_value) == 0:
            print(u'校验失败 ', user_name_cell_value, u'-> 备课组长->年级必填且规范 ')
            continue
        # 校验班级
        if len(class_cell_value)!=0:
            print(u'校验失败 ', user_name_cell_value, u'-> 备课组长->学科不填 ')
            continue

    if position_cell_value == u'班主任':
        # 校验年级
        if grade_cell_value not in grade_list or len(grade_cell_value) == 0:
            print(u'校验失败 ', user_name_cell_value, u'-> 班主任->年级必填且规范 ')
            continue
        # 校验班级
        if class_cell_value not in class_list or len(class_cell_value) == 0:
            print(u'校验失败 ', user_name_cell_value, u'-> 班主任->班级必填且规范 ')
            continue
        # 校验学科
        if len(subject_cell_value) != 0:
            print(u'校验失败 ', user_name_cell_value, u'-> 班主任->学科不填 ')
            continue
    #校验校长等职务
    if position_cell_value in position_part_list:
        if len(grade_cell_value) != 0 or len(class_cell_value) != 0 or len(subject_cell_value) != 0:
            print(u'校验失败 ', user_name_cell_value, u'->校长、副校长、德育主任、总务主任、教导主任时，年级、班级、学科均不用填')
            continue

    #都满足则符合系统校验逻辑
    row_values = sheet1.row_values(row_index)
    successList.append(row_values)
    # 输出满足条件行
    print(u"校验通过", ', '.join(row_values))
#print('user_name_list: ',user_name_list)
print(u'通过校验的行数：',len(successList)-1)

#将验证通过的数据导入excel
book =  xlwt.Workbook(encoding='utf-8')
sheet = book.add_sheet('sheet1')
#设置列宽
first_col = sheet.col(0)
sec_col = sheet.col(1)
third_col = sheet.col(2)

first_col.width = 256 * 30
sec_col.width = 256 * 30
third_col.width = 256 * 30
#单元格设置[0,0]
tall_style = xlwt.easyxf('font:height 3200')  # 36pt
first_row = sheet.row(0)
first_row.set_style(tall_style)
style = xlwt.easyxf('align: wrap on') #单元格内容自动换行
sheet.write_merge(0, 0, 0, 5, row_explain,style) #合并单元格

for i in range(1,len(successList)+1):
	for j in range(0,len(header)):
		sheet.write(i,j, label = successList[i-1][j])

book.save('校验通过职务模板.xls')










