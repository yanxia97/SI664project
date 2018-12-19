# SI664project
## What to do in this project is to build a database about artworks. I will build a many-to-many relationship between artwoks and subjects.
## The data are available on [GitHub](https://github.com/tategallery/collection), consist of artists and artworks in forms of CSV and JSON files. The unit of width, height and depth in the artwork table is "mm".
## There are two subtle problems in the data in the db.
### The artist may share the same name. Therefore, I cannot figure out the exact artist of a work given the duplicate artist names. It can be further improved by linking to an attribute "artistId" in the dataset. 
### Also, due to some missing subjects in the processed files given, some related artwork subjects cannot be shown and thrown away.
## This is the screenshot of my model. ![model picture](/static/img/model.png)