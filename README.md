# Alzheimers Glasses
Alex Conesa Dabizha

## System Functionality

### run.py

### capturePerson.py


## System configuration and execution

### How to install

```shell
pip install -r requirements.txt
```

### How to capture faces

Execute the command:

```shell
# It will ask for the name
python3 capturePerson.py
```

Variants (replace `alex` by the name of the person you want to save):

```shell
python3 capturePerson.py --name alex --no-voice --no-face
```

The faces captured will automatically be stored in the `faces` folder.
The voices generated will automatically be stored in `voices` foler.

### How to execute face recognition

```shell
python3 run.py
```

Point/look with the camera at the person wanted to be recognized.

