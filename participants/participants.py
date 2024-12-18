#!/usr/bin/env python
# -*- coding: utf8 -*-

import re, csv
import itertools
from sys import argv

assert len(argv) > 1, "Specify output format as html, tags, or list..."
output = argv[1]


participants = [
	# invited speakers
    #["Abele", "Hartmut", "Vienna"],
    #["Afshordi", "Niayesh", "Perimeter/Waterloo"],
    #["Berti", "Emanuele", "John Hopkins"],
    #["Burgess", "Cliff", "Perimeter"],
    #["de Rham", "Claudia", "Imperial"],
    #["Ferreira", "Pedro", "Oxford"],
    #["Gregory", "Ruth", "Kings College"],
    #["Hui", "Lam", "Columbia"],
    #["Kasevich", "Mark", "Stanford"],
    #["Khoury", "Justin", "U Penn"],
    #["Macpherson", "Hayley", "Chicago"],
    #["McIver", "Jess", "UBC"],
    #["Medeiros", "Lia", "IAS"],
    #["Mohlabeng", "Gopolang", "Irvine/SFU"],
    #["Nissanke", "Samaya", "Amsterdam"],
    #["Percival", "Will", "Perimeter/Waterloo"],
    #["Pretorius", "Frans", "Princeton"],
    #["Raveri", "Marco", "Genova"],
    #["Sakstein", "Jeremy", "Hawaii"],
    #["Sasaki", "Misao", "Tokyo"],
    #["Sedrakian", "Armen", "Frankfurt"],
    #["Tolley", "Andrew", "Imperial"],
    #["Trodden", "Mark", "UPenn"],
    #["Vachaspati", "Tanmay", "ASU"],
    #["Weinfurtner", "Silke", "Nottingham"],
  	# LOC
  	["Frolov", "Andrei", "Simon Fraser University"],
  	["Pogosian", "Levon", "Simon Fraser University"],
]

soc = ["Frolov", "McKeen", "Medeiros", "Pogosian", "Ross", "Scott", "Silvestri"]
loc = []
exclude = []

table = []

def mangle(affiliation):
	affiliation = re.sub(r"^(The\s+)", '', affiliation)
	affiliation = re.sub(r"Queen Mary University of London", 'Queen Mary London', affiliation)
	affiliation = re.sub(r"Royal Astronomical Society", 'RASC', affiliation)
	affiliation = re.sub(r"University of British Columbia", 'UBC', affiliation)
	affiliation = re.sub(r"Simon Fraser (U|u)niversity", 'SFU', affiliation)
	affiliation = re.sub(r"Canadian Institute for Theoretical Astrophysics", 'CITA', affiliation)
	affiliation = re.sub(r"Memorial University of Newfoundland", 'Memorial', affiliation)
	affiliation = re.sub(r"California Institut?e of Technology", 'Caltech', affiliation)
	affiliation = re.sub(r"California State University", 'CSU', affiliation)
	affiliation = re.sub(r"University of California(,|\s+at)?", 'UC', affiliation)
	affiliation = re.sub(r"Rochester Institute of Technology", 'RIT', affiliation)
	affiliation = re.sub(r"University of Texas(,|\s+at)?", 'UT', affiliation)
	affiliation = re.sub(r"U(niversity of)?\s+Penn(sylvania)?", 'UPenn', affiliation)
	affiliation = re.sub(r"Penn(sylvania)?\s+State(\s+University)?", 'PennState', affiliation)
	affiliation = re.sub(r"Case Western Reserve", 'Case Western', affiliation)
	affiliation = re.sub(r"Perimeter.*", 'Perimeter', affiliation)
	affiliation = re.sub(r"ONERA, France", 'ONERA', affiliation)
	affiliation = re.sub(r"Yukawa Institute for Theoretical Physics", 'YITP', affiliation)
	affiliation = re.sub(r"Tokyo University of Science", 'TUS', affiliation)
	affiliation = re.sub(r"University College Dublin", 'UCD', affiliation)
	affiliation = re.sub(r"National Astronomical Observatory of Japan", 'NAOJ', affiliation)
	affiliation = re.sub(r"Institute of Physics, ASCR, Prague", 'Prague', affiliation)
	affiliation = re.sub(r"Max Planck Institute", 'MPI', affiliation)
	affiliation = re.sub(r"Albert Einstein Institute", 'AEI', affiliation)
	affiliation = re.sub(r"Lorentz Institute\s*(,|-)\s*Leiden.*", 'Leiden University', affiliation)
	affiliation = re.sub(r"Universidad Autónoma de Madrid", 'UAM', affiliation)
	affiliation = re.sub(r"National Centre for Nuclear Research", 'NCNR', affiliation)
	affiliation = re.sub(r"Lebedev.*", 'Lebedev', affiliation)
	affiliation = re.sub(r".*\(IKI\).*", 'IKI', affiliation)
	affiliation = re.sub(r"ITA - Aeronautics Institute of Technology", 'ITA', affiliation)
	affiliation = re.sub(r"Universidad Austral de Chile", 'UACh', affiliation)
	affiliation = re.sub(r"American University of Afghanistan", 'AUAF', affiliation)
	affiliation = re.sub(r"Prince Mohammad Bin Fahd University", 'PMU', affiliation)
	affiliation = re.sub(r"Universidade do Estado do Rio de Janeiro", 'UERJ', affiliation)
	affiliation = re.sub(r"Chinese University of Hong Kong", 'CUHK', affiliation)
	affiliation = re.sub(r"Institute of Cosmology and Gravitation Portsmouth", 'Portsmouth', affiliation)
	affiliation = re.sub(r"Universidad Nacional de Ingeniería.*", 'UNI, Peru', affiliation)
	affiliation = re.sub(r"Thapar Institute of Engineering (&|and) Technology", 'TIET', affiliation)
	affiliation = re.sub(r"Wisconsin,?\s+Milwaukee", 'Wisconsin-Milwaukee', affiliation)
	affiliation = re.sub(r"\s*(U|u)niversi(ty|té|dad)(\s+(of|at|de))?(\s+(the))?\s*", '', affiliation)
	affiliation = re.sub(r"\s*(O|o)bservato(ry|ire)(\s+(of|at|de))?(\s+(the))?\s*", '', affiliation)
	affiliation = re.sub(r",?\s*Dep(ar)?t(ment)?\s+of\s+.*", '', affiliation)
	affiliation = re.sub(r".*\s*Dep(ar)?t(ment)?,\s+", '', affiliation)
	affiliation = re.sub(r",\s*", ', ', affiliation)
	affiliation = re.sub(r"\s*/\s*", '/', affiliation)
	return affiliation

