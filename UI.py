import streamlit as st
import pandas as pd
from Navie_Bayes import load_data, preprocess_data, result_probability

# Load Data
history_df_full, recommend_df_full = load_data()

# Tiền xử lý
attributes, data, recommend_list = preprocess_data(history_df_full, recommend_df_full)

recommend_movie_names = recommend_df_full["Movie Name"]
recommend_directors = recommend_df_full["Director"]

# Streamlit UI
st.title("🎬 Movie Recommendation App")

# Hiển thị Lịch sử xem
st.header("📚 Lịch sử xem phim")
st.dataframe(history_df_full)

# Hiển thị danh sách phim chờ gợi ý
st.header("🎞️ Danh sách phim chờ gợi ý")
st.dataframe(recommend_df_full)

# Dự đoán cho các mẫu
st.header("🔍 Kết quả dự đoán")
recommendations = []

for idx, sample in enumerate(recommend_list):
    result = result_probability(sample, data, attributes)

    st.subheader(f"🎯 Phim {idx + 1}: {recommend_movie_names.iloc[idx]}")
    st.write(f"**Đạo diễn:** {recommend_directors.iloc[idx]}")
    st.write(f"**Chi tiết:** {sample}")
    st.write(f"✔️ Xác suất Yes: {result['Yes']}")
    st.write(f"❌ Xác suất No: {result['No']}")
    st.write(f"➡️ **Dự đoán:** {result['Recommend']}")
    st.markdown("---")

    if result['Recommend'] == "Yes":
        recommendations.append({
            "Movie Name": recommend_movie_names.iloc[idx],
            "Director": recommend_directors.iloc[idx],
            "Details": sample
        })

# Hiển thị danh sách phim được gợi ý
st.header("✅ Danh sách phim được gợi ý")

if not recommendations:
    st.write("Không có bộ phim nào được gợi ý!")
else:
    for idx, movie in enumerate(recommendations, 1):
        st.write(f"{idx}. {movie['Movie Name']} - Directed by {movie['Director']}")
        st.write(f"   Details: {movie['Details']}")

# Nút tải xuống
if recommendations:
    recommend_df_download = pd.DataFrame(recommendations)
    csv = recommend_df_download.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Tải danh sách gợi ý dưới dạng CSV",
        data=csv,
        file_name='recommendations.csv',
        mime='text/csv',
    )
