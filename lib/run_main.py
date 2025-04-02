import os 
import sys
from . import select_passed_diamond as dia_sel
from . import XGboost_test as XGB
from . import clean_data as CD

def MOPDT_gene_call(IN,
        OUT,GENOME):
    os.environ['IN']=str(IN)
    os.environ['OUT']=str(OUT)
    print("---Gene call with Prodigal start---\n")
    os.system('mkdir -p ${OUT}/Intermediate_dir &> /dev/null')
    if not GENOME:
        os.system('prodigal -p meta -i ${IN} -f sco -q -a ${OUT}/calling_pro.faa > ${OUT}/Intermediate_dir/Prodigal_sco.txt')
    else:
        os.system('prodigal -p single -i ${IN} -f sco -q -a ${OUT}/calling_pro.faa > ${OUT}/Intermediate_dir/Prodigal_sco.txt')
    #提取prodigal输出的蛋白的conitg来源和位置
    with open("{}/Intermediate_dir/Prodigal_sco.txt".format(OUT),"r") as f:
        a=f.read()
    try:
        import pandas as pd
    except:
        sys.exit("CRITICAL ERROR: pandas (python package) not found")

    pro=[]
    contig=[]
    for i in a.split("\n# Sequence Data: seqnum="):
        for x in i.split("\n"):
            if x.startswith(">"):
                pro.append(x)
                contig.append(i.split("\n")[0].split("seqhdr=")[1].split(" ")[0].strip("\""))
    pro_tail=[]
    pos_pre=[]
    pos_tail=[]
    strand=[]
    for y in pro:
        y_sp=y.split("_")
        pro_tail.append(y_sp[0].lstrip(">"))
        pos_pre.append(y_sp[1])
        pos_tail.append(y_sp[2])
        strand.append(y_sp[3])

    pd.DataFrame({"protein_ID":[str(i1)+"_"+str(i2) for i1,i2 in zip(contig,pro_tail)],
                "source_contig":contig,
                "gene_position_start":pos_pre,
                "gene_position_end":pos_tail,
                "chain":strand}).to_csv("{}/calling_pro2conitg.txt".format(OUT),sep="\t",index=None)

    return str("{}/calling_pro.faa".format(OUT))
    print("---Gene call with Prodigal start---\n")


def MOPDT_main(
        IN,
        OUT,
        LEVEL,
        Intermediate,
        THREAD,
        DIAMOND_DB,
        CHECK_DB,
        HMM_DB,
        NO_CHECK,
        HMM_DB_KO):
    #先判断输入的是否为蛋白，有没有该选项：
    os.environ['IN']=str(IN)
    os.environ['OUT']=str(OUT)
    os.environ['THREAD']=str(THREAD)
    os.environ['DIAMOND_DB']=str(DIAMOND_DB)
    os.environ['HMM_DB']=str(HMM_DB)
    os.environ['CHECK_DB']=str(CHECK_DB)

    #Diamond
    print("---Align with Diamond start---\n")
    os.system('mkdir -p ${OUT}/Intermediate_dir &> /dev/null')
    #os.system('mkdir -p ${OUT}/Map_file')
    os.system('diamond blastp -d ${DIAMOND_DB} -q ${IN} --unal 1 -e 10 -f 6 -o ${OUT}/Intermediate_dir/diamond.m8 -k 1 -p ${THREAD} &> /dev/null')
    os.system('sed -i \'s/\*/-/g\' ${OUT}/Intermediate_dir/diamond.m8')
    os.system('seqkit fx2tab -n -i -l ${IN} > ${OUT}/Intermediate_dir/Input_seq_len')
    dia_sel.main(diamond_IN='{}/Intermediate_dir/diamond.m8'.format(OUT),
            INPUT_SEQ_LEN='{}/Intermediate_dir/Input_seq_len'.format(OUT),
            diamond_OUT='{}/Intermediate_dir/diamond_raw_res.txt'.format(OUT))
    os.system('cat ${OUT}/Intermediate_dir/diamond_raw_res.txt |sed \'1d\'|awk -F"\t" \'$1>90\'|awk -F"\t" \'$15 > 0.8 || $16 > 0.8 {print $13}\'|sort|uniq|awk \'BEGIN {print "ID"} 1\' > ${OUT}/Intermediate_dir/diamond_res_is_MOP.txt')
    #os.system('cut -f3 ${OUT}/Intermediate_dir/diamond_not_found_as_MOP.txt|seqkit grep -f - ${IN} > ${OUT}/Intermediate_dir/diamond_not_found_as_MOP.faa 2> /dev/null')
    print("---Align with Diamond complete---\n")
                  

    #hmm
    print("---Predict with hmmsearch start---\n")
    os.system('mkdir ${OUT}/Intermediate_dir/hmm_res_split;for i in `ls ${HMM_DB}*hmm`;do x=`basename ${i} |sed \'s/\.hmm$//g\'`;echo "hmmsearch --tblout ${OUT}/Intermediate_dir/hmm_res_split/${x}_seq.txt -o /dev/null --noali --cpu 1 ${i} ${IN}";done|parallel -j ${THREAD}')
    os.system('ls ${OUT}/Intermediate_dir/hmm_res_split/*seq.txt|xargs cat |grep -v "^#"|awk  \'{print $1"\t"$3"\t"$5"\t"$6}\' > ${OUT}/Intermediate_dir/HMM_raw_res.txt')
    os.system('cat ${OUT}/Intermediate_dir/HMM_raw_res.txt |awk \'$3 < 0.00001 && $4 > 80   {print $1}\'|sort|uniq|awk \'BEGIN {print "ID"} 1\' > ${OUT}/Intermediate_dir/HMM_res_is_MOP.txt') 
    print("---Predict with hmmsearch complete---\n")
    #XGBoost
    print("---Predict with XGBoost start---\n")
    XGB.main(pro_path=str(IN),
    XG_OUT_PATH='{}/Intermediate_dir/XGboost_raw_res.tsv'.format(str(OUT)),
    Include_feat='{}/lib/Include_feat'.format(sys.path[0]),
    XG_model='{}/lib/XG_model'.format(sys.path[0]))
    os.system('cat ${OUT}/Intermediate_dir/XGboost_raw_res.tsv |awk \'$2 == "MOP" {print $1}\'|sort|uniq|awk \'BEGIN {print "ID"} 1\' > ${OUT}/Intermediate_dir/XGboost_res_is_MOP.txt')
    print("---Predict with XGBoost complete---\n")


    print("---Stat data start---\n")
    CD.stat_level(OUT=OUT,Level=LEVEL,CHECK_DB=CHECK_DB,THREAD=THREAD,IN=IN,NO_CHECK=NO_CHECK)
    end_stat_fil_out=CD.re_label(OUT=OUT,
                                THREAD=THREAD,
                                HMM_DB_KO=HMM_DB_KO)
    CD.extract_MOP(OUT=OUT,THREAD=THREAD,IN=IN,end_stat_fil_out=end_stat_fil_out)
    CD.clean(OUT,bool(Intermediate))
    print("---Stat data complete---\n")
