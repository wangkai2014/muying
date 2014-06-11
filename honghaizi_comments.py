# -*- coding: utf-8 -*-
import os
import os.path
import sys
from Db import Db
import requests
from bs4 import BeautifulSoup
import re
import time
import re
import string
import subprocess
import json
import math
reload(sys)
sys.setdefaultencoding('utf-8')

db = Db()
req=requests.Session()

class HongHaiZi:
    count=0
    site_id=5
    items=[]
    listurl=''
    listname=''
    goodstotal=''
    groupid=0
    groupname=''
    source_urls = [
        'http://redbaby.suning.com/naifen.html',
        'http://redbaby.suning.com/zhiniaoku.html',
        'http://redbaby.suning.com/fushi.html',
        'http://redbaby.suning.com/yongpin.html',
        'http://list.suning.com/0-313119-0-0-0-9173.html',
        'http://redbaby.suning.com/tongche.html',
        'http://list.suning.com/0-315058-0-0-0-9173.html',
        'http://redbaby.suning.com/xihu.html',
        'http://redbaby.suning.com/mama.html'
    ]


    def __init__(self):
        pass

    def fetch_patch(self):
        self.groupid=6
        self.groupname='童车'
        self.listurl='http://list.suning.com/0-359503-0-0-1-9017.html'
        self.listname='健身车'
        self._parse_list(self.listurl)


    def fetch_naifen(self):
        self.groupid=1
        self.groupname='奶粉'
        soup=self._req(self.source_urls[0])
        subcat = soup.select('.sortOuter dl:nth-of-type(1) a')
        del subcat[5]
        for sub in subcat:
            self.listurl = sub.get('href')
            self.listname=sub.string
            self._parse_list(self.listurl)

    def fetch_zhiniao(self):
        self.groupid=2
        self.groupname='纸尿'
        soup=self._req(self.source_urls[1])
        for i in range(3):
            subcat = soup.select('.sortOuter dl:nth-of-type(i+1) a')
            for sub in subcat:
                self.listurl = sub.get('href')
                self.listname=sub.string
                self._parse_list(self.listurl)

    def fetch_fushi(self):
        self.groupid=3
        self.groupname='辅食'
        soup=self._req(self.source_urls[2])
        for i in range(2):
            subcat = soup.select('.sortOuter dl:nth-of-type(i+1) a')
            for sub in subcat:
                self.listurl = sub.get('href')
                self.listname=sub.string
                self._parse_list(self.listurl)

    def fetch_yongpin(self):
        self.groupid=4
        self.groupname='用品'
        soup=self._req(self.source_urls[3])
        subcat = soup.select('.sortOuter dl a')
        for sub in subcat:
            try:
                self.listurl = sub.get('href')
                self.listname=sub.string
                self._parse_list(self.listurl)
            except Exception,e:
                print e
                continue

    def fetch_wanju(self):
        self.groupid=5
        self.groupname='玩具'
        soup=self._req(self.source_urls[4])
        subcat = soup.select('#navBarConIndex dl dd a')
        for sub in subcat:
            try:
                self.listurl = sub.get('href')
                self.listname=sub.string
                self._parse_list(self.listurl)
            except Exception,e:
                print e
                self.listurl = 'http://list.suning.com/'+sub.get('href')
                self.listname=sub.string
                self._parse_list(self.listurl)
                continue

    def fetch_tongche(self):
        self.groupid=6
        self.groupname='童车'
        soup=self._req(self.source_urls[5])
        for i in range(2):
            subcat = soup.select('.sortOuter dl:nth-of-type(i+1) a')
            for sub in subcat:
                self.listurl = sub.get('href')
                self.listname=sub.string
                self._parse_list(self.listurl)

    def fetch_qinju(self):
            self.groupid=7
            self.groupname='寝居'
            soup=self._req(self.source_urls[6])
            subcat = soup.select('#navBarConIndex dl dd a')
            for sub in subcat:
                try:
                    self.listurl = sub.get('href')
                    self.listname=sub.string
                    self._parse_list(self.listurl)
                except Exception,e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print e
                    print(exc_type, fname, exc_tb.tb_lineno)
                    self.listurl = 'http://list.suning.com/'+sub.get('href')
                    self.listname=sub.string
                    self._parse_list(self.listurl)
                    continue

    def fetch_mama(self):
        self.groupid=8
        self.groupname='妈妈'
        soup=self._req(self.source_urls[7])
        for i in range(7):
            subcat = soup.select('.sortOuter dl:nth-of-type(i+1) a')
            for sub in subcat:
                self.listurl = sub.get('href')
                self.listname=sub.string
                self._parse_list(self.listurl)

    def fetch_xihu(self):
        self.groupid=9
        self.groupname='洗护'
        soup=self._req(self.source_urls[8])
        for i in range(3):
            subcat = soup.select('.sortOuter dl:nth-of-type(i+1) a')
            for sub in subcat:
                self.listurl = sub.get('href')
                self.listname=sub.string
                self._parse_list(self.listurl)

    def _parse_list(self,listurl):
        '''
        -0-1-9017 自营，送至北京
        '''
        print 'listurl..'+listurl
        soup=self._req(listurl)
        time.sleep(1)


        try:
            page=soup.select('#next')[0].get('href')
            listurls=[]
            print 'page...'+page
            if page.find('cityId')==-1:
                # pagepattern=re.search(r"(\d*-\d*-)\d*\.html",page).group(1)

                try:
                    pagepattern=re.search(r'\/(\d*-\d*-)\d-\d-\d-\d*(.*)','/'+page)
                    pageurl='http://list.suning.com/'+pagepattern.group(1)+str(0)+'-0-1'+'-9017'+pagepattern.group(2)
                except AttributeError:
                    pagepattern=re.search(r'\/(\d*-\d*-).*','/'+page)
                    pageurl='http://list.suning.com/'+pagepattern.group(1)+str(0)+'-0-1-9017.html'
                print 'init..'+pageurl
                soupfilter=self._req(pageurl)
                pagetotal=int(soupfilter.select('#pageTotal')[0].string)
                if pagetotal==1:
                    print 'only one page'
                    listurls.append(pageurl)
                else:
                    for i in range(pagetotal):
                        try:
                            pagepattern=re.search(r'\/(\d*-\d*-)\d-\d-\d-\d*(.*)','/'+page)
                            pageurl='http://list.suning.com/'+pagepattern.group(1)+str(i)+'-0-1-9017'+pagepattern.group(2)
                        except AttributeError:
                            pagepattern=re.search(r'\/(\d*-\d*-).*','/'+page)
                            pageurl='http://list.suning.com/'+pagepattern.group(1)+str(i)+'-0-1-9017.html'
                        listurls.append(pageurl)

                print listurls

                time.sleep(1)
                self.goodstotal=soupfilter.select('.searchKeyT i')[0].string

            else:
                pagepattern=re.search(r"(.*&cp=)",page).group(1)
                pageurl='http://search.suning.com/'+pagepattern+str(0)+'&iy=-1&ct=1&si=5'
                soupfilter=self._req(pageurl)
                pagetotal=int(soupfilter.select('#pageTotal')[0].string)
                if pagetotal==1:
                    print 'only one page'
                    listurls.append(pageurl)
                else:
                    for i in range(pagetotal):
                        pageurl='http://search.suning.com/'+pagepattern+str(i)+'&iy=-1&ct=1&si=5'
                        listurls.append(pageurl)
                print listurls

                time.sleep(1)
                self.goodstotal=soupfilter.select('.searchKeyT i')[0].string

        except Exception ,e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print e
            print(exc_type, fname, exc_tb.tb_lineno)
            return
            # subprocess.check_output(['python','/var/www/honghaizi/honghaizi.py'])

        self._insert_cat()
        self._fetch_list(listurls)
        self._insert_list()
        self.items=[]


    def _fetch_list(self,listurls):
        print listurls
        for url in listurls:
            soup=self._req(url)
            itemurlsoup=soup.select('.inforBg span a')
            itemtitlesoup=soup.select('.inforBg span p')
            for i in itemtitlesoup:
                item={}
                itemstr=re.search(r"<p>(.*)</p>",str(i)).group(1)
                itemstr=itemstr.replace('<em>',' ')
                itemstr=itemstr.replace('</em>','')
                itemstr=itemstr.replace('<b class="highlight">','')
                itemstr=itemstr.replace('</b>','')
                item['title']=itemstr
                item['url']=itemurlsoup[itemtitlesoup.index(i)].get('href')
                if item['url'].find('emall')!=-1:
                    item['url']=self._req(item['url']).select('.sim')[0].get('href')
                self.items.append(item)

    def _req(self,url):
        try:
            source=req.get(url,timeout=10)
        except requests.exceptions.MissingSchema:
            source=req.get('http://list.suning.com/'+url,timeout=10)
        except requests.exceptions.Timeout:
            print 'timeout'
            # os.system('python /var/www/honghaizi/honghaizi.py')
            return self._req(url)
            # os._exit(0)


        soup = BeautifulSoup(source.content)
        return soup

    def _insert_cat(self):

        cate_id=db.querycatid('goods_category')
        if db.exists('goods_category','category',self.listname)==0:
            sql="insert into goods_category values (null,'"+str(self.site_id)+"','"+str(self.groupid)+"','"+self.groupname+"','"+str(cate_id+1)+"','"+self.listname+"','"+self.listurl+"','"+str(self.goodstotal)+"','"+str(int(time.time()))+"',default)"
            db.execsql(sql)
            print "insert goods_category "+self.listname+'success'
            self.cate_id= cate_id+1
        else:
            print "goods_category "+self.listname+' exists'
            self.cate_id= cate_id

    def _insert_list(self):
        for item in self.items:
            if db.exists('goods_list','goods_url',item['url'])==0:
                sql="insert into goods_list values(null,'"+str(self.site_id)+"','"+str(self.groupid)+"','"+self.groupname+"','"+str(self.cate_id)+"','"+self.listname+"',default,default,default,'"+json.dumps(item['title'],ensure_ascii=False, encoding='utf8')+"','"+item['url']+"','"+str(int(time.time()))+"')"
                db.execsql(sql)
                print "insert goods_list "+item['title']+" "+item['url']+' success\n'
            else:

                print "goods_list "+item['title']+" "+item['url']+' exists\n'

    def fetchDetail(self):
        basicinfos=self._getGoodsBasic()

        for g in basicinfos:
            if db.exists('goods_detail','goods_url',g['goods_url'])==0:
                try:
                    self.goods_id=g['id']
                    self.goods_name=g['goods_name']
                    self.group_name=g['group_name']
                    self.site_id=g['site_id']
                    self.category=g['category']
                    # self.goods_url='http://product.suning.com/0000000000/102295658.html'
                    self.goods_url=g['goods_url']
                    self.headers={
                        'referer': self.goods_url,
                        'X-Requested-With':	'XMLHttpRequest',
                        'User-Agent':	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
                        'Host':	'product.suning.com',
                        'Accept':	'application/json, text/javascript, */*; q=0.01',
                    }
                    content=requests.get(self.goods_url).content.replace('\n','')
                    sn=re.search(re.compile(r"var sn=sn\|\|(\{.*?\})",re.MULTILINE),content)
                    sn=eval(sn.group(1))
                    self.storeId=sn['storeId']
                    self.langId=sn['langId']
                    self.catalogId=sn['catalogId']
                    self.cityId=str(9017)
                    self.productId=sn['productId']
                    self.partNumber=sn['partNumber']
                    self.context=sn['context']
                    # self._queryTest()
                    self._queryVendor()
                    self._queryProm()
                    self._querySale()
                    self._queryParams()
                    self._querySelect()
                    self._insertDetail()
                    self._insertPrice()
                except SyntaxError:
                    continue
                except AttributeError:
                    continue
            else:
                print 'goods_detail existd......'
                continue

            # os._exit(0)

    def _queryTest(self):
        url="http://product.suning.com/" + self.context + "/csl_" + self.storeId + "_" + self.catalogId + "_" + self.productId + "_" + self.partNumber + "_" + self.cityId + "_.html"
        print url
        test=eval(req.get(url,headers=self.headers).content)
        print self.goods_url
        print json.dumps(test,ensure_ascii=False, encoding='utf8'),'\n'
    def _getGoodsBasic(self):

        sql="select id,site_id,group_name,category,goods_id,goods_name,goods_url from goods_list where group_name like '%辅食%'"
        return db.query(sql)

    def _queryVendor(self):
        url='http://product.suning.com/SNProductStatusView?storeId='+self.storeId+'&catalogId='+self.catalogId+'&productId='+self.productId+'&langId='+self.langId+'&partNumber='+self.partNumber+'&cityId='+self.cityId
        print url
        vendors=eval(req.get(url,headers=self.headers).content)
        self.vendor=vendors['vendor']
        self.snPrice=vendors['netPrice']
        self.salesOrg=vendors['salesOrg']
        self.deptNo=vendors['deptNo']
        print vendors

    def _queryProm(self):
        url='http://product.suning.com/SNProductPromStatusView?storeId='+self.storeId+'&catalogId='+self.catalogId+'&productId='+self.productId+'&langId='+self.langId+'&partNumber='+self.partNumber+'&salesOrg='+self.salesOrg+'&deptNo='+self.deptNo+'&vendor='+self.vendor+'&price='+self.snPrice+'&cityId='+self.cityId
        print 'prom...'+url
        try:
            proms=eval(req.get(url,headers=self.headers).content)
            self.couponOrder=proms['couponProduct']
            self.sgPrice=proms['sgPrice']
            self.voucher=proms['voucher']
        except:
            self.couponOrder=''
            self.sgPrice=''
            self.voucher=''

    def _querySale(self):
        url='http://product.suning.com/SNProductSaleView?storeId='+self.storeId+'&catalogId='+self.catalogId+'&productId='+self.productId+'&langId='+self.langId+'&partNumber='+self.partNumber+'&salesOrg='+self.salesOrg+'&deptNo='+self.deptNo+'&vendor='+self.vendor+'&price='+self.snPrice+'&cityId='+self.cityId
        sales=eval(req.get(url,headers=self.headers).content)
        self.productStatus=sales['productStatus']
        self.qgPrice=sales['qgPrice']
        self.shipOffSetText=sales['shipOffSetText']


    def _queryParams(self):
        self.param={}
        soup=self._req(self.goods_url)
        print self.goods_url
        keys=soup.select('.Imgpip span')
        values=soup.select('.td1')

        for i in range(len(keys)):
            k=keys[i].string.replace(' ','').replace('：','')
            v=values[i].string.replace(' ','')
            self.param[k]=v
        try:
            self.brand=self.param[u'品牌']
        except:
            print 'this product has not params'
            self.brand=''
            self.param=''

    def _querySelect(self):
        self.select={}
        soup=self._req(self.goods_url)
        try:
            versions=soup.select('#versionItemList li span')
            colors=soup.select('#colorItemList li img')
            vlist=[]
            clist=[]
            for v in versions:
                vlist.append(v.string)
            if vlist!=[]:
                self.select['versions']=vlist
            for c in range(colors):
                clist.append(c.get('alt'))
            if clist!=[]:
                self.select['colors']=clist

        except Exception,e:
            pass
        finally:
            if self.select=={}:
                self.select=''
            print self.select

    def _insertDetail(self):
        print '返券'+str(self.couponOrder)
        try:
            if self.couponOrder!=[]:
                self.couponOrder='返券:'+self.couponOrder[0]['name']+'  '
            else:
                self.couponOrder=''
        except:
            self.couponOrder=''
        try:
            if self.sgPrice!='-1':
                self.sgPrice='折扣价:'+str(self.sgPrice)+'  '
            else:
                self.sgPrice=''
        except:
            self.sgPrice=''
        try:
            if self.voucher!=[]:
                self.voucher='促销信息:'+str(self.voucher[0]['name'])+'  '
            else:
                self.voucher=''
        except:
            self.voucher=''

        self.shipOffSetText=self.shipOffSetText.replace("<em class='g_color'>",'').replace("</em>",'').replace("<span>",'').replace("</span>",'')
        goods_discount=self.couponOrder+str(self.sgPrice)+str(self.voucher)+str(self.qgPrice)+str(self.shipOffSetText)
        print self._filtercolumn(goods_discount)
        try:
            sql="insert into goods_detail values (null,'"+str(self.site_id)+"','"+self.group_name+"','"+self.category+"',default,'"+self.brand+"','"+str(self.goods_id)+"','"+self.goods_name.strip('"')+"','"+self._filtercolumn(goods_discount)+"','"+self.goods_url+"','','"+self._filtercolumn(self.param)+"','"+self._filtercolumn(self.select)+"','"+str(int(time.time()))+"')"
            if db.exists('goods_detail','goods_url',self.goods_url)==0:
                db.execsql(sql)
                print 'insert detial success'
            else:
                print 'goods already exist'
        except Exception,e:
            print 'insert detail fail...'
            print e

    def _insertPrice(self):
        print self.snPrice
        try:
            if db.exists('goods_price','goods_id',self.goods_id)==0:
                sql="insert into goods_price values(null,'"+str(self.site_id)+"','"+str(self.goods_id)+"','"+self.snPrice+"','"+str(int(time.time()))+"')"
                db.execsql(sql)
                print 'insert price success'
            else:
                print 'price already exist'
        except:
            print 'insert price fail...'
        self.count+=1
        print self.count

    def _filtercolumn(self,c):
        c=json.dumps(c,ensure_ascii=False, encoding='utf8')
        return c.replace("'",'"').strip('"')

    def fetch_comment(self):
        goods=self._getGoodsBasic()
        for g in goods:
            self.goods_id=g['id']
            self.goods_name=g['goods_name']
            soup=self._req(g['goods_url'])
            content=requests.get(g['goods_url']).content.replace('\n','')
            sn=re.search(re.compile(r"var sn=sn\|\|(\{.*?\})",re.MULTILINE),content)
            sn=eval(sn.group(1))
            part_num=sn['partNumber']
            more_url='http://zone.suning.com/review/product_review/'+str(part_num)+'-0-1--.html'
            soup=self._req(more_url)
            total_comment=soup.select('.cur span')[0].string.strip('（').strip('）')
            print more_url,g['goods_url']
            for i in range(int(math.ceil(int(total_comment)/7))):

                url='http://zone.suning.com/review/ajax/wcs_review/'+str(part_num)+'-0-'+str(i+1)+'-null--0-pingJiaTotal.html?callback=jQuery17202263880749233067_'+str(int(time.time()))
                print 'comment page..'+url
                content=json.loads(req.get(url).content.strip('pingJiaTotal(').strip(')'))
                for review in content['productReviewList']:
                    try:
                        self.avator=review['fullFaceImage']
                    except:
                        self.avator=''
                    try:
                        self.username=review['logonId']
                    except:
                        self.username=''
                    try:
                        self.userid=review['cmfUserId']
                    except:
                        self.userid=''
                    try:
                        self.ordertime=int(time.mktime(time.strptime(review['orderTime'],'%Y-%m-%d %H:%M:%S')))
                    except:
                        self.ordertime=''
                    try:
                        self.reviewtime=int(time.mktime(time.strptime(review['reviewTime'],'%Y-%m-%d %H:%M:%S')))
                    except:
                        self.reviewtime=''
                    try:
                        self.commentcontent=review['content']
                    except:
                        self.commentcontent=''
                    try:
                        self.score=review['qualityStar']
                    except:
                        self.score=''
                    print self.ordertime,self.reviewtime
                    self._insert_comment()

    def _insert_comment(self):
        if db.exists1('goods_comments','goods_id',self.goods_id,'com_u_name',self.username)==0:
            try:
                sql="insert into goods_comments values (null,'"+str(5)+"','"+str(self.goods_id)+"','"+self.goods_name+"','"+str(self.score)+"','"+str(self.userid)+"','"+self.username+"','"+self.avator+"','','','"+self.commentcontent+"','"+str(self.reviewtime)+"','"+str(self.ordertime)+"','')"
                db.execsql(sql)
                print 'insert comments success'
            except:
                print 'insert comment fail'
        else:
            print "comment exists"

if __name__ == '__main__':
    h = HongHaiZi()
    # h.fetch_naifen()
    # h.fetch_fushi()
    # h.fetch_yongpin()
    # h.fetch_wanju()
    # h.fetch_tongche()
    # h.fetch_qinju()
    # h.fetch_zhiniao()
    # h.fetch_patch()
    # h.fetchDetail()
    h.fetch_comment()
    # h.fetch_mama()
    # h.fetch_xihu()