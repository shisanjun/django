select userenv('language') from dual;




select *  from TSC_HEALTHCHECK_RESULTALL;


        select content,timestamp from TSC_BIGDATA_CHECK
        where bigdatatype='HDFS' and item ='NumDeadDataNodes'
        and timestamp in (select content,timestamp from TSC_BIGDATA_CHECK
        where bigdatatype='HDFS' and item ='NumDeadDataNodes' and rownum<=1 order by  timestamp desc)
        
          select * from TSC_BIGDATA_CHECK
       where bigdatatype='HDFS' and item ='NumDeadDataNodes' and rownum<=10 order by  timestamp desc
       
          select content,timestamp from TSC_BIGDATA_CHECK
       where bigdatatype='HDFS' and item ='CapacityRemainingRate' and rownum<=1 order by  timestamp desc
       
       
   select * from TSC_HEALTHCHECK_CONFIG;
   select systemid,systemname,sum(score) from (select b.systemid,b.systemname,a.checkeng,a.score,a.addend 
   from TSC_HEALTHCHECK_RESULTALL a join TSC_HEALTHCHECK_CONFIG b 
   on a.checkeng=b.checkeng)
   group by systemid,systemname
   
   
   select * from TSC_HEALTHCHECK_RESULT
