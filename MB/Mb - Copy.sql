SELECT
 artist.Id as "ArtId"
,artist.name as "Art"
,artist.begin_date_year as "ArtBegYear"
,area.name as "ArtCountry"
,artist.type as "ArtTypeId"
,artist_type.Name as "ArtTypeName"

,artist_credit_name.artist_credit as "ArtCredNameId"
,artist_credit_name.Name as "ArtCredNameName"
,artist_credit.Name as "ArtCredName"
,artist_credit.artist_count as "ArtCredArtCount"

,release_group.Id as "AlbumGroupId"
,release_group.Name as "AlbumGroupName"
,release_group.artist_credit as "AlbumGroupArtCred"
,release_group_primary_type.name as "AlbumGroupPrimTypeName"
,release_group_meta.first_release_date_year as "AlbumGroupFirstYear"

,release.id as "AlbumId"
,release.Name as "AlbumName"
,release.Quality as "AlbumDQ"
,release_country.date_year as "AlbumYear"
,area2.Name as "AlbumCountry"
,language.Name as "AlbumLang"
,script.Name as "AlbumScrip"

,medium.Id as "MediuId"
,medium.Name as "MediuName"
,medium.track_count as "MediuTracks"
,medium_format.Name as "MediuFmtName"
,medium_format.Year as "MediuFmtYear"

,track.Id as "TrackId"
,track.Position as "TrackPos"
,track.Number as "TrackNo"
,track.Name as "TrackName"
,track.length as "TrackLen"

from artist

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

inner join 
(select release_group.Id,artist.id as ArtId,min(release.id) as Min_release_id
 from artist
 inner join artist_credit_name ON artist_credit_name.artist = artist.id
 inner join artist_credit ON artist_credit.id = artist_credit_name.artist_credit
 inner join release_group ON release_group.artist_credit = artist_credit.id
 inner join release on release.release_group = release_group.id
 group by release_group.Id,artist.id
) as test on test.Min_release_id=release.id and test.artId=artist.id

where 
lower(track.Name) = 'chuva de prata'
--artist.name = 'U2'
--and release_country.date_year=release_group_meta.first_release_date_year
and area2.Name in ('Brazil','United States')
and script.Name='Latin';





