# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
from zhejiang import ZJ
from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "http://127.0.0.1:8000/assets/"
if __name__ == '__main__':
    # 基于Map构建浙江地图
    # ZJ.zhejiang_map()
    # 生成浙江省所有城市地图
    # ZJ.zhangjiang_cities_map()
    # 加载data.xlsx中的数据
    # ZJ.load_data("data.xlsx")
    # 构建浙江全省地图，并将数据渲染到地图中
    # ZJ.zhejiang_map_all()
    ZJ.zhejiang_sync_data("data.xlsx")
