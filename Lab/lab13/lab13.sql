.read data.sql


CREATE TABLE bluedog AS
  SELECT color, pet FROM students WHERE color = "blue" AND pet = "dog";

CREATE TABLE bluedog_songs AS
  SELECT color, pet, song FROM students WHERE color = "blue" AND pet = "dog";


CREATE TABLE matchmaker AS
  SELECT a.pet, a.song, a.color, b.color 
    FROM students AS a, students AS b
        WHERE a.pet = b.pet
        AND a.song = b.song
        AND a.time < b.time;


CREATE TABLE sevens AS
  SELECT a.seven FROM students as a, numbers as b
    WHERE a.time = b.time
    AND a.number = 7
    AND b."7" = "True";


CREATE TABLE favpets AS
  SELECT pet, COUNT(*) FROM students
    GROUP BY pet ORDER BY -COUNT(*) LIMIT 10; -- 默认从小到大


CREATE TABLE dog AS
  SELECT pet, COUNT(*) FROM students
    WHERE pet = "dog";


CREATE TABLE bluedog_agg AS
  SELECT song, COUNT(*) FROM bluedog_songs
    GROUP BY song ORDER BY -COUNT(*);


CREATE TABLE instructor_obedience AS
  SELECT seven, instructor, COUNT(*) FROM students
    WHERE seven = "7" GROUP BY instructor;

