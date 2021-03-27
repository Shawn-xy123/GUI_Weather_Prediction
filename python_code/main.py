from get_weather_information import get_city_url,get_weather_information

import matplotlib.pyplot as plt
from window import Ui_Dialog
from PyQt4.QtGui  import *
from PyQt4.QtCore import *
import tkinter.messagebox
from tkinter import *

#function to draw a picture of weather
def draw_picture(low_temperature,high_temperature,date):
    chart_name='weather.png'
    x=range(1,8)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # to show Chinese
    plt.plot(x,low_temperature,label='low_temperature',linewidth=1,color='b',marker='o',markerfacecolor='blue',markersize=7)
    plt.plot(x,high_temperature,label='high_temperature',linewidth=1,color='r',marker='o',markerfacecolor='red',markersize=7)
    plt.xlabel('date')
    plt.xticks(x, date,color='blue')
    plt.tick_params(labelsize=8)
    plt.ylabel('temperature/°C')
    plt.title('Weather prediction of 7 days')
    plt.legend()
    plt.savefig(chart_name)#save the chart
    plt.close()
    return chart_name



# result,low_temperature,high_temperature,weather,date=get_weather_information('合肥')
# print(result)
# draw_picture(low_temperature,high_temperature)
#according to the result to draw a picture


class MainWindow(QWidget,Ui_Dialog):
    def __init__(self, city_name2url,parent=None):
        self.city_name2url=city_name2url#define the connection between url and city name
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.lineEdit.setPlaceholderText('请输入城市名称查天气')
        self.pushButton.clicked.connect(self.push_search_Clicked)
        # define the function of search button
    def push_search_Clicked(self):
        city_name=self.lineEdit.text()#get the city name from input lineedit

        #city name not allowed to be null
        if city_name=='':
            root2 = Tk()
            root2.withdraw()
            tkinter.messagebox.showinfo(title='提示', message='请输入城市名称!')
            return 0

        #city name must in city_name2url keys
        elif city_name not in city_name2url.keys():
            root3 = Tk()
            root3.withdraw()
            tkinter.messagebox.showinfo(title='提示', message='该城市不在查询范围内!')
            return 0
        else:
            try:
                result, low_temperature, high_temperature, weather, date = get_weather_information(city_name, self.city_name2url)
            except Exception as err:
                root4 = Tk()
                root4.withdraw()
                tkinter.messagebox.showinfo(title='提示', message='请检查网络连接是否正常!')
                return 0
            self.city_label.setText(city_name)  # edit the name of city we need to predict
            # draw the chart
            chart_name = draw_picture(low_temperature, high_temperature, date)
            # set the chart
            pix = QPixmap(chart_name)
            self.label_2.setPixmap(pix)

            # add data to the table
            self.tableWidget.verticalHeader().setVisible(False)
            # set the num of row
            self.tableWidget.setRowCount(7)
            # add data to the table
            for row in range(7):
                for j in range(3):
                    item = QTableWidgetItem(str(result[row][j]))
                    self.tableWidget.setItem(row, j, item)


if __name__=='__main__':
    try:
        city_name2url= get_city_url()#get the information between city name and url
    except Exception as err:
        root1 = Tk()
        root1.withdraw()
        tkinter.messagebox.showinfo(title='提示', message='请检查网络连接情况后重新尝试!')
        exit(0)
    app = QApplication(sys.argv)#
    myapp1 = MainWindow(city_name2url)#create MainWindow class
    myapp1.show()#start to run
    app.exec_()


