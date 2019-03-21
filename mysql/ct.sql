create table User (
	userno int unsigned not null auto_increment primary key,
	username varchar(128) not null,
	pw varchar(256) not null,
	birthdate varchar(13)  NOT NULL, 
	city varchar(128) not null,
	gender varchar(5) not null,
	join_date  timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	job varchar(128) not null default '',
	email varchar(128) unique,
	following_cnt int(11) not null default 0,
	follower_cnt int(11) not null default 0,
	flag boolean default 1
);

create table Follow (			
	follow_id int unsigned not null auto_increment primary key,
	userno int unsigned not null,
	following int unsigned not null,

	constraint foreign key fk_user(userno) references User(userno),
	constraint foreign key fk_user_following(following) references User(userno),
    constraint uq_follow unique (userno, following)
);

create table List (
	list_id int unsigned not null auto_increment primary key,
	userno int unsigned not null,
	list_txt varchar(4096),
	likecnt int(11) not null default 0,
	hatecnt int(11) not null default 0,
	public boolean default 1,
	list_date timestamp NULL DEFAULT CURRENT_TIMESTAMP,

	constraint foreign key fk_user(userno) references User(userno)
);

create table Comment (
	cmt_id int unsigned not null auto_increment primary key,
	userno int unsigned not null,
	cmt_txt varchar(3000),
	cmt_date timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	list_id int unsigned not null, 
	cmt_like int(11) not null default 0,
	cmt_hate int(11) not null default 0,

	constraint foreign key fk_user(userno) references User(userno),
	constraint foreign key fk_list(list_id) references List(list_id)
);

create table Ranking (
	ranking_id int unsigned not null auto_increment primary key,
	list_id int unsigned not null,
	ranking_date timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	rank int not null,

	constraint foreign key fk_list(list_id) references List(list_id),
    constraint uq_ranking unique (list_id, ranking_date)
);

create table Likecnt (
	likecnt_id int unsigned not null auto_increment primary key,
	list_id int unsigned not null unique,
	today_like int(11) not null default 0,

	constraint foreign key fk_list(list_id) references List(list_id)
);

create table DM (
	dm_id  int unsigned not null auto_increment primary key,
	userno int unsigned not null,
	receiver int unsigned not null,
	dm_txt varchar(4096),
	dm_date timestamp NULL DEFAULT CURRENT_TIMESTAMP,

	constraint foreign key fk_user(userno) references User(userno),
	constraint foreign key fk_user_receiver(receiver) references User(userno)
);
