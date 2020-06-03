CREATE DATABASE demo;
GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost' IDENTIFIED BY '12345';
GRANT ALL PRIVILEGES ON *.* TO 'webapp'@'localhost' IDENTIFIED BY 'P@ssw0rd!';
USE demo;

CREATE TABLE IF NOT EXISTS `failed_login_count` (
  `ip_addressport` varchar(255) NOT NULL,
  `failed_count` varchar(255) NOT NULL,
  `success_count` varchar(255) NOT NULL,
  `date` datetime NOT NULL
)

CREATE TABLE IF NOT EXISTS `failed_login_attempt` (
  `ip_address` varchar(255) NOT NULL,
  `date` datetime NOT NULL
)
CREATE TABLE IF NOT EXISTS `kdd_content_features2` (
  ` ip_addressport ` varchar(255) NOT NULL,
  ` hot ` varchar(255) NOT NULL,
  ` num_failed_login ` varchar(255) NOT NULL,
  ` logged_in ` varchar(255) NOT NULL,
  ` num_compromised ` varchar(255) NOT NULL,
  ` root_shell ` varchar(255) NOT NULL,
  ` su_access ` varchar(255) NOT NULL,
  ` num_root` varchar(255) NOT NULL,
  ` num_file_creations ` varchar(255) NOT NULL,
  ` num_shells ` varchar(255) NOT NULL,
  ` num_access_files ` varchar(255) NOT NULL,
  ` num_outbound_cmds ` varchar(255) NOT NULL,
  ` is_host_login ` varchar(255) NOT NULL,
  ` is_guest ` varchar(255) NOT NULL,
  ` ip_addressport ` varchar(255) NOT NULL,
`date` datetime NOT NULL
)

