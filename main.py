#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from analyze import mean_deal
from datetime import *

if __name__ == "__main__":
    mean_deal_result = mean_deal.get_mean_deal()

    today_date = datetime.now().strftime("%Y-%m-%d")

    recode_file = open("stock_recode_"+ today_date,'w')

    mail_text = "请关注："
    for i in range(0,len(mean_deal_result)):
        mail_text += mean_deal_result[i]+","

    print >> recode_file,mail_text

    #send_mail.send_mail(mail_text)