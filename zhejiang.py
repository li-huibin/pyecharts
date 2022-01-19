import logging
import os.path
import random

from pyecharts import options as opts
from pyecharts.charts import Geo, Map
from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "http://127.0.0.1:8000/assets/"

class ZJ:
    # zhejiang_city = ["杭州市", "宁波市", "温州市", "嘉兴市", "湖州市", "绍兴市", "金华市", "衢州市", "舟山市", "台州市", "丽水市"]
    hangzhou = ["滨江区", "淳安县", "富阳区", "拱墅区", "建德市", "临安区", "临平区", "钱塘区", "上城区", "桐庐县", "西湖区", "萧山区", "临平区", "余杭区"]
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

    # 浙江省-市 映射表
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

    # 市-区县 映射表
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

    # 区县-数据映射 导入数据时全部将数据放在这个变量中
    dic_data = {'西湖区': 2.5}

    @staticmethod
    def values(rge, start: int = 20, end: int = 150) -> list:
        ar = [random.randint(start, end) for _ in range(rge)]
        return ar

    # 浙江地图基于Map构建
    @staticmethod
    def zhejiang_map():
        print("正在导出浙江全省城市地图...")
        html_path = "./html/map_zhejiang.html"
        if os.path.exists(html_path):
            os.remove(html_path)
        with open("./geojson/zhejiang_geojson.json", "r", encoding="utf-8") as file:
            stream = file.read()
        Map().add_js_funcs("echarts.registerMap('浙江省',{});".format(stream)) \
            .add("商家A", [list(z) for z in zip(ZJ.zhejiang_dic.values(), ZJ.values(len(ZJ.zhejiang_dic), 20, 150))],
                 "浙江省") \
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-浙江省地图"), visualmap_opts=opts.VisualMapOpts()
        ) \
            .render(html_path)
        print("浙江全省城市地图导出完成，文件路径:{}".format(html_path))
        return

    """浙江省地图(包含市区县)基于Map构建
    """
    @staticmethod
    def zhejiang_map_all():
        print("正在导出浙江全省城市地图...")
        html_path = "./html/map_zhejiang_all.html"
        if os.path.exists(html_path):
            os.remove(html_path)
        # 统计全省区县数量,并合并全省区县
        disTotal = 0
        all_disc = []
        for key in ZJ.zhejiang_city_dic.keys():
            disTotal += len(ZJ.zhejiang_city_dic.get(key))
            all_disc += ZJ.zhejiang_city_dic.get(key)
        with open("./geojson/zhejiang_cities_districts_geojson.json", "r", encoding="utf-8") as file:
            stream = file.read()
        Map(init_opts=opts.InitOpts(width='1200px', height='900px')) \
            .add_js_funcs("echarts.registerMap('浙江省',{});".format(stream)) \
            .add("商家A", [list(z) for z in zip(all_disc, ZJ.values(disTotal, 20, 500))],
                 "浙江省", label_opts=opts.LabelOpts(font_size=10)) \
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-浙江省地图"), visualmap_opts=opts.VisualMapOpts(max_=100)
        ) \
            .render(html_path)
        print("浙江全省城市地图导出完成，文件路径:{}".format(html_path))
        return

    # 批量生成浙江全省城市地图
    @staticmethod
    def zhangjiang_cities_map():
        print("正在批量导出全省所有城市地图...")
        for city in ZJ.zhejiang_dic.keys():
            ZJ.city_map(city)
        print("全省所有城市地图导出完成")
        return

    # 生成城市地图
    # city 城市拼音
    def city_map(city):
        print("正在导出{}地图...".format(city))
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
        print("{}地图导出完成，文件路径:{}".format(city, html_path))
        return

    ''' 加载excel中的数据，最终数据 区县-数据 做映射的，保存在变量dic_data中
          :param path 文件路径
    '''

    def load_data(path):
        wb = xlrd.open_workbook(path)
        # 创建字典key并且填充字典key对应的值
        for sheet_idx in range(len(wb.sheets())):
            sheet = wb.sheet_by_index(sheet_idx)
            data = {}
            for idx in range(sheet.nrows):
                if idx > 0:
                    data.setdefault(sheet.cell(idx, 1).value, sheet.cell(idx, 6).value)
            ZJ.dic_data.setdefault(sheet_idx, data)
        print(ZJ.dic_data)
        return len(wb.sheets())

    # 生成全省动态图
    def zhejiang_sync_data(path):
        width = '1000px'
        height = '900px'
        tl = Timeline(init_opts=opts.InitOpts(width=width, height=height)) \
            .add_schema(orient='vertical', is_auto_play=True, is_timeline_show=True)
        wb = xlrd.open_workbook(path)
        for idx in range(len(wb.sheets())):
            with open("./geojson/zhejiang_cities_districts_geojson.json", "r", encoding="utf-8") as file:
                stream = file.read()
            keys = []
            values = []
            for i in range(wb.sheet_by_index(idx).nrows):
                if i > 0:
                    keys.append(wb.sheet_by_index(idx).cell(i, 1).value)
                    values.append(wb.sheet_by_index(idx).cell(i, 6).value)

            map0 = Map(init_opts=opts.InitOpts(width=width, height=height)) \
                .add_js_funcs("echarts.registerMap('浙江省',{});".format(stream)) \
                .add("商家A", [list(z) for z in zip(keys, values)], "浙江", min_scale_limit=1) \
                .set_global_opts(title_opts=opts.TitleOpts(title="Map-浙江省地图"),
                                 visualmap_opts=opts.VisualMapOpts(max_=100, is_piecewise=True)
                                 )
            tl.add(map0, "{}年".format(idx))
        tl.render("html/timeline_map.html")
        return

zhejiang = ZJ()
