"""Read-only, deterministic tools for the fictional Empório da Música store."""
from __future__ import annotations
import csv
import json
import re
import unicodedata
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
from pypdf import PdfReader

DATA = Path(__file__).resolve().parent / 'data'


def rows(filename):
    with (DATA / filename).open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def norm(value):
    value = unicodedata.normalize('NFKD', str(value))
    return ''.join(c for c in value if not unicodedata.combining(c)).casefold().strip()


def money(value):
    return f'R$ {Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP):,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def catalog(search='', category='', max_price=None, limit=10):
    """Search active instruments; only in-stock listings appear in search results."""
    categories = {r['category_id']: r['name'] for r in rows('categories.csv')}
    promotions = {r['product_id']: r for r in rows('promotions.csv') if r['is_active'] == '1'}
    output=[]
    for p in rows('products.csv'):
        if p['status'] != 'active' or int(p['stock_quantity']) <= 0:
            continue
        if search and not all(word in norm(p['name']+' '+p['description']) for word in norm(search).split()):
            continue
        cat_name=categories.get(p['category_id'], '')
        if category and norm(category) not in norm(cat_name):
            continue
        base=Decimal(p['price_brl'])
        promo=promotions.get(p['product_id'])
        final=(base*(Decimal(100)-Decimal(promo['discount_percent']))/Decimal(100)) if promo else base
        if max_price is not None and final > Decimal(str(max_price)):
            continue
        output.append({'id':int(p['product_id']),'name':p['name'],'category':cat_name,
                       'list_price':money(base),'current_price':money(final),
                       'stock':int(p['stock_quantity']),
                       'promotion_percent':int(promo['discount_percent']) if promo else 0})
    output.sort(key=lambda p: (float(p['current_price'].replace('R$ ', '').replace('.', '').replace(',', '.')),p['name']))
    return {'results':output[:max(1,min(int(limit),20))],'total_matches':len(output),
            'note':'Snapshot of supplied CSV files; not connected to a live store system.'}


def get_product(query):
    ps=rows('products.csv')
    exact=[p for p in ps if norm(p['name']) == norm(query) or p['product_id']==str(query)]
    matches=exact or [p for p in ps if norm(query) in norm(p['name'])]
    if not matches:
        return {'found':False,'message':'Product not found in supplied catalog.'}
    p=matches[0]
    response=catalog(search='', limit=20)
    item=next((x for x in catalog(search=p['name'],limit=20)['results'] if x['id']==int(p['product_id'])),None)
    if item is None:
        return {'found':True,'name':p['name'],'available':False,'stock':int(p['stock_quantity']),
                'status':p['status'],'list_price':money(p['price_brl']),
                'note':'Not currently available for sale; do not offer as in stock.'}
    return {'found':True,'available':True,**item,'description':p['description']}


def order_status(order_id, email):
    """Require exact order id + registered e-mail; never leak records on mismatch."""
    if not email or not order_id:
        return {'verified':False,'message':'Ask for the order number and the e-mail used for purchase.'}
    order=next((o for o in rows('orders.csv') if o['order_id']==str(order_id)),None)
    customer=next((c for c in rows('customers.csv') if order and c['customer_id']==order['customer_id']),None)
    if not order or not customer or norm(email)!=norm(customer['email']):
        return {'verified':False,'message':'Order and e-mail do not match. Please contact a human attendant for verification.'}
    product_names={r['product_id']:r['name'] for r in rows('products.csv')}
    items=[{'product':product_names.get(i['product_id'],'Unknown product'),'quantity':int(i['quantity'])}
           for i in rows('order_items.csv') if i['order_id']==str(order_id)]
    return {'verified':True,'order_id':order['order_id'],'status':order['status'],
            'order_date':order['order_date'],'estimated_delivery':order['estimated_delivery'],
            'tracking_code':order['tracking_code'] or None,'total':money(order['total_brl']),
            'items':items,'note':'Historical snapshot from supplied CSV, not live carrier data.'}


def policy_lookup(topic):
    """Retrieve relevant PDF pages using lexical matching; cite page numbers."""
    query=set(norm(topic).split())
    stop={'a','o','de','da','do','e','para','como','qual','quais','me','um','uma','sobre','the','what','how','is','can','i'}
    query={w for w in query if len(w)>2 and w not in stop}
    # Document headings/contexts provide stronger matches for common questions.
    tags={
        'horario':['funcionamento','horario','abre','fecha','aberto','expediente','endereco','localizacao'],
        'pagamento':['pix','pagamento','cartao','parcelamento','boleto','parcela'],
        'trocas':['troca','devolucao','arrependimento','reembolso','defeito'],
        'frete':['frete','entrega','prazo','correios','sedex','pac','rastreamento'],
        'promocoes':['promocao','promocoes','desconto','oferta','acumula'],
        'whatsapp':['atendimento','whatsapp','telefone','contato'],
        'garantia':['garantia','defeito','fabricante'],
        'privacidade':['lgpd','privacidade','dados','consentimento'],
    }
    reader=PdfReader(DATA/'store_policies.pdf')
    pages=[p.extract_text(extraction_mode='layout') or '' for p in reader.pages]
    scores=[]
    for idx,page in enumerate(pages):
        body=norm(page)
        score=sum(body.count(w) for w in query)
        if any(w in query for w in tags['horario']) and idx==1: score+=25
        if any(w in query for w in tags['pagamento']) and idx==2: score+=25
        if any(w in query for w in tags['trocas']) and idx==3: score+=25
        if any(w in query for w in tags['frete']) and idx in (3,4): score+=20
        if any(w in query for w in tags['promocoes']) and idx==5: score+=25
        if any(w in query for w in tags['whatsapp']) and idx==5: score+=15
        if any(w in query for w in tags['garantia']) and idx==6: score+=25
        if any(w in query for w in tags['privacidade']) and idx in (6,7): score+=20
        scores.append((score,idx))
    selected=sorted(scores,reverse=True)[:2]
    return {'source':'Empório da Música, Manual de Políticas e Procedimentos, version 2.1 (June 2025)',
            'pages':[{'page':idx+1,'text':pages[idx][:6500]} for score,idx in selected if score>0]}

TOOLS={
 'catalog':catalog,
 'get_product':get_product,
 'order_status':order_status,
 'policy_lookup':policy_lookup,
}

TOOL_SCHEMAS=[
 {'type':'function','function':{'name':'catalog','description':'Search actual inventory and promotional prices for in-stock musical instruments. Supports max price and category filters.',
 'parameters':{'type':'object','properties':{'search':{'type':'string'},'category':{'type':'string'},'max_price':{'type':'number'},'limit':{'type':'integer'}},'additionalProperties':False}}},
 {'type':'function','function':{'name':'get_product','description':'Find a specific instrument by name or ID, including its availability and current price.',
 'parameters':{'type':'object','properties':{'query':{'type':'string'}},'required':['query'],'additionalProperties':False}}},
 {'type':'function','function':{'name':'order_status','description':'Get order details only after checking the order number AND exact registered customer e-mail.',
 'parameters':{'type':'object','properties':{'order_id':{'type':'string'},'email':{'type':'string'}},'required':['order_id','email'],'additionalProperties':False}}},
 {'type':'function','function':{'name':'policy_lookup','description':'Retrieve original store policy PDF passages with source page numbers. Use for opening hours, returns, warranty, shipping, discounts and payment.',
 'parameters':{'type':'object','properties':{'topic':{'type':'string'}},'required':['topic'],'additionalProperties':False}}},
]
