# just a backup script ;-)
WORKING_DIR="/opt"
#WORKING_DIR="/var/devel"
TODAY=`date +'%Y%m%d%H%M'`
HOY=${TODAY}

inicializar:
	mkdir -p ${WORKING_DIR}/sites/salvas

salva:
	@mysqldump -u gesta -psecret gestadns > ${WORKING_DIR}/sites/gesta/templates/gestadns.sql
	@tar zcf ${WORKING_DIR}/sites/salvas/gesta.`date +'%Y%m%d%H%M'`.tgz ${WORKING_DIR}/sites/gesta/ >/dev/null 2>&1
	@echo gesta.`date +'%Y%m%d%H%M'`.tgz

today:	
	echo ${TODAY}
hoy:	
	echo ${HOY}

dirs:
	sudo chown -R osvaldo ${WORKING_DIR}/sites/chroot/
	python makedirs.py 
	sudo chown -R apache ${WORKING_DIR}/sites/chroot/

