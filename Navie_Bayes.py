import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv('movies_data_50.csv')
recommend_df = pd.read_csv('recommend_movie.csv')
attributes = list(df.columns)
data = df.values.tolist()
recommend_list = recommend_df.values.tolist()

# 1. Phân loại dữ liệu thành hai nhóm Yes và No
def split_data_by_label(data):
    yes_data = [row for row in data if row[-1] == "Yes"]
    no_data = [row for row in data if row[-1] == "No"]
    return yes_data, no_data

# 2. Lấy các giá trị duy nhất của một thuộc tính
def get_unique_values(data, index):
    return list(set(row[index] for row in data))

# 3. Tính xác suất có điều kiện P(value|Yes) hoặc P(value|No)
def calculate_conditional_probability(data, subset_data, index, value):
    count = sum(1 for row in subset_data if row[index] == value)
    total = len(subset_data)
    unique_values = get_unique_values(data, index)
    
    # Áp dụng Laplace Smoothing nếu xác suất bằng 0
    if count == 0:
        k = len(unique_values)
        return (count + 1) / (total + k)
    else:
        return count / total

# 4. Tính xác suất tổng quát và dự đoán nhãn
def predict_label(sample, data, attributes):
    yes_data, no_data = split_data_by_label(data)
    prob_yes = len(yes_data) / len(data)
    prob_no = len(no_data) / len(data)

    # Tính xác suất cho từng thuộc tính trong mẫu
    for i in range(len(attributes) - 1):
        prob_yes *= calculate_conditional_probability(data, yes_data, i, sample[i])
        prob_no *= calculate_conditional_probability(data, no_data, i, sample[i])

    # Kết luận dựa trên xác suất cao hơn
    prediction = "Yes" if prob_yes > prob_no else "No"
    return {
        "Yes": prob_yes,
        "No": prob_no,
        "Recommend": prediction
    }

# 5. Dự đoán cho tất cả các mẫu trong recommend_movie.csv
print("=== Kết quả dự đoán ===")
recommendations = []  # Danh sách phim được gợi ý
for idx, sample in enumerate(recommend_list):
    result = predict_label(sample, data, attributes)
    print(f"Sample {idx + 1}: {sample}")
    print(f"  -> Probability Yes: {result['Yes']:.4f}")
    print(f"  -> Probability No: {result['No']:.4f}")
    print(f"  -> Predicted Class: {result['Recommend']}")
    print("-" * 40)

    # Nếu được gợi ý (Yes) thì thêm vào danh sách
    if result['Recommend'] == "Yes":
        recommendations.append(sample)

# 6. Hiển thị danh sách phim được gợi ý
def display_recommendations(recommendations):
    if not recommendations:
        print("\nKhông có bộ phim nào được gợi ý!")
    else:
        print("\n=== Danh sách phim được gợi ý ===")
        for idx, movie in enumerate(recommendations, 1):
            print(f"{idx}. {movie}")

# Gọi hàm để hiển thị danh sách phim gợi ý
display_recommendations(recommendations)
