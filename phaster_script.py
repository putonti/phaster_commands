import os
import json

path='/media/catherine/ExtraDrive1/Eli_Ecoli/'

with open(path+'new_ecoli_genomes_lst.txt','r') as f:
    files=[i.rstrip() for i in f.readlines()]

# submits files to phaster
#for i in files:
#    outfile=i[:i.find(".")]
#    command='nohup wget --post-file="'+path+'ec_pt1/'+i+'" "http://phaster.ca/phaster_api?contigs=1" -O '+path+'new_phaster_output/'+outfile
#    print(command+'\n')
#    os.system(command)

# check current status of submission: http://phaster.ca/phaster_api?acc=ZZ_567e255585

#wget "http://phaster.ca/phaster_api?acc=ZZ_023a167bf8" -O Output_filename

# gets results from phaster
#for i in files:
#    output=path+'phaster_output/'+i[:i.find(".")]
#    with open(output,'r') as f:
#        data=json.load(f)
#    job_id=data['job_id']
#    command='wget "phaster.ca/submissions/'+job_id+'.zip"'
#    os.system(command)
#    command='mv '+path+'/'+job_id+'.zip '+path+'new_phaster_output/'+i[:i.find(".")]+'_output.zip'
#    os.system(command)

# for i in *.zip; do unzip "$i" -d "${i%%.zip}"; done

from os import walk
from Bio import SeqIO

# root folder where all of the result folders are
path=path+'new_phaster_output/'

# output file
output_intact=open(path+'all_new_intact_phasters.fna','w')
output_questionable=open(path+'all_questionable_phasters.fna','w')
output_incomplete=open(path+'all_incomplete_phasters.fna','w')


for i in files:
    # determine which phage sequence is which category
    filename=path+i[:i.find(".")]+'_output/summary.txt'
    if os.path.exists(filename):
        with open(filename,'r') as f:
            details=f.readlines()
        intact=[]
        questionable=[]
        incomplete=[]
        j=0
        while j < len(details):
            if '-----' in details[j]:
                break
            else:
                j+=1
        j+=1
        while j < len(details):
            line=details[j].strip().split()
            if 'intact' in line[2]:
                intact.append(line[0])
            elif 'question' in line[2]:
                questionable.append(line[0])
            else:
                incomplete.append(line[0])
            j+=1
        num_found=len(intact)+len(questionable)+len(incomplete)
        
        if num_found>0:
           # write sequences to file
            seqs=list(SeqIO.parse(path+i[:i.find(".")]+'_output/phage_regions.fna','fasta'))
            for j in seqs:
                if j.id in intact:
                    description=str(j.description)
                    description=description.replace('\t ','_')
                    description=description.replace(',','_')
                    output_intact.write('>'+i[:i.find(".")]+'_'+description+'\n'+str(j.seq)+'\n')
                if j.id in questionable:
                    description=str(j.description)
                    description=description.replace('\t ','_')
                    output_questionable.write('>'+i[:i.find(".")]+'_'+description+'\n'+str(j.seq)+'\n')
                if j.id in incomplete:
                    description=str(j.description)
                    description=description.replace('\t ','_')
                    output_incomplete.write('>'+i[:i.find(".")]+'_'+description+'\n'+str(j.seq)+'\n')
    else:
        print(filename)

output_intact.close()
output_questionable.close()
output_incomplete.close()
