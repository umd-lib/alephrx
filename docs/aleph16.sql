# MySQL dump 8.14
#
# Host: localhost    Database: aleph16
#--------------------------------------------------------
# Server version	3.23.38

#
# Table structure for table 'RXreply'
#

CREATE TABLE RXreply (
  id int(11) NOT NULL default '0',
  parent_id int(11) NOT NULL default '0',
  name varchar(50) default NULL,
  date datetime default NULL,
  text text,
  timestamp datetime default NULL,
  itd varchar(10) default NULL
) TYPE=MyISAM;

#
# Table structure for table 'kbase'
#

CREATE TABLE kbase (
  id int(11) NOT NULL auto_increment,
  service varchar(20) default NULL,
  subject varchar(50) default NULL,
  create_date date default NULL,
  add_date timestamp(14) NOT NULL,
  summary varchar(50) default NULL,
  text mediumtext,
  ref varchar(50) default NULL,
  PRIMARY KEY  (id)
) TYPE=MyISAM;

#
# Table structure for table 'people'
#

CREATE TABLE people (
  id int(11) NOT NULL auto_increment,
  grp varchar(20) default NULL,
  campus varchar(6) default NULL,
  phone varchar(14) default NULL,
  name varchar(100) default NULL,
  email varchar(30) default NULL,
  timestamp datetime default NULL,
  PRIMARY KEY  (id)
) TYPE=MyISAM;

#
# Table structure for table 'reply'
#

CREATE TABLE reply (
  id int(11) NOT NULL auto_increment,
  parent_id int(11) NOT NULL default '0',
  name varchar(50) default NULL,
  date datetime default NULL,
  text text,
  timestamp datetime default NULL,
  itd varchar(10) default NULL,
  PRIMARY KEY  (id),
  FULLTEXT KEY ReplyTextName (text,name)
) TYPE=MyISAM;

#
# Table structure for table 'report'
#

CREATE TABLE report (
  id int(11) NOT NULL default '0',
  date date default NULL,
  grp varchar(15) default NULL,
  status varchar(18) default NULL,
  summary varchar(255) default NULL,
  text text,
  supress char(3) default 'no',
  cataloger varchar(50) default NULL,
  assigned varchar(50) default NULL,
  timestamp datetime default NULL,
  updated datetime default NULL,
  version varchar(20) default NULL,
  PRIMARY KEY  (id),
  FULLTEXT KEY ReportTextSummary (text,summary)
) TYPE=MyISAM;

#
# Table structure for table 'response'
#

CREATE TABLE response (
  id int(11) NOT NULL auto_increment,
  parent_id int(11) NOT NULL default '0',
  name varchar(50) default NULL,
  date datetime default NULL,
  text text,
  timestamp datetime default NULL,
  itd varchar(10) default NULL,
  PRIMARY KEY  (id)
) TYPE=MyISAM;

#
# Table structure for table 't'
#

CREATE TABLE t (
  max_date datetime default NULL,
  parent_id int(11) default NULL
) TYPE=MyISAM;

