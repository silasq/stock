import mean_deal
import tomorrow_sun
from datetime import *

today_date = datetime.now().strftime("%Y-%m-%d")

file_mean_deal = open("../focus/mean_deal_" + today_date, 'a+')

mean_deal_result = mean_deal.get_mean_deal()

#mail_text = "请关注："
#for i in range(0, len(mean_deal_result)):
#    mail_text += mean_deal_result[i] + ","

print >> recode_file, mail_text