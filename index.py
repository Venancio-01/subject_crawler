from excel import init_excel, edit_excel, save_excel
from browser import init_browser, get_data, quit_browser

url = 'https://learn.open.com.cn/studentcenter/MyWork/ExercisePreviewPage?courseId=24149&way=1b303c34-0c1d-426c-b907-9a6ffb06e343,6d4904f6-e1bb-4049-90f4-464b7edf919b&goodsId=null'


def main():
    workbook, sheet = init_excel()
    init_browser(url)
    subject_title, right_answer = get_data()
    print(len(subject_title), 'total subject_title')
    print(len(right_answer), 'total right_answer')
    edit_excel(sheet, subject_title, right_answer)
    save_excel(workbook)
    quit_browser()


main()
