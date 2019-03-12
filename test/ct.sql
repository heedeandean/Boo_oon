drop table if exists User;

create table User (
	username,
    pw,
    birthdate,
    email,
    city,
    gender,
    regidate,
    job,
    following_cnt,
    follower_cnt
);

create table Follow (
	username,
    following
);

create table List (
	list_id,
    username,
    list_txt,
    likecnt,
    hatecnt,
    public,
    list_date
);

create table Comment (
	cmt_id,
    username,
    cmt_txt,
    cmt_date,
    list_id,
    cmt_like,
    cmt_hate
);

create table Ranking (

);

