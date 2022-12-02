create table if not exists playlist
(
    id              uuid not null
        constraint playlist_pk
            primary key,
    name            text not null,
    description     text,
    organisation_id text not null
);

