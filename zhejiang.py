import logging
import os.path
import random

from pyecharts import options as opts
from pyecharts.charts import Geo, Map


class ZJ:
    # zhejiang_city = ["杭州市", "宁波市", "温州市", "嘉兴市", "湖州市", "绍兴市", "金华市", "衢州市", "舟山市", "台州市", "丽水市"]
    hangzhou = ["滨江区", "淳安县", "富阳区", "拱墅区", "建德市", "临安区", "临平区", "钱塘区", "上城区", "桐庐县", "西湖区", "萧山区", "临平区"]
    ningbo = ["海曙区", "江北区", "北仑区", "镇海区", "鄞州区", "奉化区", "象山县", "宁海县", "余姚市", "慈溪市"]
    wenzhou = ["鹿城区", "龙湾区", "瓯海区", "洞头区", "永嘉县", "平阳县", "苍南县", "文成县", "泰顺县", "瑞安市", "乐清市", "龙港市"]
    jiaxing = ["南湖区", "秀洲区", "嘉善县", "海盐县", "海宁市", "平湖市", "桐乡市"]
    huzhou = ["吴兴区", "南浔区", "德清县", "长兴县", "安吉县"]
    shaoxing = ["越城区", "柯桥区", "上虞区", "新昌县", "诸暨市", "嵊州市"]
    jinhua = ["婺城区", "武义县", "浦江县", "磐安县", "兰溪市", "义乌市", "东阳市", "永康市", "金东区"]
    quzhou = ["柯城区", "衢江区", "常山县", "开化县", "龙游县", "江山市"]
    zhoushan = ["定海区", "普陀区", "岱山县", "嵊泗县"]
    taizhou = ["椒江区", "黄岩区", "路桥区", "三门县", "天台县", "仙居县", "温岭市", "临海市", "玉环市"]
    lishui = ["莲都区", "青田县", "缙云县", "遂昌县", "松阳县", "云和县", "庆元县", "景宁畲族自治县", "龙泉市"]

    zhejiang_dic = {
        'hangzhou': "杭州市",
        'ningbo': "宁波市",
        'wenzhou': "温州市",
        'jiaxing': "嘉兴市",
        'huzhou': "湖州市",
        'shaoxing': "绍兴市",
        'jinhua': "金华市",
        'quzhou': "衢州市",
        'zhoushan': "舟山市",
        'taizhou': "台州市",
        'lishui': "丽水市"
    }

    zhejiang_city_dic = {
        'hangzhou': hangzhou,
        'ningbo': ningbo,
        'wenzhou': wenzhou,
        'jiaxing': jiaxing,
        'huzhou': huzhou,
        'shaoxing': shaoxing,
        'jinhua': jinhua,
        'quzhou': quzhou,
        'zhoushan': zhoushan,
        'taizhou': taizhou,
        'lishui': lishui
    }

    @staticmethod
    def values(rge, start: int = 20, end: int = 150) -> list:
        ar = [random.randint(start, end) for _ in range(rge)]
        return ar

    # 浙江地图基于Map构建
    @staticmethod
    def zhejiang_map():
        logging.info("正在导出浙江全省城市地图...")
        html_path = "./html/map_zhejiang.html"
        if os.path.exists(html_path):
            os.remove(html_path)
        with open("./geojson/zhejiang_geojson.json", "r", encoding="utf-8") as file:
            stream = file.read()
        Map().add_js_funcs("echarts.registerMap('浙江省',{});".format(stream)) \
            .add("商家A", [list(z) for z in zip(ZJ.zhejiang_dic.values(), ZJ.values(len(ZJ.zhejiang_dic), 20, 150))], "浙江省") \
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-浙江省地图"), visualmap_opts=opts.VisualMapOpts()
        ) \
            .render(html_path)
        logging.info("浙江全省城市地图导出完成，文件路径:{}".format(html_path))
        return

    # 批量生成浙江全省城市地图
    @staticmethod
    def zhangjiang_cities_map():
        logging.info("正在批量导出全省所有城市地图...")
        for city in ZJ.zhejiang_dic.keys():
            ZJ.city_map(city)
        logging.info("全省所有城市地图导出完成")
        return

    # 生成城市地图
    # city 城市拼音
    def city_map(city):
        logging.info("正在导出{}地图...".format(city))
        html_path = "./html/map_{}.html".format(city)
        if os.path.exists(html_path):
            os.remove(html_path)
        geojson_path = "./geojson/{}_geojson.json".format(city)
        with open(geojson_path, "r", encoding="utf-8") as file:
            stream = file.read()
        Map().add_js_funcs("echarts.registerMap('{}',{});".format(ZJ.zhejiang_dic.get(city), stream)) \
            .add("商家A", [list(z) for z in zip(ZJ.zhejiang_city_dic.get(city), ZJ.values(
            len(ZJ.zhejiang_city_dic.get(city)), 20, 150))],
                 ZJ.zhejiang_dic.get(city)) \
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-{}地图".format(ZJ.zhejiang_dic.get(city))),
            visualmap_opts=opts.VisualMapOpts()
        ) \
            .render(html_path)
        logging.info("{}地图导出完成，文件路径:{}".format(city,html_path))
        return


zhejiang = ZJ()
