SRCDIR=~/Dropbox/OrionMuse/LineMaps
DESTDIR=~/tmp/musedata
rsync -avP $SRCDIR/{linesum,mean,sigma}-*-[0-9][0-9][0-9][0-9].fits $DESTDIR
