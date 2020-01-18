# -*- coding: utf-8 -*-
import configparser, falcon, os, logging, pytz, datetime, json, pdfkit, markdown, random, string
from orator import DatabaseManager, Model
from weasyprint import HTML

head = """
        <style>
 

    body {
        font-family: 'Open Sans', sans-serif;
        font-weight: normal;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ff8800;
        font-weight: 900;
        
    }
    h1 {
        font-size: 250%;
        font-family: 'Politics Head', sans-serif;
    }
    h2 {
        font-size: 200%;
    }
    h3 {
        font-size: 160%;
    }
    h4 {
        font-size: 140%
    }
    h5 {
        font-size: 120%;
    }
    h6 {
        font-size: 100%;
    }
    blockquote {
        margin-left: 30px;
        padding: 3px;
        background: #FFE1BF;
        border-left: 2px solid #ff8800;
        }
    img {
        margin: auto;
        display: block;
        max-width: 70%;
    }
    a, a:active, a:hover, a:visited {
        color: #ff8800;
    }
    
    </style>
    """

def convertMarkdownToHtml(md):
    return markdown.markdown(md, encoding="utf-8")

def makePdfFromHtml(self, html, title):
    options = {
        'page-size': 'A4',
        'margin-top': '15mm',
        'margin-right': '15mm',
        'margin-bottom': '25mm',
        'margin-left': '25mm',
        'encoding': "UTF-8",

        'no-outline':None,
        'title': title
        }
    #path_wkthmltopdf = wkhtmltopdf_path
    #config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    config = pdfkit.configuration()


    return pdfkit.from_string(self.head+html, False)#, configuration=config, options=options)

def randomString(stringLength=30):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))




class MarkdownToPdf():
    def on_post(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # reading config
        config = configparser.ConfigParser()
        config.readfp(open('config.ini'))
        dbhost = config.get('database', 'host')
        dbdatabase = config.get('database', 'database')
        dbuser = config.get('database', 'user')
        dbpassword = config.get('database', 'password')
        prefix = config.get('database', 'prefix')
        wkhtmltopdf_path = config.get('wkhtmltopdf', 'path')
        baseurl = config.get('frontend', 'baseurl')

        #Setup DB
        config = {
            'mysql': {
                'driver': 'mysql',
                'host': dbhost,
                'database': dbdatabase,
                'user': dbuser,
                'password': dbpassword,
                'prefix': ''
            }
        }

        
        #TODO create tables 

        db = DatabaseManager(config)
        Model.set_connection_resolver(db)
        

        data = {"status": "failure", "data": {}}
        try:
            title = req.params['title']
            data = {"status": "success", "data": {}}      
        except:
            title = ''
        try:
            md = req.params['markdown']  
            data = {"status": "success", "data": {}}      
        except:
            data = {"status": "failure", "data": {}}
            md = False

        

        if md != False:
            md = head+convertMarkdownToHtml(md)
            key = datetime.datetime.now().strftime("%Y-%m-%d_")+randomString()

            file_ = HTML(string=md).write_pdf()

            

            try:
                db.table(prefix+'files').insert({
                    'file_key': key,
                    'file': file_
                })
                data = {"status": "success", "data": {"key": key, "url": baseurl+key}}
            except Exception as e:
                print(e)
                data = {"status": "failure", "data": {}}
                resp.status = falcon.HTTP_503
                return
        
        else: 
            data = {"status": "failure", "data": {}}
        resp.body = json.dumps(data) 

class GetFile():
    def on_get(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        # reading config
        config = configparser.ConfigParser()
        config.readfp(open('config.ini'))
        dbhost = config.get('database', 'host')
        dbdatabase = config.get('database', 'database')
        dbuser = config.get('database', 'user')
        dbpassword = config.get('database', 'password')
        prefix = config.get('database', 'prefix')
        wkhtmltopdf_path = config.get('wkhtmltopdf', 'path')
        baseurl = config.get('frontend', 'baseurl')

        #Setup DB
        config = {
            'mysql': {
                'driver': 'mysql',
                'host': dbhost,
                'database': dbdatabase,
                'user': dbuser,
                'password': dbpassword,
                'prefix': ''
            }
        }

        db = DatabaseManager(config)
        Model.set_connection_resolver(db)

        try:
            key = req.params['key']
            data = {"status": "success", "data": {}}      
        except:
            resp.status = falcon.HTTP_404
            return

        try:
            val = db.table(prefix+'files').where('file_key', key).first()
        except: 
            esp.status = falcon.HTTP_503
            return


        try: 
            resp.set_header("Content-Disposition", "attachment; filename="+key+".pdf")
            resp.data = val['file']
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_404

class CheckFile():
    def on_get(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        # reading config
        config = configparser.ConfigParser()
        config.readfp(open('config.ini'))
        dbhost = config.get('database', 'host')
        dbdatabase = config.get('database', 'database')
        dbuser = config.get('database', 'user')
        dbpassword = config.get('database', 'password')
        prefix = config.get('database', 'prefix')
        wkhtmltopdf_path = config.get('wkhtmltopdf', 'path')
        baseurl = config.get('frontend', 'baseurl')

        #Setup DB
        config = {
            'mysql': {
                'driver': 'mysql',
                'host': dbhost,
                'database': dbdatabase,
                'user': dbuser,
                'password': dbpassword,
                'prefix': ''
            }
        }

        db = DatabaseManager(config)
        Model.set_connection_resolver(db)

        try:
            key = req.params['key']
            data = {"status": "success", "data": {}}      
        except:
            resp.status = falcon.HTTP_404
            return

        try:
            val = db.table(prefix+'files').where('file_key', key).count()
        except: 
            resp.status = falcon.HTTP_503
            return

        if val > 0:
            try: 
                resp.body = json.dumps({"status": "success", "data": {"file_status": "exists", "url": baseurl+"/file?key="+key}}) 
                resp.status = falcon.HTTP_200
            except:
                resp.status = falcon.HTTP_404
        else: 
            resp.body = json.dumps(val) 

        

api = falcon.API()
api.req_options.auto_parse_form_urlencoded=True
api.add_route('/markdowntopdf', MarkdownToPdf())
api.add_route('/file', GetFile())
api.add_route('/checkfile', CheckFile())




