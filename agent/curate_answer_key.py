# Builds data/projects_input.json from parsed EQB entries + a short curated list
# (the "answer key" I checked by hand). Each notice keeps its source link and a quote.
import json,re,datetime
E=json.load(open("entries.json"))
def iso(d):
    try: return datetime.datetime.strptime(d,"%B %d, %Y").date().isoformat()
    except: return None
def field(t,name):
    m=re.search(name+r':\s*(.*?)(?=(Process:|Step:|End of comment period:|Responsible governmental unit|Project description|Notice description|Location of public|\n|$))',t)
    return m.group(1).strip().rstrip(';') if m else None
def quote(t):
    m=re.search(r'(?:Project|Notice|Variance) description:\s*(.*)',t)
    if not m: return None
    s=m.group(1); s=re.split(r'(?<=[.])\s',s)
    q=s[0]; 
    if len(q.split())<12 and len(s)>1: q+=' '+s[1]
    return q[:260]
C=[
 # id, category, display name, title regex, lat, lon, precision, location label, note
 ("hermantown-dc","confirmed","Hermantown Data Center",r"^Hermantown Data Center",46.8069,-92.2382,"city center (approx.)","Hermantown, St. Louis County",
  "May be the same site as the Harmony Group project and the Hermantown Industrial AUAR. City planning materials (Aug 2026) describe a Google data center campus in Hermantown. Unconfirmed link."),
 ("harmony-group","confirmed","Harmony Group Data Center",r"^Harmony Group Data Center",46.8069,-92.2382,"city center (approx.)","Hermantown, St. Louis County",
  "Check: is this the same site as the 2025 Hermantown Data Center petition? Not stated in the notices."),
 ("igh-dc","confirmed","Inver Grove Heights Data Center",r"^Inver Grove Heights Data Center",44.8480,-93.0427,"city center (approx.)","Inver Grove Heights, Dakota County",None),
 ("nobles-dc","confirmed","Nobles County Data Center AUAR",r"^Nobles County Data Center",43.674,-95.754,"county center (approx.); site is in Summit Lake and Elk Townships","Summit Lake & Elk Townships, Nobles County",None),
 ("archer-faribault","confirmed","Archer Datacenters Faribault Campus",r"^Archer Datacenters",44.2950,-93.2688,"city center (approx.)","Faribault, Rice County",
  'In June 2026 the Minnesota Court of Appeals found the city\'s decision not to require an EIS was unsupported (<a href="https://www.fredlaw.com/alert-court-of-appeals-finds-citys-decision-to-decline-a-data-center-eis-was-erroneous" target="_blank">summary</a>).'),
 ("hermantown-auar","possible","Hermantown Industrial AUAR (possible data center site)",r"Hermantown Industrial AUAR",46.8069,-92.2382,"city center (approx.)","Hermantown, St. Louis County",
  "Notice says 'light industrial' and never says data center. Flagged because it is in the same city and has a similar size to the data center proposals, and power lines are being routed to 'the customer's facility' in Hermantown. Needs confirmation."),
 ("cannon-falls","possible","Cannon Falls Industrial AUAR (possible data center)",r"^Cannon Falls Industrial AUAR",44.5069,-92.9049,"city center (approx.)","Cannon Falls & Randolph Twp, Goodhue/Dakota",
  "Notice describes 'technology park' use by code-named LLCs (MNLCO). 'Technology park' is often used for data centers. Needs confirmation."),
 ("rosemount-dakota-east","possible","Dakota East Area AUAR (possible data center)",r"^Dakota East Area AUAR",44.7394,-93.1258,"city center (approx.)","Rosemount, Dakota County",
  "Same code-named developer family as Cannon Falls (MNLCO). One scenario is large non-residential buildings. Needs confirmation."),
 ("north-mankato","possible","North Mankato Industrial AUAR, 'Project Deacon' (possible data center)",r"^North Mankato Industrial AUAR",44.1733,-94.0338,"city center (approx.)","North Mankato, Nicollet County",
  "4 million sq ft of 'technology park' by a code-named LLC. Needs confirmation."),
 ("monticello-tech","possible","Monticello Technology Campus / Scannell Technology Park (possible data center)",r"^Monticello Technology Campus",45.3055,-93.7941,"city center (approx.)","Monticello Township, Wright County",
  "'Technology campus' language; petition notices only. Needs confirmation."),
 ("skyway-345","related","North Rochester to Skyway 345 kV Transmission Line (for Google)",r"^North Rochester to Skyway",44.2013,-92.6463,"city center (approx.)","Pine Island area, Goodhue County",
  "Power line co-applied by Xcel Energy and Echo Zone LLC, a Google subsidiary, per the notice. Shown as related infrastructure, not a data center."),
 ("stlouis-230","related","St. Louis County 230 kV Transmission Line (to a facility in Hermantown)",r"^St\. Louis County 230 kV",46.8069,-92.2382,"city center (approx.)","Hermantown, St. Louis County",
  "Lines to 'the customer's facility' in Hermantown. Shown as related infrastructure."),
 ("project-skyway","possible","Project Skyway, Pine Island (possible data center)",r"^Project Skyway",44.2013,-92.6463,"city center (approx.)","Pine Island & Pine Island Twp, Goodhue County",
  "Code-named 'Technology Center' on about 482 acres (Ryan Companies). A 345 kV line named 'North Rochester to Skyway' is co-applied by a Google subsidiary. Found by the agent during testing; it was missing from the hand-made answer key. Needs confirmation."),
]
P=[]
for cid,cat,name,rx,lat,lon,prec,loc,note in C:
    ns=[];seen=set()
    for e in E:
        if re.search(rx,e['title']):
            t=e['text'].replace('\n',' ')
            key=(e['volume'])
            if key in seen: continue
            seen.add(key)
            ns.append({"date":e['date'] or "date not found","iso":iso(e['date']) or "2025-07-01","volume":"Vol. "+e['volume'].replace('-',', No. '),
              "url":e['url'],"process":field(t,"Process"),"step":field(t,"Step") or "see notice","deadline":field(t,"End of comment period"),
              "rgu":(re.search(r'Responsible governmental unit and contact:\s*([^,]*)',t) or [None,None])[1],
              "phone":(re.search(r'Responsible governmental unit and contact:[^\n]*?(\(?\d{3}\)?[-. ]\d{3}-\d{4})',t) or [None,None])[1],"quote":quote(t)})
    ns.sort(key=lambda x:x['iso'],reverse=True)
    if not ns: print("NO NOTICES",cid);continue
    last=ns[0]
    dl=next((iso(n['deadline']) for n in ns if n['deadline'] and iso(n['deadline'])),None)
    P.append({"id":cid,"category":cat,"name":name,"location":loc,"location_precision":prec,"lat":lat,"lon":lon,
      "process":last['process'] or ns[-1]['process'] or "see notice","latest_step":last['step'],
      "comment_deadline":dl,"rgu":next((n['rgu'] for n in ns if n['rgu']),None),"rgu_phone":next((n['phone'] for n in ns if n.get('phone')),None),
      "consultation_noted":"unknown","note":note,
      "notices":[{"date":n['date'],"iso":n['iso'],"volume":n['volume'],"url":n['url'],"step":n['step'],"deadline":n['deadline'],"quote":n['quote']} for n in ns]})
json.dump(P,open("repo/data/projects_input.json","w"),indent=1)
for p in P: print(p['id'],len(p['notices']),'|',p['process'],'|',p['latest_step'],'|',p['comment_deadline'],'|',p['rgu'])
