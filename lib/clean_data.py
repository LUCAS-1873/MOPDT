import sys
import os
import shutil
try:
    import pandas as pd
except:
    sys.exit("CRITICAL ERROR: The pandas not found (python package)")


def stat_level(OUT,Level,THREAD,IN,NO_CHECK,CHECK_DB):
    os.environ['THREAD']=str(THREAD)
    os.environ['CHECK_DB']=str(CHECK_DB)
    os.environ['IN']=str(IN)
    os.environ['OUT']=str(OUT)
    MOPD_ID2label=pd.read_csv("{}/DB/MOPD_ID2label.txt".format(sys.path[0]),sep="\t")
    hm=pd.read_csv("{}/Intermediate_dir/HMM_res_is_MOP.txt".format(OUT),index_col=0)
    hm["HMM-based"]=1
    di=pd.read_csv("{}/Intermediate_dir/diamond_res_is_MOP.txt".format(OUT),index_col=0)
    di["Aligned-based"]=1
    xg=pd.read_csv("{}/Intermediate_dir/XGboost_res_is_MOP.txt".format(OUT),index_col=0,sep="\t")
    di_raw=pd.read_csv("{}/Intermediate_dir/diamond_raw_res.txt".format(OUT),sep="\t")
    xg["XGboost-based"]=1
    stat_inthree=pd.merge(di,hm,how='outer',left_index=True,right_index=True).merge(xg,how='outer',left_index=True,right_index=True).fillna(0)
    stat_inthree.index.name=None
    no_hit_set=set(di_raw["Query_name"]) - set(stat_inthree.index)
    Len_no_hit=len(no_hit_set)
    no_hit_df=pd.DataFrame({"Aligned-based":[0]*Len_no_hit,"HMM-based":[0]*Len_no_hit,"XGboost-based":[0]*Len_no_hit},index=no_hit_set)
    end_stat=pd.concat([stat_inthree,no_hit_df])
    end_stat["Credible grade"]=end_stat.sum(axis=1)
    end_stat.index.name="Query_name"
    end_stat.to_csv("{}/Intermediate_dir/All_detect_detail.txt".format(OUT),sep="\t")
    dia_with_label=di_raw[["Query_name","tar_name"]].merge(MOPD_ID2label,left_on="tar_name",right_on="MOPD_ID").drop(columns="tar_name")
    if Level=="default":
        Grade=2
    elif Level=="strict":
        Grade=3
    elif Level=='loose':
        Grade=1
    else:
        sys.exit("ERROR: The input level is not in default|strict|loose!")
    end_stat_fil=end_stat[end_stat["Credible grade"] >= Grade]
    end_stat_fil.index.name=None
    end_stat_fil_out=pd.merge(end_stat_fil[["Credible grade"]],dia_with_label,left_index=True,right_on="Query_name",how="left")
    end_stat_fil_out["MOPD_ID"]=end_stat_fil_out["MOPD_ID"].fillna("-")
    end_stat_fil_out=end_stat_fil_out[["Query_name","Credible grade","MOPD_ID"]]
    #添加diamond检查步骤：
    if not NO_CHECK:
        print("---Start checking procedure---\n")
        end_stat_fil_out.to_csv("{}/Intermediate_dir/All_detect_as_MOP_pre_forcheck.txt".format(OUT),index=None,sep="\t")
        with open("{}/Intermediate_dir/All_detect_as_MOP_pre_forcheck.txt".format(OUT)) as f:
            count_ = len(f.readlines())
        if count_>1:
            os.system('cut -f1 ${OUT}/Intermediate_dir/All_detect_as_MOP_pre_forcheck.txt|seqkit grep -j ${THREAD} -f - ${IN} 2> /dev/null |diamond blastp -k 1 -p ${THREAD} -d ${CHECK_DB} -q - |awk -F"\t" \'$2~/^Not_methane:_:/ \'|cut -f 1  > ${OUT}/Intermediate_dir/NOT_MOP_IN_CHECK.tsv')
            if os.path.getsize("{}/Intermediate_dir/NOT_MOP_IN_CHECK.tsv".format(OUT)) !=0:
                end_stat_fil_out= end_stat_fil_out[~(end_stat_fil_out["Query_name"].isin(pd.read_csv("{}/Intermediate_dir/NOT_MOP_IN_CHECK.tsv".format(OUT),header=None)[0].tolist()))]
        end_stat_fil_out.to_csv("{}/Intermediate_dir/All_detect_as_MOP.txt".format(OUT),index=None,sep="\t")
        print("---Checking procedure complete---\n")
    else:
        end_stat_fil_out.to_csv("{}/Intermediate_dir/All_detect_as_MOP.txt".format(OUT),index=None,sep="\t")
    os.system('cut -f1 ${OUT}/Intermediate_dir/All_detect_as_MOP.txt|seqkit grep -j ${THREAD} -f - ${IN} > ${OUT}/Intermediate_dir/All_detect_as_MOP.faa 2> /dev/null')

