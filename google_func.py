import googlemaps


latlngs = [(22.953177, 121.129813), (23.002835, 120.203139), (24.940991, 121.241919), (24.151393, 120.632390),
           (24.948036, 121.202812), (22.547708, 120.566461), (24.672270, 121.756171), (25.118782, 121.568831)]


def search_area(latlng):
    area = {"宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣", "臺北市", "新北市", "桃園市", "臺中市", "臺南市",
            "高雄市", "基隆市", "新竹縣", "新竹市", "苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣", "嘉義市", "屏東縣"}
    map_dict = {'台北市': "臺北市", '台南市': "臺南市", '台東縣': "臺東縣", '台中市': "臺中市"}
    area_simple = {'台北市', '台南市', '台東縣', '台中市'}
    gmaps = googlemaps.Client(key='AIzaSyBB3nC8IGf6s8em6z7AUmgAQ9ubDyzdB_I')
    reverse_geocode_result = gmaps.reverse_geocode(
        latlng=latlng, language='zh-tw')
    set_data = set()
    for el in reverse_geocode_result:
        for conponent in el['address_components']:
            # print(conponent['long_name'])
            if 'administrative_area_level_1' in conponent['types']:
                set_data.add(conponent['long_name'])
            if 'administrative_area_level_2' in conponent['types']:
                set_data.add(conponent['long_name'])
            if 'administrative_area_level_3' in conponent['types']:
                set_data.add(conponent['long_name'])
    if len(area & set_data) == 0:
        return map_dict[list(area_simple & set_data)[0]]
    elif len(area & set_data) == 0:
        return None
    else:
        return list(area & set_data)[0]


# for i in range(0, len(latlngs)):
#     result = search_area(latlngs[i])
#     print(result)
