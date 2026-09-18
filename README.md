<li>Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.</li>
<li>Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan reseptejä.</li>
<li>Käyttäjä pystyy lisäämään kuvia reseptiin.</li>
<li>Käyttäjä näkee sovellukseen lisätyt reseptit.</li>
<li>Käyttäjä pystyy etsimään reseptejä hakusanalla.</li>
<li>Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät reseptit.</li>
<li>Käyttäjä pystyy valitsemaan reseptille  yhden tai useamman luokittelun (esim. reseptin tyyppi, ruoka-aine, kokkausaika).</li>
<li>Käyttäjä pystyy kommentoimaan palvelussa olevia reseptejä.</li>

<h1>Sovelluksen asentaminen:</h1>

Luo virtuaaliympäristö sovelluksen pyörittämiseen

<code>$ python3 -m venv venv</code>

Käynnistä virtuaaliympäristö komennolla

<code>$ source venv/bin/activate</code>

Asenna flask -kirjasto virtuaaliympäristössä

<code>$ pip install flask</code>

Luo taulut tietokantaan komennolla

<code>$ sqlite3 database.db < schema.sql</code>

Käynnistä ohjelma komennolla ja seuraa komentotulkin ohjeita

<code>$ flask run</code>