#添加使用KOFAM进行标签匹配
def re_label(OUT,HMM_DB_KO,THREAD):
    os.environ['OUT']=str(OUT)
    os.environ['THREAD']=str(THREAD)
    os.environ['HMM_DB_KO']=str(HMM_DB_KO)
    if os.path.getsize("{}/Intermediate_dir/All_detect_as_MOP.faa".format(OUT)) !=0:
        os.system('mkdir ${OUT}/Intermediate_dir/hmm_res_split_relabel;for i in `ls ${HMM_DB_KO}*hmm`;do x=`basename ${i} |sed \'s/\.hmm$//g\'`;echo "hmmsearch --tblout ${OUT}/Intermediate_dir/hmm_res_split_relabel/${x}_seq.txt -o /dev/null --noali --cpu 1 ${i} ${OUT}/Intermediate_dir/All_detect_as_MOP.faa";done|parallel -j ${THREAD}')
        os.system('ls ${OUT}/Intermediate_dir/hmm_res_split_relabel/*seq.txt|xargs cat |grep -v "^#"|awk  \'{print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6}\' > ${OUT}/Intermediate_dir/HMM_kofam_res.txt')
        detect_as_MOP=pd.read_csv("{}/Intermediate_dir/All_detect_as_MOP.txt".format(OUT),sep="\t")
        if os.path.getsize("{}/Intermediate_dir/HMM_kofam_res.txt".format(OUT)) !=0:
            HMM_KO=pd.read_csv("{}/Intermediate_dir/HMM_kofam_res.txt".format(OUT),sep="\t",header=None)
            HMM_KO_max_score=HMM_KO.loc[HMM_KO.groupby(0)[5].idxmax()]
            KO2gene={"K16157":"mmoX","K16158":"mmoY","K16159":"mmoZ","K16160":"mmoB","K16161":"mmoC","K16162":"mmoD","K10944":"pmoA","K10945":"pmoB","K10946":"pmoC"}
            for i,x in HMM_KO_max_score.iterrows():
                if x[4]<1e-3:
                    HMM_KO_max_score.loc[i,"MOP type"]=KO2gene[x[2]]
                else:
                    HMM_KO_max_score.loc[i,"MOP type"]=KO2gene[x[2]]+" like MOP"
            HMM_KO_max_score["KO"]=HMM_KO_max_score[2]
            detect_as_MOP_with_ann=pd.merge(detect_as_MOP,HMM_KO_max_score[[0,"KO","MOP type"]],left_on="Query_name",right_on=0,how="left").fillna("Unclassified MOP")
            detect_as_MOP_with_ann=detect_as_MOP_with_ann[["Query_name","MOP type","KO","MOPD_ID","Credible grade"]]
            detect_as_MOP_with_ann.to_csv("{}/Intermediate_dir/detect_as_MOP_with_ann.txt".format(OUT),index=None,sep="\t")
        else:
            detect_as_MOP_with_ann=detect_as_MOP.copy()
            detect_as_MOP_with_ann["KO"]="-"
            detect_as_MOP_with_ann["MOP type"]="Unclassified MOP"
            detect_as_MOP_with_ann=detect_as_MOP_with_ann[["Query_name","MOP type","KO","MOPD_ID","Credible grade"]]
            detect_as_MOP_with_ann.to_csv("{}/Intermediate_dir/detect_as_MOP_with_ann.txt".format(OUT),index=None,sep="\t")
        return detect_as_MOP_with_ann
def extract_MOP(OUT,THREAD,IN,end_stat_fil_out):
    os.environ['OUT']=str(OUT)
    os.environ['THREAD']=str(THREAD)
    os.environ['IN']=str(IN)

    if os.path.getsize("{}/Intermediate_dir/All_detect_as_MOP.faa".format(OUT)) !=0:
        os.system('seqkit fx2tab -i ${OUT}/Intermediate_dir/All_detect_as_MOP.faa > ${OUT}/Intermediate_dir/MOP_seq2tab.txt')
        seq_tab=pd.read_csv("{}/Intermediate_dir/MOP_seq2tab.txt".format(OUT),sep="\t",header=None)
        seq_tab=seq_tab.merge(end_stat_fil_out,left_on=0,right_on="Query_name",how="left")
        seq_tab["Header"]=seq_tab["Query_name"].astype(str)+" "+seq_tab["MOPD_ID"].astype(str)+":"+seq_tab["MOP type"].astype(str)+" "+"credible lv."+seq_tab["Credible grade"].astype(str)
        seq_tab[["Header",1]].to_csv("{}/Intermediate_dir/MOP_pre_tab.txt".format(OUT),sep="\t",header=None,index=None)
        os.system('seqkit tab2fx ${OUT}/Intermediate_dir/MOP_pre_tab.txt > ${OUT}/Intermediate_dir/All_detect_as_MOP_re_header.faa' )

def clean(OUT,Intermediate):
    if os.path.exists("{}/Intermediate_dir/All_detect_as_MOP_re_header.faa".format(OUT)):
        shutil.copy("{}/Intermediate_dir/All_detect_as_MOP_re_header.faa".format(OUT),"{}/MOP_detect.faa".format(OUT))
        shutil.copy("{}/Intermediate_dir/detect_as_MOP_with_ann.txt".format(OUT),"{}/MOP_info_from_MOPDT.txt".format(OUT))
    shutil.copy("{}/Intermediate_dir/All_detect_detail.txt".format(OUT),"{}/All_detect_level_from_MOPDT.txt".format(OUT))
    if not Intermediate:
        shutil.rmtree("{}/Intermediate_dir/".format(OUT))
