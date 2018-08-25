import fabric
import sys
import time
import os
import string

target_host='tutturu.party'
username='a.kulyashov'
ls=[]

#connection and getting ls in /etc/ with cron grep
with fabric.Connection(host=str(target_host), user=str(username), port=22) as conn:
	ls_cron=conn.run('ls -p /etc/ | grep cron', hide=True)
	ls_output=ls_cron.stdout
	ls=str(ls_output).splitlines()
	
	
	
	#loop that ls's directories and cat's files
	#for file_or_dir in ls:
		#if "/" in file_or_dir:
			#print 'contents of '+str(file_or_dir)
			#ls_subdir=conn.run('ls -p /etc/'+str(file_or_dir))
		#else:
			#print 'contents of '+str(file_or_dir)
			#cat_file=conn.run('cat /etc/'+str(file_or_dir))
	
	
	#processing of directories with cron in the name, for now cron.d only, manualy set
	dir_to_ansible='cron.d/'		
	if dir_to_ansible in ls:
		ls_subdir=str(conn.run('ls -p /etc/'+str(dir_to_ansible), hide=True).stdout).splitlines()
		
		yml_file=open("crond.yml", "w+")
		yml_file.truncate()
		tmp_cat_crond=open("cat_crond_tmp.txt", "w+")
		
		#handling every file found in directory
		for target_file in ls_subdir:
			if '/' not in str(target_file):
				tmp_cat_crond.seek(0)
				tmp_cat_crond.truncate()
				tmp_cat_crond.write(conn.run('cat /etc/'+str(dir_to_ansible)+str(target_file), hide=True).stdout.encode('utf-8'))
				tmp_cat_crond.seek(0)
				
				#taking care of strings starting with a digit or *
				for line in tmp_cat_crond:
					cron_task=[]
					if line[0].isdigit()==True or str(line[0])==str("*"):
						cron_task=line.split()
						cron_task[6:len(cron_task)]=[' '.join(cron_task[6:len(cron_task)])]
						cron_task[len(cron_task)-1]=str(cron_task[len(cron_task)-1]).rstrip('\n')
						cron_min=cron_task[0]
						cron_hour=cron_task[1]
						cron_day=cron_task[2]
						cron_month=cron_task[3]
						cron_week=cron_task[4]
						cron_user=cron_task[5]
						cron_job=cron_task[6]
						yml_file.write("cron:\n	"+'name: '+str(target_file)+'\n	'+'minute: '+str(cron_min)+'\n	'+'hour: '+str(cron_hour)+'\n	'+'day: '+str(cron_day)+'\n	'+'month: '+str(cron_month)+'\n	'+'weekday: '+str(cron_week)+'\n	'+'user: '+str(cron_user)+'\n	'+'job: '+str(cron_job)+'\n')
				
				