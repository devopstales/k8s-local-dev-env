set -e

cp -rLf /tmp/frr/* /etc/frr/

export TINI_SUBREAPER=true

/sbin/tini -- /usr/lib/frr/docker-start &
attempts=0
until [[ -f /etc/frr/frr.log || $attempts -eq 60 ]]; do
    sleep 1
    attempts=$(( $attempts + 1 ))
done
tail -f /etc/frr/frr.log