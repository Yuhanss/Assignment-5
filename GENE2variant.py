#!/usr/bin/env python
import fileinput
import re
import json
import urllib

Lookup_geneName={}

gene_name = raw_input("Please type your gene name, all caps, and press enter (e.g. APOE):")

for line in fileinput.input(['/home/yuhan/example/Homo_sapiens.GRCh37.75.gtf']):
    gene_id_matches = re.findall('gene_id \"(.*?)\";',line)
    gene_name_matches = re.findall('gene_name \"(.*?)\";',line)
    if gene_name_matches:
       if gene_id_matches:
          Lookup_geneName[gene_name_matches[0]] = gene_id_matches[0]
print "The variants within the gene", gene_name, Lookup_geneName[gene_name], "are:"

url = 'http://rest.ensembl.org/overlap/id/' + Lookup_geneName[gene_name] + '.json?feature=variation'
response = urllib.urlopen(url)
data = json.loads(response.read())

for i in range(0,len(data)):
    dic = data[i]
    var_id = dic["id"]
    var_cons_type = dic["consequence_type"]
    var_clinic = dic["clinical_significance"]
    var_cons_new = var_cons_type.replace("_"," ")
    if var_clinic:
       print "Variant", var_id, "is a", var_cons_new, ", and is clinically", var_clinic[0].upper(), ".\n"
    else:
       print "Variant", var_id, "is a", var_cons_new, ".\n"
