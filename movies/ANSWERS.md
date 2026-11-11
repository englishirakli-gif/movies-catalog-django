# ANSWERS

## ნაწილი 1: თეორია

**1. `null=True` და `blank=True`**
`null=True` ბაზას ეხება: სვეტში შეიძლება NULL ჩაიწეროს. `blank=True` ვალიდაციას ეხება: ფორმაში (მაგ. admin-ში) ველი შეიძლება ცარიელი დარჩეს.
`TextField`-ისთვის მხოლოდ `blank=True`-ს ვიყენებ. ცარიელი ტექსტი ინახება როგორც `""`, ასე რომ ორი სხვადასხვა „ცარიელი“ (`""` და NULL) არ გვექნება.
`birth_year` რიცხვია, რიცხვს `""` ვერ ექნება, ამიტომ მას ორივე სჭირდება.

**2. `DecimalField` vs `FloatField` ფულისთვის**
`FloatField` ორობით მცოცავ წერტილს იყენებს და ზოგ რიცხვს ზუსტად ვერ ინახავს (მაგ. `0.1 + 0.2 = 0.30000000000000004`).
`DecimalField` ზუსტ ათობით რიცხვს ინახავს, ამიტომ ფულზე თეთრები არ იკარგება.

**3. რატომ არ ვწერთ `id`-ს?**
Django ავტომატურად ამატებს `id` ველს ყველა model-ს (`DEFAULT_AUTO_FIELD = BigAutoField` settings-ში).
ცხრილში ის ჩნდება როგორც `"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT` (ჩანს `sqlmigrate`-ში).

**4. `auto_now_add` vs `auto_now`**
`auto_now_add=True` თარიღს მხოლოდ ერთხელ წერს, ჩანაწერის შექმნისას. `auto_now=True` ყოველ `save()`-ზე ანახლებს.
„შექმნის თარიღისთვის“ `auto_now_add`, „ბოლო ცვლილებისთვის“ `auto_now`.

**5. `makemigrations` და `migrate`**
`makemigrations` model-ის ცვლილებებს უყურებს და migration ფაილს წერს (ბაზას არ ეხება). `migrate` ამ ფაილებს ბაზაზე უშვებს.
თუ model-ს შევცვლი და მხოლოდ `migrate`-ს გავუშვებ, არაფერი შეიცვლება („No migrations to apply“), რადგან ახალი migration ფაილი არ არსებობს. Django გაგვაფრთხილებს, რომ model-ში ცვლილებებია, რომლებიც migration-ში არ არის.

**6. `SlugField(unique=True)`, ერთნაირი slug**
მეორე ფილმს ვერ შევინახავთ: admin-ში გამოდის „Ფილმი with this Slug already exists.“, კოდიდან კი `IntegrityError`.
ბაზაში ეს წესი არის `UNIQUE` შეზღუდვა (index) სვეტზე `slug`.

**7. migration-ები git-ში, `db.sqlite3` არა**
migration-ები კოდის ნაწილია: მათით ყველა თავის კომპიუტერზე ერთნაირ ცხრილებს აწყობს.
`db.sqlite3` კი ჩემი ლოკალური მონაცემებია (პაროლებიც), ყველას თავისი აქვს და git-ში conflict-ებს გამოიწვევდა.

**8. `age_rating` და `TextChoices`**
ბაზაში ინახება მოკლე მნიშვნელობა (`"G"`, `"PG13"`), admin-ში კი ჩანს ლამაზი სახელი („ყველასთვის“, „13+“).

---

## ნაწილი 2: პრაქტიკა

### დავალება 1: `sqlmigrate movies 0001`
```sql
CREATE TABLE "movies_director" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "birth_year" integer NULL, "bio" text NOT NULL);
CREATE TABLE "movies_genre" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL UNIQUE);
```
- `UNIQUE` არის `movies_genre.name`-ზე.
- `NULL` (და არა `NOT NULL`) არის `birth_year`-ზე. `bio` არის `NOT NULL`, რადგან მას მხოლოდ `blank=True` აქვს.

### დავალება 2: სვეტების ტიპები `movies_movie`-ში
- `budget` → `decimal`
- `is_published` → `bool` (SQLite-ში რეალურად 0/1)
- `age_rating` → `varchar(4)` (ჩვეულებრივი ტექსტი, choices ბაზაში არ ჩანს)

