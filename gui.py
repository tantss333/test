import sys, os
import PySimpleGUI as sg
import threading
import json
import function


sg.theme("LightGray")

path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])))

def mainWin():
    sg.set_options(
        font=("", 11),
        text_color='black'
    )

    col3_1 = sg.Column([
        [sg.T("当日交易模块", font=("", 12))]
    ])

    col3_2 = sg.Column([
        [sg.Combo([], readonly=True, size=(20,10), font=10, background_color="white", text_color="black", key="plate", enable_events=True)],

    ])


    c = sg.Frame('',[[col3_1,col3_2,sg.Button('刷新交易模块(可选)',key='refresh_schedule')]],border_width=0)


    bid_col1 = sg.Col([
        [sg.T('标的物编号：')],
        [sg.T('标的物名称：')],
        [sg.T('数量（吨）：')],
        [sg.T('开始时间：')],
        [sg.T('结束时间：')],
    ])

    bid_col2 = sg.Col([
        [sg.T('   ',key='matterCode')],
        [sg.T('   ',key='name')],
        [sg.T('   ',key='quantity')],
        [sg.T('   ',key='startTime')],
        [sg.T('   ',key='endTime')],
    ])

    bid_frame = sg.Frame('',[
        [bid_col1,bid_col2]
    ], vertical_alignment='top')

    bid_col3 = sg.Col([
        [sg.T('状态：',font=('',16))],
        [sg.T('起拍价格：',font=('',16),text_color='green')],
        [sg.T('当前价格：', text_color='blue',font=('',16))],
    ])

    bid_col4 = sg.Col([
        [sg.T('   ', key='status',font=('',16))],
        [sg.T('   ', key='begin_price',font=('',16),text_color='green')],
        [sg.T('   ', key='current_price', text_color='blue',font=('',16))],
    ])

    bid_frame2 = sg.Frame('', [
        [bid_col3, bid_col4]
    ],vertical_alignment='top')

    funtion_part2 = sg.Frame("", [
        [c],
        [sg.Button('停止刷新场次', key='stop-check', visible=False, disabled_button_color=('white', 'gray'))],
        [bid_frame, bid_frame2],
    ],key='frame1'
             )

    time_frame = sg.Frame('',[
        [sg.T('离结束还有(秒):', font=('',18)), sg.T('       ', key='gap', font=('',17),text_color='red')]
    ])

    book_part = sg.Frame("", [
        [time_frame],
        [sg.T('投标上限（可选）')],
        [sg.InputText("",key="limitPrice",size=(15,1), background_color="white", text_color="black",border_width=1, font=10)],
        [sg.Button('自动加注', size=(20, 1), key="start",disabled_button_color=('white','gray'))],
        [sg.Button('停止', size=(20, 1), key="stop")],

    ], vertical_alignment='top', border_width=0)

    show_part = sg.Frame("提示区域",[
        [sg.Multiline(key="show",size=(70,10),background_color="white", font=8, text_color="black")],[sg.Button('清空内容', key='clear')]])

    col_left = sg.Column([
        [funtion_part2]
    ], vertical_alignment='top')

    col_right = sg.Column([
        [book_part]
    ],vertical_alignment='top')

    user_part = sg.Frame('用户信息',[
        [sg.T('用户名:'),sg.In('',size=(20,1),key='user', background_color='white',text_color='black', border_width=1),
         sg.T('登录密码:'),sg.In('',size=(20,1),key='passwd', background_color='white',text_color='black', border_width=1),
         sg.Button('登录',key='login')]
    ])

    table = sg.Table(values=[], headings=['是否中标', '下单Order', '标的物编号', '名称','数量','出价'],
                     font=("Arial", 12),
                     auto_size_columns=False,
                     col_widths=[10, 15, 15, 10,10,10],
                     def_col_width=50,
                     justification='center',
                     num_rows=10,
                     alternating_row_color='#FAEBD7',
                     # selected_row_colors=('black', 'white'),
                     key='table',
                     )

    layout = [
        [
            [user_part],
            # sg.Button('手动更换代理地址', font=("",10),size=(20,1),key='proxy-button'),
            # sg.Button('添加IP', font=("",10),size=(20,1),key='ip-button'),
         ],
        [col_left, col_right],
        [table],
        [show_part]
    ]

    mainW = sg.Window("榆林煤炭交易市场", layout=layout, finalize=True)

    f = function.Function(mainW)

    try:
        with open('./user.json', 'r', encoding='utf-8') as file:
            user_dict = json.load(file)
            file.close()

        mainW['user'].update(user_dict['user'])
        mainW['passwd'].update(user_dict['passwd'])
    except:
        pass

    while True:

        event, value = mainW.read()

        if event == 'login':
            if '' in [value['user'], value['passwd']]:
                sg.Popup('请保证账号密码完整')
                continue

            f.login(value['user'], value['passwd'])

        elif event == 'return-gap':
            mainW['gap'].update(value['return-gap'])

        elif event == 'return-info':
            matterCode, name, quantity, startTime, endTime, status, beginPrice, current_price = value['return-info']

            mainW['matterCode'].update(matterCode)
            mainW['name'].update(name)
            mainW['quantity'].update(quantity)
            mainW['startTime'].update(startTime)
            mainW['endTime'].update(endTime)

            mainW['status'].update('未开始' if status==1 else '正在招标')
            mainW['begin_price'].update(beginPrice)
            mainW['current_price'].update(current_price)


        elif event == 'return-plate':
            plate_dict = value['return-plate']

            plate_list = [i for i in plate_dict.keys()]
            mainW['plate'].update(values=plate_list)
            mainW['show'].print('监测到当前有 %s 个竞价'%len(plate_list))


        elif event == 'refresh_schedule':
            f.check_scedule()


        elif event == 'ip-button':
            ip = sg.PopupGetText('',title='请输入ip地址', background_color='white', text_color='black')

            if ip is None or ip == '':
                continue

            check_ip = ip.split('.')
            if len(check_ip) != 4:
                sg.Popup('IP地址格式不正确')
                continue
            else:
                f.add_whitelist(ip)

        #
        # elif event == 'proxy-button':
        #     proxy_win.win()


        elif event in [None, 'Quit']:
            try:
                f.stop_check()
            except:
                pass
            break

        elif event == 'clear':
            mainW['show'].update('')

        elif event == 'return-table':
            mainW['table'].update(values=value['return-table'])


        elif event == 'stop-check':
            try:
                f.stop_check()
            except:
                pass
            mainW['stop-check'].update(visible=False)

            mainW['matterCode'].update('')
            mainW['name'].update('')
            mainW['quantity'].update('')
            mainW['startTime'].update('')
            mainW['endTime'].update('')
            mainW['status'].update('')
            mainW['begin_price'].update('')
            mainW['current_price'].update('')

            mainW['table'].update(values=[])


        elif event == 'plate':

            try:
                f.stop_check()
            except:
                pass

            plateId = plate_dict[value['plate']]['plateId']
            tradeModeId = plate_dict[value['plate']]['tradeModeId']
            tradeTimeId = plate_dict[value['plate']]['tradeTimeId']
            mainW['show'].update('开始监测场次......\n')
            mainW['stop-check'].update(visible=True)

            threading.Thread(target=f.run, args=(plateId,tradeModeId,tradeTimeId,),daemon=True).start()
            threading.Thread(target=f.get_bid_result, daemon=True).start()


        elif event == 'message':
            mainW['show'].print(value['message'])


        elif event == 'message1':
            mainW['show'].print(value['message1'],text_color='red')

        elif event == 'clear-message':
            mainW['show'].update('')


        elif event == 'start':
            mainW['start'].update(disabled=True)
            threading.Thread(target=f.start_bid, args=(value['limitPrice'],),daemon=True).start()

        elif event == 'stop':
            try:
                f.stop_bid()
            except:
                pass
            mainW['start'].update(disabled=False)

        elif event == 'reset-status':
            mainW['start'].update(disabled=False)

    mainW.close()


if __name__ == '__main__':
    #

    mainWin()
