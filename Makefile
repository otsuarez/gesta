WORKING_DIR="/var/devel"
TODAY=`date +'%Y%m%d%H%M'`
HOY=${TODAY}

# Just a backup script ;-)

inicializar:
	mkdir -p ${WORKING_DIR}/sites/salvas

salva:
	@mysqldump -u gesta -psecret gestadns > templates/gestadns.sql
	tar zcf ${WORKING_DIR}/sites/salvas/gesta.`date +'%Y%m%d%H%M'`.tgz ${WORKING_DIR}/sites/gesta/

today:	
	echo ${TODAY}
hoy:	
	echo ${HOY}
