#!/usr/bin/env bash
#AUTHER:LUCAS
#DATE:20250224
#GOAL:输入fastq序列根据MOPD和Pseudo-MOPD数据库估计甲烷氧化基因的丰度
#USAGE:脚本 输出文件夹 线程数 输入的序列.fq（若为双端则输在后面即可）
#支持单端序列和双端序列：
#Example：estimate_MOP_abun.sh output_dir 190 x.R1.fq x.R2.fq
##注意保证双端序列header名一致（空格前一致，如某些序列为.../1 .../2命名双端序列则有问题，需要输入前人为修改为相同header）

des_dir=`realpath $1`
Thread=$2
Read=${@:3}

echo "Attention! If You input pair-read FastQ files, make sure the header same!"
echo "#### Start with ${Thread} threads on ${Read} ####"
RANDOM_1=`head -n 20 /dev/urandom | cksum |cut -f1 -d " "`
mkdir ${des_dir} &> /dev/null
#合并输入的双端/单 一文件
##对输入的
seqkit replace -p '^' -r 'X1^_^' `echo ${Read}| awk '{print $1}'`> ${des_dir}/X_${RANDOM_1}_1_tmp
seqkit replace -p '^' -r 'X2^_^' `echo ${Read}| awk '{print $2}'`> ${des_dir}/X_${RANDOM_1}_2_tmp 2> /dev/null
cat ${des_dir}/X_${RANDOM_1}* > ${des_dir}/merge_${RANDOM_1}
#diamond将合并的文件和MOPD_rep比对
echo "#### Diamond on pos-Database ####"
diamond blastx -p ${Thread} -k 1 --db `dirname $0`/DB/MOPD_rep.dmnd -q ${des_dir}/merge_${RANDOM_1}|cut -f1 > ${des_dir}/matches_fmt6
#提取比对上的序列再和check_db.dmnd比对
echo "#### Diamond on psedo-Database ####"
cat ${des_dir}/matches_fmt6| seqkit grep -j ${Thread} -f - ${des_dir}/merge_${RANDOM_1} 2> /dev/null |diamond blastx -k 1 -p ${Thread} -d `dirname $0`/DB/check_db.dmnd -q -|awk -F '\t' '$2~/^Not_methane:_:/ '|cut -f1 > ${des_dir}/Not_methane
#取差集，去掉可以比对到非MOP数据库的序列ID
sort ${des_dir}/matches_fmt6 ${des_dir}/Not_methane ${des_dir}/Not_methane| uniq -u > ${des_dir}/END_MAP_READ
#考虑对于双端序列若其中一端可以比对上则保留认为比对上一条
cat ${des_dir}/END_MAP_READ|sed 's/^.*\^_\^//g'|sort|uniq |wc -l > ${des_dir}/MOPDT_count
seqkit stat -T `echo ${Read}| awk '{print $1}'`|cut -f4|sed '1d' > ${des_dir}/IN_read_count_total
x1=`cat ${des_dir}/MOPDT_count`
x2=`cat ${des_dir}/IN_read_count_total`
echo "scale=6; ${x1}/${x2}" | bc|sed 's/^/0/g' > ${des_dir}/Proportion_MOPDT
echo "#### Cleaning ####"
mkdir ${des_dir}/inter_files_${RANDOM_1}
mv ${des_dir}/END_MAP_READ  ${des_dir}/IN_read_count_total  ${des_dir}/matches_fmt6  ${des_dir}/merge_${RANDOM_1}  ${des_dir}/MOPDT_count  ${des_dir}/Not_methane ${des_dir}/X_*_tmp ${des_dir}/inter_files_${RANDOM_1}

echo "#### End ####"
