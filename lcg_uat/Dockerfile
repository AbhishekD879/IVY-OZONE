#FROM 740335462382.dkr.ecr.eu-west-2.amazonaws.com/crlat-voltron-base:3.6.8.5
# FROM 740335462382.dkr.ecr.eu-west-2.amazonaws.com/crlat-voltron-base:3.6.8.6.1_rust
FROM 740335462382.dkr.ecr.eu-west-2.amazonaws.com/crlat-voltron-base:3.12.1_rust
ENV http_proxy=http://atvp1xipxy002.apz.unix:3128
ENV https_proxy=http://atvp1xipxy002.apz.unix:3128
ENV no_proxy="qa2.myaccount.ladbrokes.com,bpp.internal.tst.ladbrokes.com,betting-ms-beta.internal.coral.co.uk,betting-ms-beta.internal.ladbrokes.com,betting-ms.internal.coral.co.uk,betting-ms.internal.ladbrokes.com,*.gvcgroup.corp;*.Bwin.*;*.cms.bwin;*.bwinparty.com;*.bwinparty.corp;*.bpty;*.partypoker.com;*.partypoker.es;*.partycasino.*;*.premium.*;*.partypremium.*;*.partygaming.com;*.partygaming.local;*.sportingbet.*;*.internal.sportingbet.ro;*.finadmin.sportingbet.com;mal-xenwebsvr01.sbet-emea.ads;*.betboo.*;*.coral.local;*.icepor.com;*.itsfogo.com;*.ivycomptech.co.in;*.Vistabet.*;webpool02.is.icepor.com;*.brands.local;*.dimensiondata.com;admin.kalixa.com.*;*.csmng.intranet;www.csmng.intranet;*.igmg;wiki.openbet.com;gvcisr.int;*.wms.com;*.iglobalmedia.com;bvservices-stage.webdollar.com;services.bverified.com;gi1p1udoms001.prod.gi01.bpty;nj0p1udora999.prod.nj01.bpty;gi1p1udoms001.prod.gi01.bpty;oem.mgmt.nj02.bpty;baf01.im.cozygames.com;preprod.*;preprod-*;dev.*;*.env.works;*.e7new.com;qa2.*;qa5.*;test-*;test2.*;*.test2;*.apz.unix;*.dbz.unix;repo.nt.lan;wss.plc-gc.com;wss://bwin.spingames.net;kibana.*;my.gvcgroup.com;meet.gvcgroup.com;lyncdiscoverinternal.gvcgroup.com;webpool01.is.icepor.com;gi2m1xiidm001.gi02.bpty;gi2m1xiidm002.gi02.bpty;help.nj.playmgm.com.cms.bwin.prod;preprod-m-lcm.ladbrokes.com;tools.ladbrokes.com;tst1-mobile-lcm.ladbrokes.com;tst2-mobile-lcm.ladbrokes.com;tst2-sports-lcm.ladbrokes.com;tst2-feeds-lcm.ladbrokes.com;stg-feeds-lcm.ladbrokes.com;feeds-obr4-tst2.ladbrokes.com;feeds-obr4-tst2-ext.ladbrokes.com;feeds-obr4-stg.ladbrokes.com;portal-admin-AccountOne-test.ladbrokes.com;portal-admin-accountone-stg.ladbrokes.com;feeds-obr2-stg-ext.coral.co.uk;jira.ladbrokes.co.uk;obbackoffice-stg2.gib1.egalacoral.com;*.betmgm.com;10.*;172.*;10.185.28.72.*;27.251.125.211;45.127.102.252;66.224.70.114;66.224.70.115;81.88.161.44;81.88.161.45;115.112.80.111;192.168.104.*;192.168.107.*;192.168.*;203.153.210.7;217.135.225.4;217.135.225.5,icepor.com,*.coral.co.uk,qa2.sports.ladbrokes.com,jenkins-vie.coral.co.uk,nexus-vie.coral.co.uk,obbackoffice-tst2.ladbrokes.com,obbackoffice-tst2.internal.ladbrokes.com,backoffice-tst2.coral.co.uk,selenoid,172.17.0.2,172.17.0.3,172.17.0.4,172.17.0.4,172.17.0.5,172.17.0.6,172.17.0.7,172.17.0.8,172.17.0.9,172.17.0.10,172.17.0.11,172.17.0.12,172.17.0.13,172.17.0.14,172.17.0.15,172.17.0.16,172.17.0.17,172.17.0.18,172.17.0.19,172.17.0.20,localhost,grim-invictus.coral.co.uk,grim-invictus.ladbrokes.com,spartans2-invictus.coral.co.uk,spartans2-excalibur.ladbrokes.com"
COPY ./ /voltron
WORKDIR /voltron
RUN curl -o /etc/ssl/certs/ca-certificates.crt https://dev_voltron:d7N2f9rd98KEiP3bhF@nexus-vie.coral.co.uk/repository/certs/certs/tls-ca-bundle.pem
RUN curl -o /etc/ssl/certs/wildcard.internal.tst.ladbrokes.com https://dev_voltron:d7N2f9rd98KEiP3bhF@nexus-vie.coral.co.uk/repository/certs/certs/wildcard.internal.coral.co.uk.pem
RUN curl -o /etc/ssl/certs/wildcard.internal.tst.ladbrokes.com https://dev_voltron:d7N2f9rd98KEiP3bhF@nexus-vie.coral.co.uk/repository/certs/certs/wildcard.internal.tst.ladbrokes.com
RUN curl -o /etc/ssl/certs/wildcard.internal.tst.coral.co.uk https://dev_voltron:d7N2f9rd98KEiP3bhF@nexus-vie.coral.co.uk/repository/certs/certs/wildcard.internal.tst.coral.co.uk
RUN export PIP_EXTRA_INDEX_URL=https://pypi.org/simple
RUN sudo rm -rf /etc/pip.conf
COPY pip.conf /etc
RUN pip install wheel
RUN pip install transformers==4.41.1
RUN pip install tokenizers==0.19.1
RUN pip install greenlet==3.0.3
RUN pip install browserstack-local-1.2.7.tar
# RUN pip install selenium-fwproxy-3.141.0.tar
RUN pip install -r requirements.txt
RUN pip install pyyaml==6.0.1
ENV LOCATION_NAME=AWS_GRID
ENV IGNORE_TEST_PATHS=''
ENV OX_HOSTNAME=bet-tst1.coral.co.uk
ENV TEST_PATH=./tests_uat
ENV RUN_ON='mobile, desktop'
ENV MARK='tst2'
ENV PYTEST_TIMEOUT='425'
ENV CUSTOM_MARKS=''
ENV DISCOVERY_DIR='/voltron/discovered-tests'
ENV REPORTS_DIR='/voltron/reports'
ENV ATTACHMENTS_DIR='/voltron/attachments'
VOLUME $DISCOVERY_DIR
VOLUME $REPORTS_DIR
VOLUME $ATTACHMENTS_DIR
