To run the analysis, first setup the repo.

```
mkvirtualenv -p `which python3` ahca
pip install -r requirements.txt
```

Then, use the process script to do everything:

```
bash process.sh
```

Your output files will be in `data/output`.