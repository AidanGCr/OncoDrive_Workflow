#!/usr/bin/env python3
# Push VCF file into SQLite3 database using dbname

import sys
import re
import sqlite3

if len(sys.argv) < 2:
    print("usage {} [dbname]").format(sys.argv[0])
    print("reads VCF on stdin, and writes output to a sqlite3 db [dbname]")
    exit(1)

dbname = sys.argv[1]

# parse the header
# into a mapping from tag -> type

infotypes = {}
infonumbers = {}
formattypes = {}
formatnumbers = {}
sampletypes = {} 
sample_list = [] 

print("---- Processing header ----") 
for line in sys.stdin:
    if line.startswith('##INFO'):
        #<ID=XRS,Number=1,Type=Float,
        i = re.search("ID=(.*?),", line)
        n = re.search("Number=(.*?),", line)
        t = re.search("Type=(.*?),", line)
        if i and n and t:
            iden = i.groups()[0]
            number = n.groups()[0]
            typestr = t.groups()[0]
            if number == "A":
                number = -1
            elif number == "G" or number == "." or int(number) > 1:
                number = 0
                typestr = "String"
            else:
                number = int(number)
            # remove "REF" flag type column - the same name of the "REF" columns causes errors
            if iden == "REF" and typestr == "Flag": 
                continue
            else: 
                infotypes[iden] = typestr
                infonumbers[iden] = number
                print(iden, number, typestr)
        else:
            continue
    elif line.startswith('##FORMAT'): 
        # read in the format lines
        #<ID=XRS,Number=1,Type=Float,
        i = re.search("ID=(.*?),", line)
        n = re.search("Number=(.*?),", line)
        t = re.search("Type=(.*?),", line)
        if i and n and t:
            iden = i.groups()[0]
            number = n.groups()[0]
            typestr = t.groups()[0]
            if number == "R" or number == "G":
                typestr = "String" 
            elif int(number) > 1:
                # unclear how to deal with these
                continue
            else:
                number = int(number)
            formattypes[iden] = typestr
            formatnumbers[iden] = number
        else:
            continue
    elif line.startswith('#CHROM'): 
        # process samples - last line of header so this will be done last
        # samples will be stored in infotypes for ease of processing
        non_sample_fields = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']  
        fields = line.split('\t')
        for field in fields: 
            if field not in non_sample_fields:  
                sample_list.append(field) 
                for format_field in formattypes.keys(): 
                    if not field.endswith("\n"): 
                        sample_format_field_name = str(field) + "_" + str(format_field)  
                        infotypes[sample_format_field_name] = formattypes[format_field] 
                    else: 
                        new_field = field[:-2]
                        sample_format_field_name = str(new_field) + "_" + str(format_field)  
                        infotypes[sample_format_field_name] = formattypes[format_field] 
    elif line.startswith('##'):
        continue # other header lines which are unused
    else: 
        break # out of header lines
print("---- Header processed ----") 

# write the table schema
print("---- Writing table schema ----") 
infotype_to_sqltype = {}
infotype_to_sqltype["Flag"] = "boolean"
infotype_to_sqltype["Integer"] = "integer"
infotype_to_sqltype["Float"] = "real"
infotype_to_sqltype["String"] = "text"
infotype_to_sqltype["Character"] = "text"

tablecmd = """create table alleles"""
specs = ["CHROM text",
        "POS integer",
        "ID text",
        "REF text",
        "ALT text",
        "QUAL real",
        "FILTER text"]

sorted_fields = sorted(infotypes.keys())
for field in sorted_fields:
    infotype = infotypes[field]
    sqltype = infotype_to_sqltype[infotype]
    field = field.replace(".", "_") # escape periods, which are not allowed
    field = field.replace("-", "_") # testing escaping dashes
    specs.append(field + " " + sqltype)

tablecmd += " (" + ", ".join(specs) + ")"

#Diagnostic ---- 
print("---- DIAGNOSTIC START ---") 
print("---- Printing specs ----") 
print(specs) 
print("---- Printing tablecmd ----") 
print(tablecmd) 
print("---- DIAGNOSTIC END ----") 
#Diagnostic ----

conn = sqlite3.connect(dbname)
conn.execute(tablecmd)
print("---- Tables built ----") 

# for each record
# parse the record
# for each allele

counter = 0
for line in sys.stdin:
    counter = counter + 1
    print("---- Adding Line " + str(counter) + " ----") 
    fields = line.split('\t')
    chrom, pos, iden, ref, alts, qual, filt, info, form = fields[:9]
    samples = fields[10:]
    alts = alts.split(",")
    form = form.split(":")
    altindex = 0
    chrom = "\'" + chrom + "\'"
    iden = "\'" + iden + "\'"
    ref = "\'" + ref + "\'"
    filt = "\'" + filt + "\'"
    for alt in alts:
        alt = "\'" + alt + "\'"
        info_values = {}
        for pair in info.split(";"):
            if pair.find("=") is not -1:
                pair = pair.split("=")
                key = pair[0]
                value = pair[1]
                if key not in infonumbers:
                    continue
                if infonumbers[key] == -1:
                    values = value.split(",")
                    value = values[altindex]
                info_values[key] = value
            else:
               # boolean flag
                info_values[pair] = "1" 
        # parse samples - again using info_values for ease of use
        sample_index = 0
        for sample in samples: 
            format_index = 0
            for sample_field in sample.split(":"): 
                key = str(sample_list[sample_index]) + "_" + str(form[format_index]) 
                value = sample_field
                if value == ".":
                    value = "null" 
                info_values[key] = value
                format_index += 1 
            sample_index += 1 
        ordered_insertion = []
        for field in sorted_fields:
            value = "null"
            if field in info_values:
                value = info_values[field]
                if infotypes[field] == "String" or infotypes[field] == "Character":
                    value = "\'" + value + "\'"
            else:
                # missing flag means "false" for that flag
                if infotypes[field] == "Flag":
                    value = "0"
            ordered_insertion.append(value)
        cmd = "insert into alleles values (" \
            + ", ".join([chrom, pos, iden, ref, alt, qual, filt]) \
            + ", " \
            + ", ".join(ordered_insertion) + ")"
        try:
            conn.execute(cmd)
        except Exception as e:
            print("---- Printing cmd ----") 
            print(cmd) 
            print("---- Printing exception ----") 
            print(e) 
        altindex += 1
    print("---- Finished Line ----") 
conn.commit()

# TODO ignoring samples (for now)

# add indexes everywhere?

conn.close()
