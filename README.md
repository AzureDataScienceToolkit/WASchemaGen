# waschemagen
Recursively scans Azure Web Apps log directory and creates both table and partition schemas.

##Script syntax
<code>
usage: waschemagen.py [-h] [-v] table directory script 
                                                           
Azure Web Apps log Hive schema generator.                
                                                           
    positional arguments:                                      
      table       name of the hive table                       
      directory   name of HDFS directory (may be wasb://...)   
      script      name of generated script file                
                                                           
    optional arguments:                                        
      -h, --help  show this help message and exit              
      -v          verbose-prints some useful information       
</code>

##Basic usage example

###Generating table and partition schema script
<code>
waschemagen.py mylogtable wasb://mycontainer@mystorage.blob.core.windows.net/logs/ mylogs.hql
</code>
