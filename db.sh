#!/bin/sh
USERNAME=$1
echo "Starting download";
curl -L -o qa.sql https://www.dropbox.com/s/aqop2af4i39pe1w/qa.sql?dl=1;
curl -L -o graph.sql https://www.dropbox.com/s/7mb6snalnxndlxp/graph.sql?dl=1;
curl -L -o ssb.sql https://www.dropbox.com/s/y609n91exdishyf/ssb.sql?dl=1;
curl -L -o tpch.sql https://www.dropbox.com/s/kdk4iq9kngu5cr2/tpch.sql?dl=1;
echo "Starting DB creation";
mysql -u $USERNAME -p < qa.sql;
mysql -u $USERNAME -p < graph.sql;
mysql -u $USERNAME -p < ssb.sql;
mysql -u $USERNAME -p < tpch.sql;