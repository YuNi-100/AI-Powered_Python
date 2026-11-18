# AI-Powered Python 자동 팩트체킹

5차 과제에서 Python으로 데이터의 사실을 추출하고, 수업 RAG 챗봇의 답변을 근거 ID와 대조했다. 문제 1은 Billboard Hot 100과 Spotify 음악 특성 데이터를, 문제 2는 Olist 주문·리뷰 자료를 사용했다.

## 파일 구성

| 파일 | 내용 |
| --- | --- |
| [music_analysis.ipynb](music_analysis.ipynb) | Google Colab용 분석 노트북과 저장된 실행 결과 |
| [music_analysis.py](music_analysis.py) | 같은 분석을 로컬에서 실행하는 Python 스크립트 |
| [fact_table.csv](fact_table.csv) | 문제 1에서 만든 사실표 F-1~F-3 |
| [답안과_실행안내.txt](답안과_실행안내.txt) | 드라이브에 보관한 초안과 실행 안내. 문제 2의 음악 데이터 질문은 초안에 적은 예시다. |

## 문제 1 · 음악 데이터에서 사실 추출

| 사실 ID | 결과 | 집계 기준 |
| --- | --- | --- |
| F-1 | **32,503행 × 33열** | 제목 행 제외, 중복 포함. 고유 `song_id`는 32,366개 |
| F-2 | **평균 차트 진입 주 수 11.57주** | `weeks_on_chart` 결측 3행을 제외한 32,500행. 합계 376,058주 ÷ 32,500행 |
| F-3 | **장르 결측 1,600행** | 원본 전체의 `spotify_genre` 열 |

전체 결측 셀은 104,916개다. 이 CSV에는 스트리밍 횟수 열이 없다. `spotify_track_popularity`는 인기도 지표다.

### Colab에서 실행

1. [Colab에서 노트북 열기](https://colab.research.google.com/github/YuNi-100/AI-Powered_Python/blob/main/music_analysis.ipynb)를 선택한다.
2. 첫 코드 셀을 실행하고 `billboard_hot_100_spotify_audio_features_enriched.csv`를 업로드한다. 과제에 사용한 원본은 내 드라이브의 `Colab Notebooks/5차과제` 폴더에 있다. 원본은 출처 페이지와 재배포 조건을 확인한 뒤 별도로 공유할 수 있다.
3. 나머지 셀을 순서대로 실행한다. 마지막 셀은 `fact_table.csv`를 생성한다.

### 로컬에서 실행

원본 CSV를 스크립트와 같은 폴더에 놓고, 그 폴더에서 실행한다.

```sh
python -m pip install pandas
python music_analysis.py
```

## 문제 2 · Olist 챗봇 답변 검증

수업 RAG 챗봇에서 **채널 C**를 사용했다. 채널 C는 Olist 사실표, 모델 설명서, 판매자 규정집을 참조한다. 답변에 사용한 근거 ID를 붙이고, 자료에서 확인할 수 없는 질문에는 확인 불가라고 답하도록 했다.

| 실제 질문 | 확인 결과 | 근거 ID |
| --- | --- | --- |
| 늦게 도착한 주문의 리뷰 점수는? | 평균 **2.57점** | F14 |
| 두 번 이상 구매한 고객의 비율은 몇 %야? | **3.0%** | F07 |
| 배송이 빠르면 고객이 평점을 남길까? | 배송 속도와 평점 **작성 여부**의 직접 관계는 확인할 수 없음 | F11, F17 |
| 저평점 위험 판매자는 어떤 조치를 받아? | 14일 안에 출고 기한 준수 계획서를 제출하고, 다음 분기에도 해당 등급이면 신규 상품 등록이 제한됨 | R13 (조치), F29 (판매자 특성) |

근거 ID가 붙어 있어도 해당 자료가 질문에 직접 답하는지 확인했다. 예를 들어 배송 기간과 리뷰 점수에 관한 자료만으로 평점 작성 여부를 판단할 수는 없다.
