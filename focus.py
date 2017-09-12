# coding=utf-8

import tushare as ts
import pandas as pd
import datetime
import make_data
import log


def refresh_focus():
    return


def read_focus():
    log_file = open("log/focus.log", 'a+')
    log.write(log_file, "focus analyze start!")

    # 从focus.csc文件中获取最近5日的关注列表
    all_focus = []
    with open('focus/mean_deal.csv','r') as f:
        lines = f.readlines()
        if len(lines) < 5:
            line_cut = lines
        else:
            line_cut = lines[-5:]

        for i in range(0,len(line_cut)):
            all_focus.append(line_cut[i].strip().split(','))

    log.write(log_file, "get old focus list succeed!")

    f_change = open('focus/p_change_' + make_data.last_trade_date()[0] + ".html", 'w')
    f_change.write("<html>\n<body>\n")

    # 获取关注股票的近几日走势
    focus_p_change = []

    for i in range(0,len(all_focus)):
        f_change.write('<p>\n')
        f_change.write('<table border="1">\n')
        # 写入日期
        f_change.write('<caption align = "center" > %s </caption>\n' % all_focus[i][0])
        # 写入表头
        f_change.write('<tr align = "right">\n')
        f_change.write('<th>%s</th>\n' % "股票代码")
        f_change.write('<th>%s</th>\n' % "股票名称")
        print make_data.last_trade_date()[0]
        print all_focus[i][0]
        for l in list(pd.date_range(start=all_focus[i][0],end=make_data.last_trade_date()[0])):
            f_change.write('<th>%s</th>\n' % str(l)[5:10])
        f_change.write("</tr>\n")

        for j in range(1,len(all_focus[i])):
            f_change.write('<tr align = "right">\n')
            f_change.write('<td width="100">%s</td>\n' % all_focus[i][j])  # 输入第一列 股票代码
            f_change.write('<td width="100">%s</td>\n' % make_data.get_stock_name(all_focus[i][j][2:]))  # 输入第二列，股票名称
            hist = ts.get_hist_data(all_focus[i][j], start=all_focus[i][0], end=make_data.last_trade_date()[0])['p_change'].tolist()
            hist.reverse()

            for k in range(0, len(hist)):
                # 设定涨跌颜色
                if hist[k] > 0:
                    p_change_color = '<font color="#FF0000">'
                else:
                    p_change_color = '<font color="#00FF003">'
                f_change.write('<td width="100">%s%s</td>\n' % (p_change_color,hist[k]))
            f_change.write("</tr>\n")
        f_change.write("</table>\n")
        f_change.write('</p>\n')

    f_change.write("</body>\n</html>\n")
    f_change.close()

    log.write(log_file, "get old focus price change succeed!")


read_focus()