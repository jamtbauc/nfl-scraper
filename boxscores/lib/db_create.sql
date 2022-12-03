-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS nfl.team
(
    name character varying(25) NOT NULL,
    locale character varying(15) NOT NULL,
    mascot character varying(15) NOT NULL,
    abbrev_pff character(3) NOT NULL,
    PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS nfl.player
(
	id character varying(10) NOT NULL,
    name character varying(30) NOT NULL,
    college character varying(100),
    dob date,
    career_start smallint DEFAULT 0,
    career_end smallint DEFAULT 0,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS nfl.official
(
    name character varying(25) NOT NULL,
    career_start smallint,
    career_end smallint,
    jersey_num smallint,
    PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS nfl.stadium
(
    name character varying(35) NOT NULL,
    city character varying(20),
    state character varying(20),
    surface character varying(10) NOT NULL,
    roof character varying(17) NOT NULL,
    PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS nfl.game
(
	id character(14) NOT NULL,
    date date NOT NULL,
    season smallint,
    week character varying(8) NOT NULL,
    attendance integer,
    stadium_id character varying(40) NOT NULL,
	game_duration time without time zone NOT NULL,
    roof_type character varying(6),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS nfl.official_game
(
	id serial NOT NULL,
	ref_position character varying(11) NOT NULL,
    official_id character varying(25) NOT NULL,
    game_id character(14) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS nfl.team_game
(
    id serial NOT NULL,
    team_id character varying(25) NOT NULL,
    game_id character(14) NOT NULL,
    won_toss boolean NOT NULL,
    toss_decision character varying(10),
    is_home boolean NOT NULL,
    is_favored boolean NOT NULL,
    spread numeric(3,1) NOT NULL,
    over_under numeric(3,1) NOT NULL,
    first_downs smallint NOT NULL DEFAULT 0,
    rush_atts smallint NOT NULL DEFAULT 0,
    rush_yds smallint NOT NULL DEFAULT 0,
    rush_tds smallint NOT NULL DEFAULT 0,
    pass_comps smallint NOT NULL DEFAULT 0,
    pass_atts smallint NOT NULL DEFAULT 0,
    pass_yds smallint NOT NULL DEFAULT 0,
    pass_tds smallint NOT NULL DEFAULT 0,
    pass_ints smallint NOT NULL DEFAULT 0,
    sacked smallint NOT NULL DEFAULT 0,
    sack_yds_lost smallint NOT NULL DEFAULT 0,
    net_pass_yds smallint NOT NULL DEFAULT 0,
    total_yds smallint NOT NULL DEFAULT 0,
    fumbles smallint NOT NULL DEFAULT 0,
    fumbles_lost smallint NOT NULL DEFAULT 0,
    turnovers smallint NOT NULL DEFAULT 0,
    penalties smallint NOT NULL DEFAULT 0,
    penalty_yds smallint NOT NULL DEFAULT 0,
    third_down_atts smallint NOT NULL DEFAULT 0,
    third_down_convs smallint NOT NULL DEFAULT 0,
    fourth_down_atts smallint NOT NULL DEFAULT 0,
    fourth_down_convs smallint NOT NULL DEFAULT 0,
    possession_time time without time zone NOT NULL,
    coach character varying(20) NOT NULL,
    score smallint NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS nfl.player_game
(
    id serial NOT NULL,
    player_id character varying(10) NOT NULL,
    tm_game_id integer NOT NULL,
    pass_comps smallint NOT NULL DEFAULT 0,
    pass_atts smallint NOT NULL DEFAULT 0,
    pass_yds smallint NOT NULL DEFAULT 0,
    pass_tds smallint NOT NULL DEFAULT 0,
    pass_ints smallint NOT NULL DEFAULT 0,
    sacked smallint NOT NULL DEFAULT 0,
    sack_yds_lost smallint NOT NULL DEFAULT 0,
    long_pass smallint NOT NULL DEFAULT 0,
    pass_rating numeric(4,1) NOT NULL,
    rush_atts smallint NOT NULL DEFAULT 0,
    rush_yds smallint NOT NULL DEFAULT 0,
    rush_tds smallint NOT NULL DEFAULT 0,
    long_rush smallint NOT NULL DEFAULT 0,
    rec_targets smallint NOT NULL DEFAULT 0,
    receptions smallint NOT NULL DEFAULT 0,
    rec_yds smallint NOT NULL DEFAULT 0,
    rec_tds smallint NOT NULL DEFAULT 0,
    long_rec smallint NOT NULL DEFAULT 0,
    fumbles smallint NOT NULL DEFAULT 0,
    fumbles_lost smallint NOT NULL DEFAULT 0,
    def_int smallint NOT NULL DEFAULT 0,
    def_int_yds smallint NOT NULL DEFAULT 0,
    def_int_tds smallint NOT NULL DEFAULT 0,
    long_def_int smallint NOT NULL DEFAULT 0,
    pass_defs smallint NOT NULL DEFAULT 0,
    def_sacks numeric(2,1) NOT NULL DEFAULT 0,
    def_tack_comb smallint NOT NULL DEFAULT 0,
    def_tack_solo smallint NOT NULL DEFAULT 0,
    def_tack_assist smallint NOT NULL DEFAULT 0,
    def_tack_loss smallint NOT NULL DEFAULT 0,
    def_qb_hits smallint NOT NULL DEFAULT 0,
    fumble_recs smallint NOT NULL DEFAULT 0,
    fumble_rec_yds smallint NOT NULL DEFAULT 0,
    fumble_rec_tds smallint NOT NULL DEFAULT 0,
    forced_fumbles smallint NOT NULL DEFAULT 0,
    kick_rets smallint NOT NULL DEFAULT 0,
    kick_ret_yds smallint NOT NULL DEFAULT 0,
    avg_kick_ret numeric(4,1) NOT NULL DEFAULT 0,
    kick_ret_tds smallint NOT NULL DEFAULT 0,
    long_kick_ret smallint NOT NULL DEFAULT 0,
    punt_ret smallint NOT NULL DEFAULT 0,
    punt_ret_yds smallint NOT NULL DEFAULT 0,
    avg_punt_ret numeric(4,1) NOT NULL DEFAULT 0,
    punt_ret_td smallint NOT NULL DEFAULT 0,
    long_punt_ret smallint NOT NULL DEFAULT 0,
    xpm smallint NOT NULL DEFAULT 0,
    xpa smallint NOT NULL DEFAULT 0,
    fgm smallint NOT NULL DEFAULT 0,
    fga smallint NOT NULL DEFAULT 0,
    punts smallint NOT NULL DEFAULT 0,
    punt_yds smallint NOT NULL DEFAULT 0,
    avg_punt numeric(3,1) NOT NULL DEFAULT 0.0,
    long_punt smallint NOT NULL DEFAULT 0,
    pass_first_downs smallint NOT NULL DEFAULT 0,
    pass_first_downs_pct numeric(4,1) NOT NULL DEFAULT 0.0,
    pass_intended_air_yds smallint NOT NULL DEFAULT 0,
    avg_pass_intended_air_yds numeric(3,1) NOT NULL DEFAULT 0.0,
    pass_air_yds smallint NOT NULL DEFAULT 0,
    avg_pass_air_yds_comp numeric(3,1) NOT NULL DEFAULT 0.0,
    avg_pass_air_yds_att numeric(3,1) NOT NULL DEFAULT 0.0,
    pass_yac smallint NOT NULL DEFAULT 0,
    avg_pass_yac_comp numeric(3,1) NOT NULL DEFAULT 0.0,
    pass_drops smallint NOT NULL DEFAULT 0,
    pass_drop_pct numeric(4,1) NOT NULL DEFAULT 0.0,
    poor_throws smallint NOT NULL DEFAULT 0,
    poor_throw_pct numeric(4,1) NOT NULL DEFAULT 0.0,
    passes_blitzed smallint NOT NULL DEFAULT 0,
    passes_hurried smallint NOT NULL DEFAULT 0,
    passes_hits smallint NOT NULL DEFAULT 0,
    passes_pressured smallint NOT NULL DEFAULT 0,
    pass_pressured_pct numeric(4,1) NOT NULL DEFAULT 0.0,
    scrambles smallint NOT NULL DEFAULT 0,
    avg_scramble_yds numeric(3,1) NOT NULL DEFAULT 0.0,
    rush_first_down smallint NOT NULL DEFAULT 0,
    rush_ybc smallint NOT NULL DEFAULT 0,
    avg_rush_ybc numeric(3,1) NOT NULL DEFAULT 0,
    rush_yac smallint NOT NULL DEFAULT 0,
    avg_rush_yac numeric(3,1) NOT NULL DEFAULT 0,
    rush_broken_tackles smallint NOT NULL DEFAULT 0,
    avg_rush_broken_tackles numeric(3,1) NOT NULL DEFAULT 0.0,
    rec_first_down smallint NOT NULL DEFAULT 0,
    rec_air_yds smallint NOT NULL DEFAULT 0,
    avg_rec_air_yds numeric(3,1) NOT NULL DEFAULT 0,
    rec_yac smallint NOT NULL DEFAULT 0,
    avg_rec_yac numeric(3,1) NOT NULL DEFAULT 0.0,
    rec_adot numeric(3,1) NOT NULL DEFAULT 0.0,
    rec_broken_tackles smallint NOT NULL DEFAULT 0,
    avg_rec_broken_tackles numeric(3,1) NOT NULL DEFAULT 0,
    rec_drops smallint NOT NULL DEFAULT 0,
    rec_drop_pct numeric(4,1) NOT NULL DEFAULT 0.0,
    rec_target_int smallint NOT NULL DEFAULT 0,
    rec_pass_rating numeric(4,1) NOT NULL DEFAULT 0.0,
    def_targets smallint NOT NULL DEFAULT 0,
    def_comps smallint NOT NULL DEFAULT 0,
    def_comp_pct numeric(4,1) NOT NULL DEFAULT 0.0,
    def_comp_yds smallint NOT NULL DEFAULT 0,
    avg_def_yds_comp numeric(3,1) NOT NULL DEFAULT 0.0,
    avg_def_yds_tgt numeric(3,1) NOT NULL DEFAULT 0.0,
    def_comp_tds smallint NOT NULL DEFAULT 0,
    def_pass_rating numeric(4,1) NOT NULL DEFAULT 0.0,
    avg_def_tgt_yds numeric(3,1) NOT NULL DEFAULT 0.0,
    def_air_yds smallint NOT NULL DEFAULT 0,
    def_yac smallint NOT NULL DEFAULT 0,
    def_blitzes smallint NOT NULL DEFAULT 0,
    def_qb_hurries smallint NOT NULL DEFAULT 0,
    def_qb_knockdowns smallint NOT NULL DEFAULT 0,
    def_qb_pressures smallint NOT NULL DEFAULT 0,
    def_missed_tack smallint NOT NULL DEFAULT 0,
    def_missed_tack_pct numeric(4,1) NOT NULL DEFAULT 0.0,
    is_starter boolean NOT NULL,
    starting_pos character varying(5),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS nfl.game_weather
(
    id serial NOT NULL,
    temp integer NOT NULL,
    humidity double precision NOT NULL,
    wind integer NOT NULL,
    game_id character varying(14) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS nfl.scoring_play
(
    id serial NOT NULL,
	home_score smallint NOT NULL,
	scoring_team_id integer NOT NULL,
	away_score smallint NOT NULL,
    qtr smallint NOT NULL,
    qtr_time_rem time without time zone NOT NULL,
    description text NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS nfl.play_by_play
(
    id bigserial NOT NULL,
    qtr character varying(2),
    qtr_time_rem time without time zone,
    down smallint,
    yds_to_go smallint,
    yd_start character varying(6),
    score_away smallint,
    score_home smallint,
    detail text NOT NULL,
    exp_pts_before numeric(3,1),
    exp_pts_after numeric(3,1),
    seq smallint NOT NULL,
    game_id character varying(14) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS nfl.player_gm_snap
(
    id serial NOT NULL,
	player_game_id integer NOT NULL,
    start_pos character varying(5) NOT NULL,
    off_snaps smallint NOT NULL DEFAULT 0,
    off_snap_pct numeric(4,1) NOT NULL DEFAULT 0.0,
    def_snaps smallint NOT NULL DEFAULT 0,
    def_snap_pct numeric(4,1) NOT NULL DEFAULT 0.0,
    st_snaps smallint NOT NULL DEFAULT 0,
    st_snap_pct numeric(4,1) NOT NULL DEFAULT 0.0,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS nfl.tm_gm_drive
(
    id serial NOT NULL,
    drive_num smallint NOT NULL DEFAULT 0,
    quarter smallint NOT NULL DEFAULT 0,
    time_start time without time zone NOT NULL,
    yd_start character varying(6) NOT NULL,
    num_plays smallint NOT NULL DEFAULT 0,
    drive_time time without time zone NOT NULL,
    net_yds smallint NOT NULL DEFAULT 0,
    drive_result character varying(20) NOT NULL,
    tm_gm_id integer NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS nfl.game
    ADD CONSTRAINT held_in FOREIGN KEY (stadium_id)
    REFERENCES nfl.stadium (name) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS nfl.official_game
    ADD CONSTRAINT official_id FOREIGN KEY (official_id)
    REFERENCES nfl.official (name) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS nfl.official_game
    ADD CONSTRAINT game_id FOREIGN KEY (game_id)
    REFERENCES nfl.game (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS nfl.team_game
    ADD CONSTRAINT team_id FOREIGN KEY (team_id)
    REFERENCES nfl.team (name) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS nfl.team_game
    ADD CONSTRAINT game_id FOREIGN KEY (game_id)
    REFERENCES nfl.game (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS nfl.player_game
    ADD CONSTRAINT player_in FOREIGN KEY (player_id)
    REFERENCES nfl.player (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS nfl.player_game
    ADD CONSTRAINT played_for FOREIGN KEY (tm_game_id)
    REFERENCES nfl.team_game (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS nfl.game_weather
    ADD CONSTRAINT weather_for FOREIGN KEY (game_id)
    REFERENCES nfl.game (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS nfl.scoring_play
    ADD CONSTRAINT scoring_team FOREIGN KEY (scoring_team_id)
    REFERENCES nfl.team_game (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS nfl.play_by_play
    ADD CONSTRAINT occurred_in FOREIGN KEY (game_id)
    REFERENCES nfl.game (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.player_gm_snap
    ADD CONSTRAINT snaps_in_game FOREIGN KEY (player_game_id)
    REFERENCES nfl.player_game (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.tm_gm_drive
    ADD CONSTRAINT drives_in_game FOREIGN KEY (tm_gm_id)
    REFERENCES nfl.team_game (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;

END;