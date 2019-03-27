create table Users (
	userno int unsigned not null auto_increment primary key,
	username varchar(128) not null unique,
	pw varchar(256) not null,
	birthdate varchar(13)  not null, 
	city varchar(128) not null,
	gender varchar(5) not null,
	join_date  timestamp not null DEFAULT CURRENT_TIMESTAMP,
	job varchar(128) not null,
	email varchar(128) not null unique,
	following_cnt int(11) not null default 0,
	follower_cnt int(11) not null default 0,
    ismember boolean not null default 1
);

create table Follow (			
	follow_id int unsigned not null auto_increment primary key,
	userno int unsigned not null,
	following int unsigned not null,

	constraint foreign key fk_users(userno) references Users(userno),
	constraint foreign key fk_users_following(following) references Users(userno),
    constraint uq_follow unique (userno, following)
);

create table Lists (
	list_id int unsigned not null auto_increment primary key,
	userno int unsigned not null,
	list_txt varchar(4096),
	likecnt int(11) not null default 0,
	hatecnt int(11) not null default 0,
	public boolean default 1,
	list_date timestamp not null DEFAULT CURRENT_TIMESTAMP,

	constraint foreign key fk_users(userno) references Users(userno)
);

create table Cmt (
	cmt_id int unsigned not null auto_increment primary key,
	userno int unsigned not null,
	cmt_txt varchar(3000),
	cmt_date timestamp not null DEFAULT CURRENT_TIMESTAMP,
	list_id int unsigned not null, 
	cmt_like int(11) not null default 0,
	cmt_hate int(11) not null default 0,

	constraint foreign key fk_users(userno) references Users(userno),
	constraint foreign key fk_lists(list_id) references Lists(list_id)
);

create table Ranking (
	ranking_id int unsigned not null auto_increment primary key,
	list_id int unsigned not null,
	ranking_date timestamp not null DEFAULT CURRENT_TIMESTAMP,
	rank int not null,

	constraint foreign key fk_lists(list_id) references Lists(list_id),
    constraint uq_ranking unique (list_id, ranking_date)
);

create table Likecnt (
	likecnt_id int unsigned not null auto_increment primary key,
	list_id int unsigned not null unique,
	today_like int(11) not null default 0,

	constraint foreign key fk_lists(list_id) references Lists(list_id)
);

create table DM (
	dm_id  int unsigned not null auto_increment primary key,
	userno int unsigned not null,
	receiver int unsigned not null,
	dm_txt varchar(4096),
	dm_date timestamp not null  DEFAULT CURRENT_TIMESTAMP,

	constraint foreign key fk_users(userno) references Users(userno),
	constraint foreign key fk_users_receiver(receiver) references Users(userno)
);
