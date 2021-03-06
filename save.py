#########
# 提醒给幼崽存教育储蓄，如果之前有忘存的、本月到期的，则按照本息合计补存
# 等幼崽上了大学，直接把这个存折给幼崽，生活费就不再给了。
#########
import time
import datetime

## 一切的开始,从这一天开始给幼崽存教育金
THEDATE = '20081124'


#####
# 传入一个日期，以及一个金额，本函数会自动计算该日期存入指定金额的5年期定期存款，自动转存时，到今天的账面余额（注意：未计算活期利息）
# 输入:date string YYYYmmdd 格式的存款日期；amount float 存款金额
# 返回:float 自动转存记复利的本息合计账面余额。（注：未包含本期的活期利息）
####

def calcMoney(date, amount=1000, cDate='19880101'):
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

    tDay = str(year - 5) + txtMonth + txtDay  # 取得5年前今天的日期

    if date > tDay:  # 如这个日期在传入日期之前，则说明该笔存款还未到期，直接返回本金金额
        return amount
    else:
        sum = round(amount * (1 + getRate(date) * 5 / 100), 2)  # 计算5年后到期本息合计
        iyear = date[0:4]  # 取得年份
        nyear = str(int(iyear) + 5)
        ndate = date.replace(iyear, nyear)  # 取得5年后的日期
        nSum = calcMoney(ndate, sum)  # 用本次计算出的本息合计再次计算再5年后的本息合计，递归调用直到到期日超过当前日期
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
# 表内月份正常缴存了教育金
saveMonth = {
    '200811',
    '200903',
    '200904',
    '200905',
    '200906',
    '200907',
    '200908',
    '200912',
    '201001',
    '201002',
    '201003',
    '201004',
    '201005',
    '201009',
    '201010',
    '201011',
    '201012',
    '201101',
    '201102',
    '201208',
    '201209',
    '201210',
    '201211',
    '201212',
    '201301',
    '201302',
    '201303',
    '201304',
    '201305',
    '201401',
    '201402',
    '201403',
    '201404',
    '201405',
    '201406',
    '201407',
    '201408',
    '201410',
    '201412',
    '201501',
    '201502',
    '201503',
    '201504',
    '201505',
    '201507',
    '201509',
    '201811',
    '201812',
    '201911',
    '201912',
    '202001',
    '202002',
    '202003',
    '202004',
    '202005'
}

# 表内月份补存了之前的教育金，为了确保每月有定存到期，将这些补缴取出
payBack = {
    '200901': 2920.5,
    '200903': 1460.25,
    '200912': 3540.0,
    '201008': 3540.0,
    '201202': 2550.0,
    '201208': 2475.0,
    '201312': 8662.5,
    '201402': 6187.5,
    '201503': 5000.0,
    '201508': 3000.0
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


## 取得当前时间

today = time.localtime(time.time())
year = today[0]
month = today[1]
day = today[2]

year = 2020
month = 4
day = 10

for year in range(2020, 2028):
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

        totalAmount = 2000  # 本月缴纳总数

        print("今天是", txtYear, "年", txtMonth, "月", txtDay, '日,记得给豆子宝存', totalAmount, '米教育基金哦！')

        years = 5  # 存期为5年期
        tDay = str(year - years) + txtMonth + txtDay  # 需要缴存的日期的文本日期
        while (tDay > THEDATE):  # 如果日期大于教育金起存日期，则要检查当月是否已经缴存，和是否有退款
            tMonth = str(year - years) + txtMonth  # 取得月份
            itamount = 1000
            if tMonth > '201810':  # 如果月份为201811以后，也就是在教育储蓄满10年后，开始存2000
                itamount = 2000
            if tMonth not in saveMonth:  # 如果没存，那么提示
                s = calcMoney(tDay, itamount, txtDate)
                print(years, "年前的", month, "月你没有给豆子宝存钱，今天要存", s, "元补上！")
                totalAmount += s

            if tMonth in payBack:  # 如果本月有退款，则提示
                print(years, "年前的本月你为豆子宝补存了教育基金，可以拿出来", payBack[tMonth], "！")

            years += 5
            tDay = str(year - years) + txtMonth + txtDay
        print("合计：", totalAmount, "元。")
