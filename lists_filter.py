# coding:utf-8
import re
import json

# hadoop journal列表过滤器
def journal(seedhosts, port):
    newlist = []
    for i in seedhosts:
        newlist.append(i+':'+port)
    return ';'.join(newlist)

#生成一个双引号的transfer列表
def gentransferlist(seedhosts):
    return json.dumps(seedhosts.split(","))

#扩容时用来合并先前集群和当前列表中的ip地址,供配置文件使用
def ipstring(precluster, seedhosts):
    listip = []
    for i in precluster:
        listip.append(i.split(':')[0])
    return [i.encode("utf-8") for i in list(set(listip+seedhosts))]

#扩容时用来合并先前集群和当前列表中的ip和端口,供配置文件使用
def ipport(precluster, seedhosts, port):
    seedhostsport = []
    for i in seedhosts:
        i = i+':'+str(port)
        seedhostsport.append(i)
    return [i.encode("utf-8") for i in precluster+seedhostsport]

# 生成zk zoo.cfg文件中的server列表
def zkservers(preclusters, seedlists):
    preclusterslist = []
    for i in preclusters:
        preclusterslist.append(i.split(':')[0]+':'+i.split(':')[5]+':'+i.split(':')[6])
    return list(set(preclusterslist+seedlists))
# 生成kafka扩展时配置文件中bootstrapserver的列表
def kafkaboot(preclusters, seedlists):
    preclusterlist = []
    for i in preclusters:
        preclusterlist.append(i.split(':')[0]+':'+i.split(':')[4])
    return ','.join(list(set(preclusterlist+seedlists)))
# 生产flink配置文件中master列表
def flinkmaster(preclusters):
    preclusterlist = []
    masterlist = preclusters[0].split(':')[5].rstrip(']').lstrip('[')
    masterlist=masterlist.replace("'","").split(',')
    for i in masterlist:
        for j in preclusters:
            if j.split(':')[0]==i:
                preclusterlist.append(j)
    masters = []
    for i in preclusterlist:
        masters.append(i.split(':')[0]+':'+i.split(':')[4])
    return list(set(masters))
# 生成flink配置文件中的slave列表
def flinkslave(preclusters,seedlists):
    preclusterlist=[]
    slavelist = preclusters[0].split(':')[-3]
    for i in slavelist.split(','):
        preclusterlist.append(i)
    return list(set(preclusterlist+seedlists))
    
# 获取flink的jobmanip
def getflinkjobm(precluster):
    firsthost = precluster[0]
    return firsthost.split(':')[-2]
# 获取flink的jobmanip的user
def getflinkjobmuser(precluster,jobmip):
    for i in precluster:
        if i.split(':')[0]==jobmip:
            return i.split(':')[2]
        
def prehosts(precluster):
    preclu = []
    for i in precluster:
        preclu.append(i.split(':')[0].encode("utf-8"))
    return preclu
def prehostsutf8(precluster):
    preclu = []
    for i in precluster:
        preclu.append(i.encode("utf-8"))
    return preclu


def prehostsport(precluster):
    preclu = []
    for i in precluster:
        preclu.append(i.split(':')[0].encode("utf-8")+':'+str(i.split(':')[1]))
    return preclu
# 获取集群中第一个主机
def getfirsthost(preclusters):
    first = preclusters[0]
    return first.split(':')[0]
def getfirstuser(preclusters):
    first = preclusters[0]
    return first.split(':')[2]

### 按照IP地址过滤列表中对应条目的用户名和密码
def gethostuser(precluster, ips):
    return [user.split(':')[2] for user in precluster if ips in precluster][0]
def gethostpass(precluster, ips):
    return [user.split(':')[3] for user in precluster if ips in precluster][0]

###生成配置文件中用来设置集群ip列表的数据[192.168.1.1:111,192.168.1.2:222]
def gencluips(seedhosts):
    hosts=seedhosts[0]
    newseedhosts=[]
    for host in hosts.split(','):
        if host:
            newseedhosts.append(host.encode("utf-8"))
    return list(set(newseedhosts))

class FilterModule(object):
    def filters(self):
        return {
          'ipstring': ipstring,
          'ipport': ipport,
          'prehosts': prehosts,
          'prehostsutf8': prehostsutf8,
          'prehostsport': prehostsport,
          'getfirstuser': getfirstuser,
          'getfirsthost': getfirsthost,
          'gencluips': gencluips,
          'zkservers': zkservers,
          'kafkaboot': kafkaboot,
          'flinkmaster': flinkmaster,
          'flinkslave': flinkslave,
          'getflinkjobm': getflinkjobm,
          'getflinkjobmuser': getflinkjobmuser,
          'gethostuser': gethostuser,
          'gethostpass': gethostpass,
          'journal': journal,
          'gentransferlist': gentransferlist
        }
if __name__ == "__main__":
    a=prehosts([u'192.168.181.79:888:insuser:1234qwer:22', u'192.168.181.131:333:insuser:1234qwer:22', u'192.168.181.131:22', u'192.168.181.79:22'])
    print(a)
    b=flinkmaster(["192.168.1.1:22:sss:eee:888:192.168.1.11,192.168.1.2:192,168,1,1,192.168.1.2,192.168.1.3:/app","192.168.1.2:22:sss:eee:888:192.168.1.1,192.168.1.2:192.168.1.1,192.168.1.2,'192.168.1.3:/app","192.168.1.3:22:sss:eee:888:192.168.1.1,192.168.1.2,192.168.1.11:192.168.1.1,192.168.1.2,192.168.1.3:/app"])
    print(b)
    print(gentransferlist('192.168.181.129:58433,192.168.181.129:58434'))
