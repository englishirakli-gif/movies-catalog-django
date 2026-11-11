# movies-catalog-django

ფილმების კატალოგი Django-ზე. დავალება model-ებზე, migration-ებსა და admin-ზე.

## Model-ები

- **Movie**: სათაური, slug, აღწერა, გამოშვების წელი, ხანგრძლივობა, ასაკობრივი რეიტინგი, ბიუჯეტი, ენა, პოსტერი
- **Genre**: ჟანრი
- **Director**: რეჟისორი
- **Festival**: კინოფესტივალი

მთავარი გვერდი გადამისამართებს admin-ზე. კითხვებზე პასუხები: [movies/ANSWERS.md](movies/ANSWERS.md)

## გაშვება

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

README დავამატე, რომ GitHub-ზე პროექტის გახსნისას მაშინვე ჩანდეს, რას აკეთებს და როგორ გაეშვას.
