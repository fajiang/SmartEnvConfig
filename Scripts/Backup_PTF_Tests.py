from pywinauto import application
import time
import os
import sys
import cx_Oracle


db_name = 'EP92PDVL'
ps_tool_path = 'C:\SmartAutomation\pt\\bin\client\winx86\pside.exe'
User_ID='VP1'
##User_Password='VP1'
User_Password='QEDMO'
db_user_name='people'
db_password='peop1e'
t_db_name= 'E92ERIC1'
#t_db_name= exo
t_ps_tool_path = 'C:\SmartAutomation\pt\\bin\client\winx86\pside.exe'
t_User_ID='VP1'
t_User_Password='VP1'
#tests=['PYSHELL01','PYSHELL02']
tests=['AR_TEST_CFL_0401_26223375','AR_TEST_CFL_0706_25990155','AR_TEST_CFL_1603_26038232','AR_TEST_CFL_0401_25455024','AR_TEST_CFL_0401_25455024','AR_TEST_CFL_0606_25837936','AR_TEST_CFL_0606_26039175','AR_TEST_CFL_1003_25830876','AR_TEST_CFL_1301_25406962','AR_TEST_CFL_1402_25607937']
proj_name='PTF_TEST'+str(time.strftime('%Y%m%d%H%M%S'))
copytoprjcmd = "%s -HIDE -PJTF %s -FP c:\\temp\\export -CT ORACLE -CD %s -CO %s -CP %s -QUIET -LF c:\\temp\\copytofile.log" % (ps_tool_path,proj_name,db_name,User_ID,User_Password)
copyfromprjcmd = "%s -HIDE -PJFF %s -FP c:\\temp\\export -CT ORACLE -CD %s -CO %s -CP %s -QUIET -LF c:\\temp\\copyfromfile.log" % (t_ps_tool_path,proj_name,t_db_name,t_User_ID,t_User_Password)

def get_all_test(tests):
    sql_base = 'select distinct pttst_cmd_recog ' + \
               'from pspttstcommand where pttst_cmd_obj_type = 35000 and pttst_cmd_type = 35001 ' + \
               'start with pttst_name in (%s) connect by nocycle prior pttst_cmd_recog = pttst_name'
    con = cx_Oracle.connect(db_user_name, db_password, db_name)
    cur = con.cursor()
    tests_str = "'%s'" % "','".join(tests)
    sql = sql_base % tests_str
    cur.execute(sql)
    names_set = set()
    for test_item in cur:
        names_set.add(test_item[0])
    for test_name in tests:
        names_set.add(test_name)
    print names_set
    cur.close()
    con.close()
    return list(names_set)

def login(app, db_name,User_ID,User_Password):
    login_window = app.top_window()
    #login_window.print_control_identifiers()
    login_window['&Database Name:Edit0'].type_keys(db_name)
    login_window['&User ID:Edit'].type_keys(User_ID)
    login_window['&Password:Edit'].type_keys(User_Password)
    login_window.OKButton.click()

def add_test(app,tests,main_form):
    main_form.MenuSelect('Insert->Definitions into Project...')
    insert_form=app.top_window()
    insert_form.ComboBox.Select('Tests')
    for test in tests:
        insert_form.Edit.type_keys(test)
        insert_form.ListBox.select('Test Cases')
        #insert_form.print_control_identifiers()
        insert_form['&Insert'].click()
        item_count = insert_form.ListView.ItemCount()
        if item_count > 0:
            insert_form.ListView.select(0)
            insert_form['&Insert'].click()
    insert_form['&Close'].click()

def save_project(main_form,app,proj_name):
    main_form.MenuSelect('File->Save Project As')
    save_window=app.top_window()
    #save_window.print_control_identifiers()
    save_window['Save Project &Name As:Edit'].type_keys(proj_name)
    save_window.OKButton.click()

def CopyToPrj():
    os.system(copytoprjcmd)

def CopyFromPrj():
    os.system(copyfromprjcmd)


if __name__ == '__main__':
    test_list = get_all_test(tests)
    app = application.Application()
    app.start(ps_tool_path)
    time.sleep(20)
    login(app, db_name,User_ID,User_Password)
    time.sleep(40)
    main_form=app.top_window()
    add_test(app,test_list,main_form)
    main_form=app.top_window()
    save_project(main_form,app,proj_name)
    main_form.close()
    CopyToPrj()
    CopyFromPrj()



