# appleid_unblocker
一套使用imap配合selenium自动解锁appleid的系统
##使用步骤
1. 安装自行对应平台chromedriver，chrome
2. EmailManager 负责读取邮箱内的未读解锁邮件，并读取邮件内的解锁url调用unblocker类使用无头浏览器进行解锁，
你需要自行修改 unblocker.py里面的path to chromedriver,并且自定义EmaiManager.py里面的设置
3. 可以用crontab 定时运行，系统解锁成功则会自动标记邮件为已读
##To-do
1. 目前只能被动的接受邮箱解锁邮件来解锁，计划支持自动check 账户可用性并自动进行解锁
2. 多账号支持

其实代码很简单，自己改改就ok了 :)

