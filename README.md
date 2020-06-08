# Pixel-A
텐서플로우 활용기초 - 조별과제 2조 코드입니다.(Pixel-A)

'cloud', 'sun', 'pants', 'umbrella', 'table', 'ladder', 'eyeglasses', 'clock', 'scissors', 'cup','apple','pizza','eye','frog','flower','hand','foot','donut','elephant','bicycle','candle','chair','face','fish','tree'을 인식 가능합니다.

## files

* script/hand-quickdraw.py
  - 손그림 인식 프로그램  
* script/quickdrawmodel.h5
  - 손그림 인식 모델
* script/QuickDraw.ipynb
  - 손그림 인식 학습 code


### script/QuickDraw.ipynb
> https://colab.research.google.com/ 을 통해 열어주세요

### script/hand-quickdraw.py
손그림 인식 프로그램입니다.
실행 후 모델을 가져와서 손 그림을 맞출 수 있습니다.

1. 패키지 설치

```pip install -r requirements.txt```

2. 모델 불러오기

3. 실행

```python script/hand-quickdraw.py```

![Alt sample](/img/sample.PNG)



