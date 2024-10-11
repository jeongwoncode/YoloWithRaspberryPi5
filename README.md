# YoloWithRaspberryPi5

## modify .pt file
yolo_motor_test5.py (line 91)

weight_files = list(model_dir.glob('best*.pt')) # modify this

## git push
```
git add .

git commit -m "commit message"

git push origin main
```

## git pull
```
git branch --set-upstream-to=origin/main main

git pull
```