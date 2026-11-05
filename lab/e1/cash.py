"""Cash-session calculations."""

def cash_state(events):
    current=None
    for e in events:
        p=e['payload']
        if e['kind']=='open':current={'id':e['id'],'opening':p['opening'],'expected':p['opening'],'moves':[]}
        elif e['kind']=='close':current=None
        elif current:
            amount=p['cash'] if e['kind']=='sale' else p['amount']*(1 if p['type']=='Entrada' else -1)
            current['expected']+=amount;current['moves'].append({'id':e['id'],'kind':e['kind'],'amount':amount,'reason':p.get('reason','Venta')})
    return current


def cash_summary(events, corrections, order_moves, session, adjustment=0):
    """Current-session sales by applied payment; order receipts stay separate."""
    sales={e['id']:dict(e['payload']) for e in events if e['kind']=='sale' and e['payload'].get('session')==session['id']}
    for document in corrections:
        p=document['payload']
        if p.get('session')!=session['id']:continue
        if p['target'] in sales:sales[p['target']]=p['after']
        if p.get('replacement'):sales[p['replacement']['id']]=p['replacement']
    result={'expected':session['expected']+adjustment,'sales_count':0,'payments':{k:{'amount':0,'count':0} for k in ('cash','card','transfer')},'orders':{k:0 for k in ('cash','card','transfer')}}
    for p in sales.values():
        if p.get('cancelled'):continue
        result['sales_count']+=1
        for k,row in result['payments'].items():
            row['amount']+=p.get(k,0)
            row['count']+=int(p.get(k,0)>0)
    for p in order_moves:
        for k in result['orders']:result['orders'][k]+=p.get(k,p.get('amount',0) if k=='cash' else 0)
    return result