### დავალება 3
შევიყვანე 4 ფილმი, 3 რეჟისორი და 3 ჟანრი. სია admin-ში: მონანიება, მიმინო, ნატვრის ხე, ფიროსმანი (ახლიდან ძველისკენ).
ფილტრი „ყველასთვის“ აჩვენებს მიმინოს და ფიროსმანს, ძებნა „მიმ“ პოულობს მიმინოს.

### დავალება 4: წესების შემოწმება
1. **slug `mimino` მეორედ:** შეცდომა „Ფილმი with this Slug already exists.“. მიზეზი: `slug`-ის `unique=True`.
2. **ჟანრი `დრამა` მეორედ:** შეცდომა „Genre with this Name already exists.“. მიზეზი: `name`-ის `unique=True`.
3. **ცარიელი `description` და `budget`:** შეინახა. მიზეზი: `description`-ს აქვს `blank=True`, `budget`-ს `null=True, blank=True`.
4. **ცარიელი `release_year`:** შეცდომა „This field is required.“. მიზეზი: `release_year`-ს არ აქვს `blank=True` (default-ად `blank=False`).

სატესტო ჩანაწერები წავშალე.

### დავალება 5: model-ის შეცვლა
1. `language` default-ის გარეშე → `makemigrations` გვეკითხება:
   ```
   It is impossible to add a non-nullable field 'language' to movie without specifying a default.
   This is because the database needs something to populate existing rows.
   Please select a fix:
    1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
    2) Quit and manually define a default value in models.py.
   ```
   ბაზაში უკვე 4 ფილმია და Django-მ არ იცის, რა ჩაწეროს მათ ახალ სვეტში.
2. ავირჩიე 2 (Quit), დავამატე `default="ქართული"`, შეიქმნა `0003_movie_language`. ოთხივე ფილმს აქვს `language = ქართული`.
3. `poster_url = URLField(blank=True)` → არაფერი უკითხავს. `blank=True` ტექსტურ ველზე ნიშნავს, რომ ცარიელი `""` სწორი მნიშვნელობაა, ამიტომ არსებულ ჩანაწერებს Django თავად უწერს `""`-ს.
4. `showmigrations movies`: ყველა `[X]`-ითაა (0001–0005).

### დავალება 6: shell
```
>>> Genre.objects.create(name="ანიმაცია")
<Genre: ანიმაცია>
>>> m
<Movie: სატესტო ფილმი (2026)>
>>> m.age_rating
Movie.AgeRating.G
>>> m.get_age_rating_display()
'ყველასთვის'
>>> Movie.objects.count()
5
```
`m.age_rating` არის ის, რაც ბაზაში ინახება, ანუ `"G"`. აქ `Movie.AgeRating.G` ჩანს, რადგან default-ად enum მივეცით, მაგრამ ის მაინც string `"G"`-ია.
`get_age_rating_display()` choices-დან ადამიანისთვის გასაგებ სახელს აბრუნებს. სატესტო ფილმი და ჟანრი წავშალე.

### ★ დავალება 7: Festival
- `website = abc` → „Enter a valid URL.“
- `contact_email = nino@` → „Enter a valid email address.“
- ბაზაში `website` არის `varchar(200)`, `contact_email` არის `varchar(254)`, ანუ ჩვეულებრივი ტექსტი.
  ვალიდაცია ბაზიდან კი არა, Django-დან მოდის: `URLField`-ს და `EmailField`-ს აქვთ validator-ები, რომლებსაც ფორმა (admin) ამოწმებს. `Festival.objects.create(...)` კოდიდან ვალიდაციას არ გაივლის, თუ `full_clean()`-ს არ გამოვიძახებთ.

### ★ დავალება 8: rollback
1. `language`-ს ამატებს `0003_movie_language`.
2. `migrate movies 0002` → უკან დაბრუნდა 0005, 0004 და 0003.
3. `movies_movie`-ში `language` (და `poster_url`) სვეტი წაიშალა, `movies_festival` ცხრილიც მთლიანად წაიშალა.
4. `migrate`-ით ისევ ბოლო მდგომარეობაში დავბრუნდი. `language` ისევ `ქართული`-ა (default-იდან), მაგრამ ფესტივალი, რომელიც ბაზაში იყო, დაიკარგა.

**რატომ არის rollback production-ში საშიში:** rollback სვეტებს და ცხრილებს შლის მათ მონაცემებთან ერთად, და ხელახალი `migrate` ამ მონაცემებს ვეღარ აბრუნებს.