def grouper(n, iterable, padvalue=None):
	"grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
	return itertools.zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

def chunker(n, array, padvalue=None):
	"chunker(3, 'abcdefg', 'x') --> ('a','d','g'), ('b','e','x'), ('c','f','x')"
	l = len(array); m = (l+n-1)/n
	chunks = [array[i:min(i+m,l)] for i in range(0,l,m)]
	return itertools.izip_longest(*chunks, fillvalue=padvalue)

with open('participants.csv', 'r', encoding='utf-8') as csvfile:
	for row in csv.reader(csvfile, dialect=csv.excel):
		public = row[27].lower()
		if public != 'yes' and not(output == 'tags' and public == 'no'): continue
		if row[5].lower() in [p[0].lower() for p in participants]: continue
		
		# grab names and affiliations
		first,last = row[4:6]; affiliation = row[13]
		if len(last) == 0 or output == 'tags': last = row[22]
		if len(first) == 0 or output == 'tags': first = row[21]
		if len(affiliation) == 0 or output == 'tags': affiliation = row[23]
		affiliation = re.sub(r"[\(\)]+", '', affiliation)
		
		# fix stuff for people who cannot spell
		if last == "DE OLIVEIRA":
			last = "de Oliveira"; first = "Henrique"
		if last == "Kuhn": affiliation = "UBC"
		if last == "Lindsay": affiliation = "Retired"
		#if last == "Afshordi": affiliation = "Perimeter/Waterloo"
		#if last == "Nakato": affiliation = "Kobe University"
		#if last == "Sedrakian": affiliation = "Frankfurt Institute for Advnaced Studies"
		#if last == "Weinfurtner": affiliation = "University of Nottingham"
		#if last == "MacEachern": affiliation = "University of British Columbia"
		#if last == "Yazdi": affiliation = "Independent Researcher"
		#if last == "Mirpoorian": first = "Hamid"

		participants.append([last,first,affiliation])

participants.sort(key = lambda p: (p[0]+p[1]).lower())

for p in itertools.groupby(participants):
	last,first,affiliation = p[0]
	
	# abbreviate name if it is too long
	if (len(first+last) > 24):
		first = re.sub(r'([A-Z])[a-z]+', r'\1.', first)
	
	# special roles...
	role = ""
	if last in soc and not first in exclude: role = "[soc]"
	if last in loc and not first in exclude: role = "[volunteer]"
	
	# formatted output
	if output == 'html': table.append("%s %s (%s)" % (first, last, mangle(affiliation)))
	if output == 'tags': table.append("\\nametag%s{%s %s}{%s}" % (role, first, last, mangle(affiliation)))
	if output == 'list': table.append("\\nametag%s{%s %s}{%s}" % (role, first, last, mangle(affiliation)))

if output == 'html':
	print("""<meta charset="UTF-8">
<font face="PT Sans Caption" size="6">Registered Participants:
</font>
<table>
<tbody style="vertical-align: top;">
<tr>
""")
	
	#for row in chunker(3, table, ""):
	#	print "<tr>"
	#	for name in row:
	#		print "<td style=\"width: 48ex;\">%s" % name
	
	for column in grouper((len(table)+2)//3, table):
		print("<td style=\"width: 30%;\"><ul>")
		for name in column:
			if name != None: print("<li>" + name)
		print("</ul></td>")
	
	print("""
</tr>
</tbody>
</table>
""")
else:
	for tag in table:
		print(re.sub(r"\&", '\\&', tag))
