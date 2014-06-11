# from ghost import Ghost
# ghost = Ghost()
# page, resources = ghost.open('http://baidu.com')
# result, resources = ghost.evaluate("console.log(sn)")
# print result,resources
import spynner
#
browser = spynner.Browser()
browser.load("http://www.baidu.com")
print browser.runjs("console.log('I can run Javascript!')",debug =True)
browser.close()

# from selenium import webdriver
#
# browser = webdriver.Firefox()
# browser.get('http://seleniumhq.org/')

set GOROOT=E:\go
set GOBIN=$GOROOT\bin
set GOPATH=E:\wamp\apache\htdocs\go
set PATH=%PATH%;$GOBIN;$GOPATH