import pandas as pd
 
# Đọc dữ liệu từ file CSV và bỏ cột "Movie Name" nếu có
df = pd.read_csv('movies_data_50.csv')
recommend_df = pd.read_csv('recommend_movie.csv')
 
# Loại bỏ cột "Movie Name"
if "Movie Name" in df.columns:
    df = df.drop(columns=["Movie Name"])
if "Movie Name" in recommend_df.columns:
    recommend_df = recommend_df.drop(columns=["Movie Name"])
#Loại bỏ cột "Director"
if "Director" in df.columns:
    df = df.drop(columns=["Director"])
if "MDirector" in recommend_df.columns:
    recommend_df = recommend_df.drop(columns=["Director"])
attributes = list(df.columns)
data = df.values.tolist()
recommend_list = recommend_df.values.tolist()
 
# Tính số lượng yes/no
def check_data(data):
    arr_yes = []
    arr_no = []
    for row in data:
        if row[-1] == "Yes":
            arr_yes.append(row)
        else:
            arr_no.append(row)
    return arr_yes, arr_no
   
# Tính các thành phần rời rạc trong nhãn
def get_possible_value(data, index):
    arr = []
    for row in data:
        if row[index] not in arr:
            arr.append(row[index])
    return arr
   
# Tính số lượng yes/no (P(nhãn|yes/no))
def caculator_probability(data, subnet_data, index, value):
    count = 0
    for row in subnet_data:
        if row[index] == value:
            count += 1
    result = count / len(subnet_data)
    number = get_possible_value(data, index)
    if result == 0:
        k = len(number)
        new_result = (count + 2) / (len(subnet_data) + k)
        return new_result
    return result
 
# Tính xác suất và đưa ra kết quả
def result_probability(sample, data, attribute):
    a, b = check_data(data)
    probability_yes = len(a) / len(data)
    probability_no = len(b) / len(data)
   
    for i in range(len(attribute) - 1):
        probability_yes *= caculator_probability(data, a, i, sample[i])
        probability_no *= caculator_probability(data, b, i, sample[i])
   
    recommend_class = "Yes" if probability_yes > probability_no else "No"
   
    return {
        "Yes": probability_yes,
        "No": probability_no,
        "Recommend": recommend_class
    }
 
# Dự đoán cho tất cả các mẫu trong recommend_movie.csv
print("=== Kết quả dự đoán ===")
recommendations = []  # Danh sách phim được gợi ý
for idx, sample in enumerate(recommend_list):
    result = result_probability(sample, data, attributes)
    print(f"Sample {idx + 1}: {sample}")
    print(f"  -> Probability Yes: {result['Yes']}")  # Hiển thị 10 chữ số thập phân
    print(f"  -> Probability No: {result['No']}")
    print(f"  -> Predicted Class: {result['Recommend']}")
    print("-" * 40)
 
    # Nếu được gợi ý (Yes) thì thêm vào danh sách
    if result['Recommend'] == "Yes":
        recommendations.append(sample)
 
# Hiển thị danh sách phim được gợi ý
def display_recommendations(recommendations):
    if not recommendations:
        print("\nKhông có bộ phim nào được gợi ý!")
    else:
        print("\n=== Danh sách phim được gợi ý ===")
        for idx, movie in enumerate(recommendations, 1):
            print(f"{idx}. {movie}")
 
# Gọi hàm để hiển thị danh sách phim gợi ý
display_recommendations(recommendations)
