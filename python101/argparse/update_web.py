import argparse
import os,shutil
import requests
from bs4 import BeautifulSoup as bs
import json as js
import numpy as np
import time
from tqdm import tqdm

def get_abs(url):
    """
    get abstract from an url of a article from arxiv/nature/science

    Parameters
    ----------
    url: str
        url of article
    
    Returns:
    ----------
    abstract: str
    """
    
    try:
        res=requests.get(url)
    except:
        print('!!!! connection failed.')
        abstract, index = 'connection failed', '000.000'
        return abstract, index
    
    soup=bs(res.text,features="html.parser")
    absls=[] # 从一个以上的标签中获取文章摘要.其中一种方式是获取页面上显示的摘要

    if 'arxiv' in url:
        # 获取摘要方法1
        for row in soup.find_all('row'):
            if row.get('name') == 'citation_abstract':
                abstract=(' '.join(row.get('content').split('\n'))).strip(' ') # substitute '\n' with ' '. may be ''
                absls.append(abstract)

        # 获取摘要方法2
        for row in soup.find_all('blockquote'):
            rowclass=row.get('class')
            if rowclass==None: continue
            if 'abstract' in rowclass:
                #abs_row=rows
                abscontent=row.contents[2] # get abstract content from 'blockquote' tag
                abstract=(' '.join(abscontent.split('\n'))).strip(' ') # substitute '\n' with ' '
                absls.append(abstract)

        # 获取文章编码
        index=url.split('/')[-1]
        
    elif 'nature' in url:
        # 获取摘要,方法1
        for row in soup.find_all('div'):
            row_id=row.get('id')
            if row_id=='Abs1-content':
                # type(row) # 是tag类型
                row_ptag=[x for x in row.p.contents if not '<' in str(x)] # 把含摘要内容的标签里的一些非摘要部分去出掉, 只留摘要部分
                abstract=''.join(row_ptag) # may be ''
                absls.append(abstract)

        # 获取摘要,方法2
        for row in soup.find_all('script'):
            if row.get('type')=='application/ld+json':
                # type(row) # 是tag类型
                json_str=js.loads(row.string)
                abstract=json_str['mainEntity']['description'] # may be ''
                absls.append(abstract)
        
        volls,pagels=[],[]
        
        # 获取卷数和页数
        for row in soup.find_all('p'):
            row_class = row.get('class')
            if row_class == None: continue
            if "c-article-info-details" in row.get('class'):
                children=list(row.descendants)
                for idx, child in enumerate(children):
                    if child == None: continue
                    if str(child) == 'volume':
                        vol=str(int(children[idx+1]))
                        volls.append(vol)
                    if str(child).strip(' ') == 'pages':
                        page=str(children[idx+1]).split('–')[0]  #与众不同的分隔符233
                        pagels.append(page)

        # 获取卷数和页数方法2
        for row in soup.find_all('meta'):
            row_name = row.get('name')
            if row_name == None: continue
            if row_name == "prism.volume": 
                vol=row.get('content')
                volls.append(vol)
            if row_name == "prism.startingPage":
                page=row.get('content')
                pagels.append(page)
        
        # 判断获取的卷数和页数是否有效, 无效则返回000.000
        for idx,vol in enumerate(volls):
            if vol != '' and vol != None:
                volume = vol
                break
            elif idx==len(volls)-1:
                volume = '000'
            else:
                pass
        
        for idx,pag in enumerate(pagels):
            if pag != '' and pag != None:
                page = pag
                break
            elif idx==len(pages)-1:
                page = '000'
            else:
                pass
        
        index=volume+'.'+page
    
    elif 'science' in url:
        # 获取摘要方法
        for row in soup.find_all('div'):
            row_id=row.get('id')
            #print(row_name)
            if row_id == None: continue
            if row_id == 'abstracts':
                sections=row.find_all('section')
                for sec in sections:
                    sec_id = sec.get('id')
                    if sec_id == None: continue
                    if sec_id == 'abstract':
                        abstract = ''.join([str(x) for x in sec.find('div').contents])
                        absls.append(abstract)
        
        # 获取卷数和页数
        for row in soup.find_all('div'):
            row_class = row.get('class')
        #     print(row_class)
            if row_class == None: continue
            if 'self-citation' in row_class:
                vol,iss,page='000','000','000'
                for item in row.find_all('span'):
                    prop = item.get('property')
                    if prop == None: continue
                    if 'volumeNumber' in prop:
                        vol = str(item.string)
                    if 'issueNumber' in prop:
                        issue = str(item.string)
                    try:
                        if 'pageStart' in prop:
                            page = str(item.string)
                    except:
                        page = '000'
                try:
                    index=vol+'.'+issue+'.'+page
                except:
                    index='000.000'

    else:
        absls.append('article websit unknow')
        index='000.000'

    # 判断以各自不同方式获取的摘要是否有效, 无效则返回'abstract not found'
    for idx,abstract in enumerate(absls):
        if abstract != '' and abstract != 'article websit unknow' and abstract != None:
            return abstract, index
            break
        elif abstract == 'article websit unknow':
            return abstract, index
            break
        elif idx==len(absls)-1:
            abstract = 'abstract not found'
            return abstract, index
        else:
            pass
    

