import json,sys
with open(sys.argv[1])as file:json_object=json.load(file)
idx,combined_var=1,{(*sorted(obj3["points"]),):[obj3["capacity"],1]for obj3 in json_object["links"]}
for obj1 in json_object["simulation"]["demands"]:obj1["running"]=0
for tick in range(1,1+json_object["simulation"]["duration"]):
 for obj1 in json_object["simulation"]["demands"]:
  if obj1["start-time"]is tick:
   for obj2 in json_object["possible-circuits"]:
    if obj1["end-points"]==[obj2[0],obj2[-1]]and all([combined_var[(*sorted(obj3),)]>=[obj1["demand"],1]for obj3 in zip(obj2,obj2[1:])]):
     obj1["running"]=obj2
     for obj2 in zip(obj2,obj2[1:]):combined_var[(*sorted(obj2),)][1]=0
     break
   print(f'{idx}. igény foglalás: {"<->".join(obj1["end-points"])} st:{tick} - siker{"es"if obj1["running"]else"telen"}');idx=1+idx
  if obj1["running"]and obj1["end-time"]is tick:
   for linkid in zip(obj1["running"],obj1["running"][1:]):combined_var[(*sorted(linkid),)][1]=1
   print(f'{idx}. igény felszabadítás: {"<->".join(obj1["end-points"])} st:{tick}');idx=1+idx