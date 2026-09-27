# SmartRoute AI — Final Submission Checklist

## Code
- [ ] `app.py` runs without errors
- [ ] `model/smartroute_pipeline.pkl` is the **77-intent official model**
- [ ] `requirements.txt` is present
- [ ] `train_model.py` is present
- [ ] EDA notebook/script is present

## Data
- [ ] `banking77_train.csv` retained locally
- [ ] `banking77_test.csv` retained locally
- [ ] Dataset source and license credited
- [ ] No personal/private customer data included

## Demo
- [ ] Query prediction works
- [ ] Confidence is displayed
- [ ] Top predictions display
- [ ] Routing decision changes with confidence
- [ ] Service queue is displayed
- [ ] History updates after every prediction
- [ ] Analytics counters update
- [ ] Clear History works

## Documentation
- [ ] Technical paper included
- [ ] Presentation included
- [ ] README included
- [ ] EDA outputs included if available
- [ ] Classification report included if available
- [ ] Confusion matrix included if available

## Final verification
Run:

```powershell
python app.py
```

Open `http://127.0.0.1:5000` and test at least these examples:

- `My card payment was charged twice`
- `I forgot my passcode`
- `How long will my transfer take?`
- `My refund has not arrived`

Then scroll to Routing Analytics and confirm that history and counters update.
