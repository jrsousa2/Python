SELECT
 artist.*
,area.*
,artist_type.*

,artist_credit_name.*
,artist_credit.*

,release_group.*
,release_group_primary_type.*
,release_group_meta.*

,release.*
,area2.Name as "AlbumCountry"
,language.Name as "AlbumLang"
,script.Name as "AlbumScrip"

,medium.*

,track.*

from artist
--inner join test on test.Nome = artist.Name

inner join artist_credit_name ON artist_credit_name.artist = artist.id

inner join artist_credit ON artist_credit.id = artist_credit_name.artist_credit

inner join release_group ON release_group.artist_credit = artist_credit.id

inner join release on release.release_group = release_group.id
left join release_country on release_country.release = release.id
left join area as area2 ON area2.id = release_country.country
left join language on language.id = release.language
left join script on script.id = release.script

inner join medium on medium.release = release.id

left join medium_format on medium_format.id = medium.id

inner join track on track.medium = medium.id

left join release_group_primary_type on release_group_primary_type.id = release_group.type

left join area ON artist.area = area.id

left join artist_type ON artist_type.id = artist.type

left join release_group_meta ON release_group_meta.id = release_group.id

where 
--track.name='Vapor barato'

artist.gid='382f1005-e9ab-4684-afd4-0bdae4ee37f2';

--area2.Name in ('Brazil','United States')
--and script.Name='Latin';
--artist.name = 'U2'
--and release_country.date_year=release_group_meta.first_release_date_year





