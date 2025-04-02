import sys 
try:
    import iFeatureOmegaCLI
except:
    sys.exit("CRITICAL ERROR: iFeatureOmegaCLI (python package) not found")
try:
    import xgboost as xgb
except:
    sys.exit("CRITICAL ERROR: xgboost (python package) not found")
try:
    import pandas as pd
except:
    sys.exit("CRITICAL ERROR: pandas (python package) not found")


def main(pro_path,XG_OUT_PATH,Include_feat,XG_model):
    def class_MOP(x):
        if x<0.5:
            return "N_MOP"
        else:
            return "MOP"
    # Input
    In_fea=pd.read_csv(Include_feat ,header=None)[0].tolist()
    pro=iFeatureOmegaCLI.iProtein(pro_path)
    pro.get_descriptor("AAC")
    AAC_feature=pro.encodings
    pro=iFeatureOmegaCLI.iProtein(pro_path)
    pro.get_descriptor("DPC type 2")
    DPC_feature=pro.encodings
    pro=iFeatureOmegaCLI.iProtein(pro_path)
    pro.get_descriptor("CTDC")
    CTDC_feature=pro.encodings
    pro=iFeatureOmegaCLI.iProtein(pro_path)
    pro.get_descriptor("CTDT")
    CTDT_feature=pro.encodings
    pro=iFeatureOmegaCLI.iProtein(pro_path)
    pro.get_descriptor("CTDD")
    CTDD_feature=pro.encodings

    all_feature=pd.concat([AAC_feature,CTDC_feature,DPC_feature,CTDT_feature,CTDD_feature],axis=1)[In_fea]

    model_xgb= xgb.Booster()
    model_xgb.load_model(XG_model)
    pr=pd.DataFrame({"Predic":[class_MOP(i) for i in model_xgb.predict(xgb.DMatrix(all_feature))]},index=all_feature.index)
    pr.to_csv(XG_OUT_PATH,header=None,sep="\t")

