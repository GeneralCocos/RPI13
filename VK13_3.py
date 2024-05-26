import vk_api
import networkx as nx
import matplotlib.pyplot as plt

# Авторизация в API ВКонтакте
vk_session = vk_api.VkApi(
    token='vk1.a.ct-nUBTJA6TK9DL7N9g4eMEZP3ODwGg5w10KsFRcJ0VJDtqRkCnXIfM1UetK7Iped2FmaCM9piobEYoYyGDhPad9NSuGTPSJ5BIRe6C8qK6rwyCQZ-xLfUJGTw5QsJzA1lDzvZ-PgIsKHLnQpScliOkWgNcGAtAd-PQR757EsZMkZZVPEe4gy5dFRCu7RHKYFX4dTZ0VQuqEVHkN7st1gw')
vk = vk_session.get_api()


def get_friends_ids(user_id):
    friends = vk.friends.get(user_id=user_id)
    return friends['items']


def build_graph(user_ids):
    G = nx.Graph()

    for user_id in user_ids:
        friends_ids = get_friends_ids(user_id)
        for friend_id in friends_ids:
            G.add_edge(user_id, friend_id)

    return G


# Пример списка айди пользователей
user_ids = [483297221, 183716165, 122036099]

# Создание графа с друзьями пользователей
G = build_graph(user_ids)

# Визуализация графа
pos = nx.spring_layout(G)
plt.figure(figsize=(10, 10))
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500,
        edge_color='gray', font_size=10, font_color='black')
plt.title("Граф друзей в ВКонтакте")
plt.show()
