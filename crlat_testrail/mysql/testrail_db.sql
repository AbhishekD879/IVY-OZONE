CREATE DATABASE testrail DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
CREATE USER 'testrail'@'%' IDENTIFIED BY 'secret#1';
GRANT ALL PRIVILEGES ON *.* TO 'testrail'@'%' IDENTIFIED BY 'secret#1' WITH GRANT OPTION;
