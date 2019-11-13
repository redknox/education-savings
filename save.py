#########
# 定时提醒我自己给豆子宝存钱
# 1、每月10日发送企业微信消息给我
# 2、如果5年之前相同的月份忘了存，那么5年后加上利息补上！
#########
import time
import datetime

## 一切的开始
THEDATE = '20081124'


#####
# 传入一个日期，以及一个转存次数，计算在该日期，5年期存款到期自动转存N次后，账面现金余额。
# 例如：calMoney('20191111',2,amount=5000),表示如果在2004年11月11日，存入5000元，到2019年11月11日期满账面余额
# 输入：date 计算的日期，这个日期会影响取到的之前自动转存时的利率值；count 自动转存次数：0表示没有自动转存，1表示自动转存一次，以此类推。ammount:存款金额
####

def calcMoney(date, ammount=1000):
    today = time.localtime(time.time())
    year = today[0]
    month = today[1]
    day = today[2]
    tDay = str(year - 5) + str(month) + str(day)

    if date > tDay:
        return ammount;
    else:
        sum = round(ammount * (1 + findRate(date) * 5 / 100), 2)  # 用5年前到期的账户余额，计算本次到期的本息合计
        iyear = date[0:4]  # 取得年份
        nyear = str(int(iyear) + 5)
        ndate = date.replace(iyear, nyear)  # 取得5年前的日期
        nSum = calcMoney(ndate, sum)  # 递归调用函数本身，计算5年前到期时的账户余额
        return nSum  # 返回账户余额


# 利率表,key为利率生效日期，value为利率
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
    '201504',
    '201507',
    '201509',
    '201811',
    '201812'
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

def findRate(date):
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

totalAmount = 2000  # 本月缴纳总数

# 存本月的钱
print("今天是", str(year), "年", str(month), "月", str(day), '日,记得给豆子宝存', totalAmount, '米教育基金哦！')

years = 5  # 今年与之前存款年份的差值
tDay = str(year - years) + str(month) + str(day)  # 需要缴存的日期的文本日期
while (tDay > THEDATE):  # 如果日期大于教育金起存日期，则要检查当月是否已经缴存，和是否有退款
    tMonth = str(year - years) + str(month)  # 取得月份
    itamount = 1000
    if tMonth > '201812':  # 如果月份为2019年以后，那么补缴金额基数为2000
        itamount = 2000
    if tMonth not in saveMonth:  # 如果没存，那么提示
        s = calcMoney(tDay, itamount)
        print(years, "年前的", month, "月你没有给豆子宝存钱，今天要存", s, "元补上！")
        totalAmount += s

    if tMonth in payBack:  # 如果本月有退款，则提示
        print(years, "年前的本月你为豆子宝补存了教育基金，可以拿出来", payBack[tMonth], "！")

    years += 5
    tDay = str(year - years) + str(month) + str(day)
print("合计：", totalAmount, "元。")
