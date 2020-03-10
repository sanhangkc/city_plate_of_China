# -*- coding: utf-8 -*-
"""
Project_name:drawing plate for city
@author: 帅帅de三叔
Created on Wed Oct 30 15:16:44 2019
"""
import sys
arcpy_path = [r'D:\Python27\ArcGIS10.6\Lib\site-packages',
              r'D:\Program Files (x86)\ArcGIS\Desktop10.6\arcpy',
              r'D:\Program Files (x86)\ArcGIS\Desktop10.6\bin',
              r'D:\Program Files (x86)\ArcGIS\Desktop10.6\ArcToolbox\Scripts']
sys.path.extend(arcpy_path)  #
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr 
reload(sys) #通过import引用进来时,setdefaultencoding函数在被系统调用后被删除了，所以必须reload一次
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde 
sys.setdefaultencoding('utf-8')

import arcpy #导入地理处理模块
from arcpy import env #导入环境类
env.workspace = r"D:\python for ArcGIS\绘制北京板块" #设置工作目录
env.overwriteOutput = True #是否开启复写
import pandas as pd #导入数据分析模块
plate_data = pd.read_excel(u"北京板块边界.xlsx") #读取板块数据
rows, cols = plate_data.shape #数据框尺寸
lng_lat = plate_data[u'边界坐标'] #经纬度数据
plate_name = plate_data[u'板块'] #板块名称

#factoryCode = arcpy.GetParameterAsText(4490) #WGS_1984_World_Mercator投影坐标系工厂代码4490，3395
#spatial_ref = arcpy.SpatialReference(factoryCode) #设置空间参考参数           
spatial_ref = arcpy.SpatialReference('China Geodetic Coordinate System 2000') #China Geodetic Coordinate System 2000 or WGS 1984 World Mercator

polygonPoints = arcpy.Array() #用来存放构成多边形的折点
polygonGeometryList = [] #用来存放多边形几何对象组

for row in range(0, rows): #按行循环
    points = lng_lat[row].split(";") #折点
    for spot in points:
        xy = spot.split(",") #折点经度和纬度
        if len(xy) == 2:
            point = arcpy.Point() #几何对象，用来存放折点对象
            point.id = row; point.X = float(xy[0]); point.Y = float(xy[1])  #转为点对象
            polygonPoints.add(point) #构成一串折点
            #print(point.id) #判断哪些点属于同一个多边形
    polygon = arcpy.Polygon(polygonPoints,spatial_ref,"","") #利用折点构造多边形带空间参考
    polygonGeometryList.append(polygon) #把多边形追加到数组  
    polygonPoints.removeAll() #移除所有折点
result = arcpy.CopyFeatures_management(polygonGeometryList, r"D:\python for ArcGIS\绘制北京板块\plate_beijing.shp", "POLYGON")