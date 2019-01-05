#!/bin/bash
#
# gitutil       This shell script takes care of connect to GitHub.
#

STAMP=`date -R`
NETRC_L=~/.netrc
NETRC_W=~/_netrc

init() {
	NETRC=$1

	echo -e "Enter your Git Server..."
	read server
	echo -e "Enter your Git Name..."
	read username
	echo -e "Enter your Git Password..."
	read password
	echo -e "Enter your Email address..."
	read email

	echo "machine ${server}" > ${NETRC}
	echo "login ${username}" >> ${NETRC}
	echo "password ${password}" >> ${NETRC}
	git config --global user.name "${username}"
	git config --global user.email ${email}
}

update() {
	git add --all
	git pull
	git commit -m "automatic update by cargentiella at ${STAMP}"
	git push -u origin master
}

# See how we were called.
case "$1" in
  -l)
	init ${NETRC_L}
	;;
  -w)
  	init ${NETRC_W}
	;;
  *)
	update
esac
