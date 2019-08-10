
def check_input(input_str):

    origin_data = ['宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣', '臺北市', '新北市', '桃園市', '臺中市',
                   '臺南市', '高雄市', '基隆市', '新竹縣', '新竹市', '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣', '嘉義市', '屏東縣']

    check_list = [[] for i in range(len(origin_data))]

    for (index, word) in enumerate(origin_data):
        for i in input_str:
            try:
                if i == '台':
                    check_list[index].append('臺')
                check_list[index].append(word.index(i))
            except:
                pass
    ls_a = [len(c) for c in check_list]
    index_list = []
    for index, n in enumerate(ls_a):
        if n == max(ls_a):
            index_list.append(index)

    return [el for index, el in enumerate(origin_data) if index in index_list]
