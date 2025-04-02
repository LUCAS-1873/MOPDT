import pandas as pd
import sys

def main(diamond_IN,INPUT_SEQ_LEN,diamond_OUT):
    MOPD_pre_len=pd.read_csv("{}/DB/MOPD_rename_pro_length".format(sys.path[0]),sep="\t",header=None)
    MOPD_pre_len.columns=["tar_name","tar_len"]
    INPUT_SEQ_LEN=pd.read_csv(INPUT_SEQ_LEN,sep="\t",header=None)
    INPUT_SEQ_LEN.columns=["Query_name","Query_len"]
    diamond_res=pd.read_csv(diamond_IN,sep="\t",header=None)
    diamond_res.columns=['qaccver' ,'saccver' ,'pident' ,'length' ,'mismatch' ,'gapopen' ,'qstart' ,'qend' ,'sstart' ,'send', 'evalue' ,'bitscore']
    merge_dia=pd.merge(left=diamond_res,
            right=MOPD_pre_len,right_on='tar_name',left_on='saccver',how="left").drop(columns="saccver").merge(INPUT_SEQ_LEN,left_on="qaccver",right_on="Query_name",how="left").drop(columns="qaccver")
    merge_dia['scov']=merge_dia['length']/merge_dia['tar_len']
    merge_dia['qcov']=merge_dia['length']/merge_dia['Query_len']
    merge_dia.to_csv(str(diamond_OUT),sep="\t",index=None)

