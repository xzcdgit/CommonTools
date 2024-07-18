# 通道人检测获取数据分析


import os
import shutil
import time
import csv
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from datetime import datetime
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"C:\Windows\Fonts\长仿宋体.ttf")


def date_to_timestamp(date:str):
    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    stamp = int(date.timestamp())
    return stamp



class DataAnalysis:
    def __init__(
        self, files_folder_path: str, st_stamp: int, ed_stamp: int, mid_stamp: int
    ) -> None:
        self.mid_stamp = mid_stamp
        self.data = self.time_range_pick(files_folder_path, st_stamp, ed_stamp)

        data = self.data
        xs = data[:, 0].astype(float)  # 将字符串时间戳转为浮点数
        ys = np.diff(xs)
        ys = ys / 60  # y轴的持续时间转为分钟单位
        ys = np.insert(ys, 0, 0)  # y轴的持续时间转为分钟单位
        xs = pd.to_datetime(xs + 8 * 60 * 60, unit="s")

        self.xs = xs
        self.ys = ys

    # 根据文件名中的时间戳信息挑选指定时间范围内的数据并且排序后输出
    def time_range_pick(self, files_folder_path: str, st_stamp: int, ed_stamp: int):
        files = os.listdir(files_folder_path)
        new_list = []
        for file_full_name in files:
            suffix = file_full_name.split(".")[-1]
            file_name = file_full_name[: -(len(suffix) + 1)]
            stses = file_name.split("_")
            if len(stses) > 3:
                continue
            prefix = stses[0]
            if stses[1] == "True":
                person_flag = 1
            else:
                person_flag = 0
            time_stamp = float(int(stses[2]) / 1000)
            if time_stamp < st_stamp or time_stamp > ed_stamp:
                continue
            file_full_path = files_folder_path + "\\" + file_full_name
            new_list.append([time_stamp, person_flag, file_full_path])
        new_list.sort(key=lambda x: x[0])
        new_list = np.asarray(new_list)
        return new_list

    # 将列表中的文件复制到另一个文件夹
    def file_out(self, output_direction: str):
        file_full_paths = self.data[:, 2]
        for file_full_path in file_full_paths:
            shutil.copy2(file_full_path, output_direction)
        print("复制成功")

    # 数据分析
    def data_split_analysis(self):
        xs = self.xs
        ys = self.ys
        data = self.data
        mid_stamp = self.mid_stamp

        day_data = data[data[:,0].astype(float)<mid_stamp]
        night_data = data[data[:,0].astype(float)>=mid_stamp]
        day_non_comliance_num = (day_data[:, 1].astype(int)).sum()
        night_non_comliance_num = (night_data[:, 1].astype(int)).sum()
        day_num = len(day_data)
        night_num = len(night_data)
        day_comliance_num = day_num - day_non_comliance_num
        night_comliance_num = night_num - night_non_comliance_num

        tol_num = len(data)
        comliance_num = day_comliance_num + night_comliance_num
        non_comliance_num = day_non_comliance_num + night_non_comliance_num

        res_list = {
            'tol_num':tol_num,
            'comliance_num':comliance_num,
            'non_comliance_num':non_comliance_num,
            "day_num": day_num,
            "night_num": night_num,
            "day_compliance_num": day_comliance_num,
            "day_non-compliance_num": day_non_comliance_num,
            "night_compliance_num": night_comliance_num,
            "night_non-compliance_num": night_non_comliance_num,
        }
        print(res_list)
        return res_list

    # 将数据绘制为折线图
    def data_plot(self, save_path: str = ""):
        if self.xs is None or self.ys is None:
            self.anomaly_data_analysis()
        data = self.data
        xs = self.xs
        ys = self.ys
        fig, ax = plt.subplots(figsize=(128, 12), dpi=200)
        plt.plot(xs, ys)
        for index, x in enumerate(xs):
            if int(data[index][1]) == 1:
                color = "red"
            else:
                color = "green"
            plt.scatter(x, ys[index], c=color)
        # 设置x轴为时间轴
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
        ax.xaxis.set_major_locator(
            mdates.MinuteLocator(interval=240)
        )  # 每x分钟显示一个刻度

        plt.title("Line Chart(green:compliance red:non-compliance)")
        plt.xlabel("time(hour)")
        plt.ylabel("time interval(minute)")
        plt.grid(True, linestyle="--", alpha=0.7)
        # plt.gcf()
        if os.path.isdir(save_path):
            # 保存图表
            plt.savefig("test.png")
            print("保存成功")
        # 显示图表
        # plt.tight_layout()
        plt.show()
        print("finished")

    def anomaly_data_analysis(self):
        data = self.data
        xs = self.xs
        ys = self.ys
        csv_file = open("data.csv", "w", newline="", encoding="gbk")
        writer = csv.writer(csv_file)
        writer.writerow(
            ["触发时间1", "触发时间2", "时间间隔", "文件1路径", "文件2路径"]
        )
        tmp = np.where(ys < 1)
        for i in list(tmp[0]):
            if i == 0:
                continue
            writer.writerow(
                [
                    f"{str(xs[i-1])}",
                    f"{str(xs[i])}",
                    f"{str(xs[i]-xs[i-1])}",
                    f"{data[i-1][2]}",
                    f"{data[i][2]}",
                ]
            )
        csv_file.close()


if __name__ == "__main__":
    ed_stamp = date_to_timestamp('2024-07-21 00:00:00')
    st_stamp = date_to_timestamp('2024-07-10 00:00:00')
    mid_stamp = date_to_timestamp('2024-07-15 00:00:00')
    print(st_stamp,ed_stamp,mid_stamp)
    files_folder_path = r"C:\Users\01477483\Desktop\临时文件\数据统计\imgs"
    out_folder_path = r"C:\Users\01477483\Desktop\临时文件\数据统计\output"
    demo = DataAnalysis(files_folder_path, st_stamp, ed_stamp, mid_stamp)
    demo.anomaly_data_analysis()
    demo.data_split_analysis()
    demo.data_plot()
    
