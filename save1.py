#########
# 计算豆子宝教育基金到期一共有多少钱
#########
import time
import datetime

## 一切的开始,从这一天开始给幼崽存教育金
THEDATE = '20081110'
ENDDATE = '20280101'


#####
# 传入一个日期，以及一个金额，本函数会自动计算该日期存入指定金额的5年期定期存款，自动转存时，到今天的账面余额（注意：未计算活期利息）
# 输入:date string YYYYmmdd 格式的存款日期；amount float 存款金额
# 返回:float 自动转存记复利的本息合计账面余额。（注：未包含本期的活期利息）
####

def calcMoney(date, amount, cDate='19880101'):
    if cDate == '19880101':
        today = time.localtime(time.time())
        year = today[0]
        month = today[1]
        day = today[2]

        txtYear = str(year)
        txtMonth = str(month)
        txtDay = str(day)

        if month < 10:
            txtMonth = '0' + txtMonth

        if day < 10:
            txtDay = '0' + txtDay
    else:
        year = int(cDate[0:4])
        month = int(cDate[4:6])
        day = int(cDate[-2])

        txtYear = cDate[0:4]
        txtMonth = cDate[4:6]
        txtDay = cDate[6:8]

    crDate = txtYear + txtMonth + txtDay

    tDay = str(year - 5) + txtMonth + txtDay  # 取得5年前今天的日期

    if date > tDay:  # 如这个日期在传入日期之前，则说明该笔存款还未到期，直接返回本金金额
        return amount
    else:
        sum = round(amount * (1 + getRate(date) * 5 / 100), 2)  # 计算5年后到期本息合计
        iyear = date[0:4]  # 取得年份
        nyear = str(int(iyear) + 5)
        ndate = date.replace(iyear, nyear)  # 取得5年后的日期
        nSum = calcMoney(ndate, sum, crDate)  # 用本次计算出的本息合计再次计算再5年后的本息合计，递归调用直到到期日超过当前日期
        return nSum  # 返回计算出的金额


# 利率表,key为利率生效日期，value为利率
# 注意：本利率表采集自中国银行网站,各商业银行执行利率在人民银行指导利率上下浮动，并不完全相同
rate = {
    '20151024': 2.75,
    '20150826': 3.05,
    '20150628': 2.15,
    '20150511': 3.75,
    '20150301': 2.65,
    '20141122': 4.25,
    '20120706': 4.75,
    '20120608': 5.1,
    '20110707': 5.5,
    '20110406': 5.25,
    '20110209': 3,
    '20101226': 4.55,
    '20101020': 4.2,
    '20081223': 3.6,
    '20081127': 3.87,
    '20081030': 5.13
}


####
# 根据传入的日期给出5年期存款的利率
# 传入 date：存款日期
# 返回：存款日期当期的5年期存款利率
####

def getRate(date):
    for i in rate:
        if i > date:
            continue
        else:
            return rate[i]


day = 10
total = 0
for year in range(2008, 2028):
    for month in range(1, 13):
        print('===================================================')

        txtYear = str(year)
        txtMonth = str(month)
        txtDay = str(day)

        if month < 10:
            txtMonth = '0' + txtMonth

        if day < 10:
            txtDay = '0' + txtDay

        txtDate = txtYear + txtMonth + txtDay

        if txtDate < THEDATE:
            print('手滑了！')
            continue
        if txtDate < '20191110':
            totalAmount = 1000
        else:
            totalAmount = 2000  # 本月缴纳总数

        s = calcMoney(txtDate, totalAmount, '20280101')
        total += s

        print(txtDate + '|' + str(totalAmount) + '|' + str(s))

print(str(total))
