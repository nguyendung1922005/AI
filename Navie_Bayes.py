import pandas as pd

def load_data():
    history_df_full = pd.read_csv('data/History.csv')
    recommend_df_full = pd.read_csv('data/recommend_movie.csv')
    return history_df_full, recommend_df_full

import copy

def preprocess_data(df, recommend_df):
    df_proc = df.copy()
    recommend_df_proc = recommend_df.copy()

    # Drop các cột không cần thiết
    for col in ["Movie Name", "Director"]:
        if col in df_proc.columns:
            df_proc = df_proc.drop(columns=[col])
        if col in recommend_df_proc.columns:
            recommend_df_proc = recommend_df_proc.drop(columns=[col])

    # Hàm group_rating giống như bạn mô tả
    def group_rating(data, index):
        element = ['Low', 'Medium', 'High', 'Very High']
        data_new = copy.deepcopy(data)
        for row in data_new:
            if row[index] <= 6:
                row[index] = "Low"
            elif row[index] <= 7.5:
                row[index] = "Medium"
            elif row[index] <= 9:
                row[index] = "High"
            else:
                row[index] = "Very High"
        return data_new

    # Convert DataFrame sang list và group lại Rating
    attributes = list(df_proc.columns)
    data = df_proc.values.tolist()
    recommend_list = recommend_df_proc.values.tolist()

    # Thực hiện nhóm rating
    data = group_rating(data, attributes.index("Rating"))
    recommend_list = group_rating(recommend_list, attributes.index("Rating"))

    return attributes, data, recommend_list

def check_data(data):
    arr_yes, arr_no = [], []
    for row in data:
        (arr_yes if row[-1] == "Yes" else arr_no).append(row)
    return arr_yes, arr_no

def get_possible_value(data, index):
    return list(set(row[index] for row in data))

def caculator_probability(data, subnet_data, index, value):
    count = sum(1 for row in subnet_data if row[index] == value)
    result = count / len(subnet_data)
    number = get_possible_value(data, index)
    if result == 0:
        k = len(number)
        return (count + 2) / (len(subnet_data) + k)
    return result

def result_probability(sample, data, attribute):
    a, b = check_data(data)
    probability_yes = len(a) / len(data)
    probability_no = len(b) / len(data)

    for i in range(len(attribute) - 1):
        probability_yes *= caculator_probability(data, a, i, sample[i])
        probability_no *= caculator_probability(data, b, i, sample[i])

    recommend_class = "Yes" if probability_yes > probability_no else "No"
    return {"Yes": probability_yes, "No": probability_no, "Recommend": recommend_class}

