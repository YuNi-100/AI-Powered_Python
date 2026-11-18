import pandas as pd
from pathlib import Path

filename = "billboard_hot_100_spotify_audio_features_enriched.csv"
if not Path(filename).exists():
    try:
        from google.colab import files
        print("함께 받은 CSV 파일을 선택해 주세요.")
        files.upload()
    except ImportError:
        raise FileNotFoundError("노트북과 CSV를 같은 폴더에 넣어 주세요.")

df = pd.read_csv(filename, encoding="utf-8-sig")
df = df.replace(r"^\s*$", pd.NA, regex=True)
print("데이터 불러오기 완료")
print("원본 행을 삭제하지 않고 분석합니다.")


print(f"① 데이터 크기: {df.shape[0]:,}행 × {df.shape[1]}열 (제목 행 제외)")
missing = df.isna().sum()
print("\n② 열별 결측치")
print(missing.to_string())
print(f"\n전체 결측 셀: {missing.sum():,}개")
print(f"결측치가 있는 행: {df.isna().any(axis=1).sum():,}행")
print(f"완전히 동일한 중복 행: {df.duplicated().sum():,}행")
print(f"song_id 고유값: {df['song_id'].nunique():,}개")
print("\n스트리밍 횟수 열: 없음")
print("spotify_track_popularity를 스트리밍 횟수로 사용하지 않습니다.")


weeks = pd.to_numeric(df["weeks_on_chart"], errors="coerce")
invalid = df["weeks_on_chart"].notna() & weeks.isna()
print("③ 계산: 평균 차트 진입 주 수")
print(f"계산 대상: {weeks.notna().sum():,}행")
print(f"제외한 결측치: {df['weeks_on_chart'].isna().sum():,}행")
print(f"추가 숫자 변환 오류: {invalid.sum():,}행")
print(f"차트 진입 주 수 합계: {weeks.sum():,.0f}주")
print(f"평균 = 합계 ÷ 유효 행 수 = {weeks.mean():.2f}주")
print("중복 행을 포함한 원본 레코드 기준이며, 고유 곡별 평균은 아닙니다.")


facts = pd.DataFrame([
    ["F-1", "분석 파일의 데이터 레코드는 32,503행이다.", f"{len(df):,}행", "첨부 CSV 전체, 제목 행 제외, 중복 포함"],
    ["F-2", "차트 진입 주 수의 평균은 약 11.57주이다.", f"{weeks.mean():.2f}주", f"weeks_on_chart 유효 {weeks.notna().sum():,}행, 결측 3행 제외, 중복 포함"],
    ["F-3", "Spotify 장르 정보가 비어 있는 레코드는 1,600행이다.", f"{df['spotify_genre'].isna().sum():,}행", "첨부 CSV 전체, spotify_genre 결측치"],
], columns=["사실ID", "내용", "숫자", "기준(대상·기간·단위)"])
print("④ 사실표")
for _, r in facts.iterrows():
    print(f"\n{r['사실ID']}: {r['내용']}\n숫자: {r['숫자']}\n기준: {r['기준(대상·기간·단위)']}")
facts.to_csv("fact_table.csv", index=False, encoding="utf-8-sig")