def appendjs(newfile, objfile):
    """
    append the contents of new json file to an existed json file
    
    Parameters:
    ----------
    newfile : new json file, str
        new contents to append.
    objjls : existed json file, str
        existed file to be appended.

    Returns:
    -------
    None.

    """
    
    # 打开新json文件, 为其添加摘要和文章编码等信息
    with open(newfile,'r') as nf:
        njs=js.load(nf)
        for artdict in tqdm(njs): # 每个json文件一个进度条
            abstract, index=get_abs(artdict['article link'])
            artdict['abstract']='\\"'.join(abstract.split('"')) # 在摘要字符串中可能存在的双引号前面加一个反斜杠
            artdict['index']=index

    # 判断待并入的json文件是否存在, 否则创建一个, 并写入新文件的内容.
    if os.path.exists(objfile):
        #print('yes')
        with open(objfile,'r') as of:
            ojs=js.load(of)

        #print(len(ojs+njs))
        with open(objfile,'w') as of:
            js.dump(ojs+njs, of, ensure_ascii=False, indent=4)
    else:
        with open(objfile,'w') as of:
            js.dump(njs, of, ensure_ascii=False, indent=4)


if __name__== '__main__': 
    

    parser = argparse.ArgumentParser(prog='update_web', description='appending new json files and generate html.')
    parser.add_argument('-f', '--file', nargs='+', dest='files', help='json file list')
    parser.add_argument('-t', '--threshold', nargs='?', dest='thres', const='30', default='30',type=int, help='threshold in minute for new jsonfile detection')
    args = parser.parse_args()
    files = args.files
    threshold = 10*args.thres

    if files == None:
        # 检测当前文件夹下过去一定分钟(默认30分钟,通过-t设定)内新增的json文件, 并添加其内容到整合的json文件中
        jslist=np.array([str(file) for file in os.listdir('./') if 'json' in file and not 'article' in file])

        ctime=np.array([os.path.getctime(x) for x in jslist]) # 检测创建日期
        age=time.time()-ctime
        newjs = jslist[(age < threshold)]
    
    else:
        # 若指定了json列表文件
        if '@' in files[0]:
            with open(files[0][1:],'r') as jsls:
                newjs = np.array([x.strip('\n') for x in jsls.readlines()])
        else:
            newjs = np.array(files)

    jsdate=[int(jsfile.split('_')[0]) for jsfile in newjs]
    newjs=list(newjs[np.argsort(jsdate)]) # 按日期从老到新排序
    
    if len(newjs) == 0:
        print('No newjs found in last {} mins!'.format(threshold))
        exit
    #print(newjs)

    for jsf in newjs:
        if jsf=='articles.json': continue
        # 检测是否需要修改json文件(格式错误)
        try:
            js.load(open(jsf,'r'))
            open(jsf,'r').close()
        except:
            newf = open(jsf,'r')
            lines = newf.readlines()

            newlines=[]
            nerr=0
            for line in lines:
                if 'title' in line:
                    title=':'.join(line.split(':')[1:]).strip(' ",\n')
                    if '\\' in title or '"' in title: nerr+=1
                    title='\\\\'.join(title.split('\\'))
                    title='\\"'.join(title.split('"'))     
                    newlines.append('"title":"{}",\n'.format(title))
                    continue
                if 'comment' in line:
                    com=':'.join(line.split(':')[1:]).strip(' ",\n')
                    if '\\' in com or '"' in com: nerr+=1
                    com='\\\\'.join(com.split('\\'))
                    com='\\"'.join(com.split('"'))     
                    newlines.append('"comment":"{}",\n'.format(com))
                    continue
                newlines.append(line)
            print('!!!!!! typo:{}'.format(nerr))
            if nerr > 0:
                shutil.copyfile(jsf,'typo_'+jsf) # 如果有错误格式的文件, 复制一份原文件
                with open(jsf,'w') as new1f:
                    new1f.writelines(newlines)
        # 检测结束
        print('appending json file:{}'.format(jsf))
        appendjs(jsf, 'articles.json')


    with open('articles.json', 'r') as artf:
        artjs=js.load(artf)

    head='''<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>文献泛读记录</title>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async
                src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
        </script>
    </head>

    <body>
        <div id="content">
            <div id="dlpage">
            <h1>文献泛读记录</h1>
            <dl>'''

    tail='''
            </dl>
        </div>
    </body>

    </html>'''

    body=''

    i=0
    for arti in artjs[::-1]:
        i+=1
        title=arti['title']
        a_type=arti['type']
        comment=arti['comment']
        link=arti['article link']
        note=arti['local note']
        ex_link=arti['external links']
        abstract=arti['abstract']
        index=arti['index']
        if 'arxiv' in link: ori='arXiv'
        if 'nature' in link: ori='Nature'
        if 'science' in link: ori='Science'
        body+='''
                    <dt>
                        <a name="item1">[{}]</a>&nbsp;
                        <span class="list-identifier">
                            <a href="{}" title="Abstract">{}:{}</a>
                            [
                            <a href="./{}" title="Note">{}</a>,
                            <a href="{}" title="Other notes">other note</a>
                            ]
                        </span>
                    </dt>
                    <dd>
                        <div class="mata">
                            <div class="list-title mathjax">
                                <font size="5" face="arial">
                                <b>{}</b>
                                </font>
                            </div>
                            <div class="list-comments mathjax">
                                <span class="descriptor">Comments:</span>
                                {}           
                            </div>
                            <div class="list-type">
                                <span class="descriptor">Type:</span>
                                {}           
                            </div>
                            <p class="mathjax" style="color:rgb(0, 0, 0, 0.7)">
                                {}
                            </p>
                        </div>
                    </dd>'''.format(i, link, ori, index, note, note, ex_link, title, comment, a_type, abstract)

    with open('article_list.html','w') as w:
        w.write(head+body+tail)
