from json import*;from sys import*;from operator import*
with open(argv[1])as file:
 json_object=load(file);json_object["links"]={tuple(sorted(obj3["points"])):[obj3["capacity"],[0]]for obj3 in json_object["links"]};json_object["simulation"]["demands"]=sorted(json_object["simulation"]["demands"],key=itemgetter("end-time","start-time"));idx=0
for obj3 in json_object["simulation"]["demands"]:obj3["running"]=[]
for tick in range(json_object["simulation"]["duration"]):
 for obj1 in json_object["simulation"]["demands"]:
  if obj1["start-time"]==tick+1:
   for obj2 in json_object["possible-circuits"]:
    if obj1["end-points"]==[obj2[0],obj2[-1]]and all([json_object["links"][tuple(sorted(obj3))][0]>=obj1["demand"]and json_object["links"][tuple(sorted(obj3))][-1]for obj3 in zip(obj2,obj2[1:])]):
     for obj3 in zip(obj2,obj2[1:]):json_object["links"][tuple(sorted(obj3))][-1]=[]
     obj1["running"]=obj2;break
   idx+=1;print(f'{idx}. igény foglalás: {obj1["end-points"][0]}<->{obj1["end-points"][1]} st:{tick} - {"sikeres" if obj1["running"]else "sikertelen"}')
  if obj1["end-time"]==tick+1 and obj1["running"]:
   for linkid in zip(obj1["running"],obj1["running"][1:]):json_object["links"][tuple(sorted(linkid))][-1]=[0]
   idx+=1;print(f'{idx}. igény felszabadítás: {obj1["end-points"][0]}<->{obj1["end-points"][1]} st:{tick}')