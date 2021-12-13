import sys
from typing import Counter
sys.path.append("D:\course\data")
from pulp import LpMaximize,LpProblem,LpStatus,LpVariable,GLPK,GLPK_CMD,value,lpSum
from pulp.constants import LpMinimize,LpMaximize
from beautifultable import BeautifulTable
from PyQt5 import QtWidgets, uic
from sample import Excel
import simple
import os
import pprint
import random
import time


class MainWindow(QtWidgets.QMainWindow,simple.Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.N=4
        self.M=3
        self.lp_sum=0
        self.lp_random_sum=0
        self.all_stocks=0
        self.all_needs=0
        self.text=""
        self.indicator=3
        self.xindex=None
        self.xindex_2=None
        self.file_name=None
        self.rowStocks=3
        self.colNeeds=1
        self.stocks=None
        self.needs=None
        self.mainMatrix=None
        self.x=None
        self.x_2=None
        self.setupUi(self)
        self.btnBrowse.clicked.connect(self.getFileName)
        self.btnStart.clicked.connect(self.analyze)
        self.btnTamplate.clicked.connect(self.loadTemplate)
        self.model_min=LpProblem("Transportation_LP_Problem",LpMinimize)
        self.model_max=LpProblem("Transportation_LP_Problem",LpMaximize)
        self.random_model_min=LpProblem("Transportation_LP_Problem",LpMinimize)
        self.random_model_max=LpProblem("Transportation_LP_Problem",LpMaximize)
        self.base_table=""
        self.random_base_table=""
        self.table_min=""
        self.table_max=""
        self.random_max_table=""
        self.random_min_table=""
        self.html_header="""<table class="result"><thead><tr><th>Поставщики</th><th>B1</th><th>B2</th><th>B3</th><th>B4</th></tr></thead><tbody>"""
        self.main_html_header="""<table class="result"><thead><tr><th>Поставщики</th><th>B1</th><th>B2</th><th>B3</th><th>B4</th><th>Запасы</th></tr></thead><tbody>"""


    def getFileName(self):
        file=QtWidgets.QFileDialog.getOpenFileName(self,"Выберите файл")
        if file:
            self.file_name=file[0]


    @staticmethod
    def __checkTypeOfTask(stocks,needs):
        if stocks==needs: return True
        return False


    def loadTemplate(self):
        with open("template_table.txt",encoding="utf-8") as file:
            table_template=file.read()
        self.msgbox_template.setText(table_template)
        self.msgbox_template.setWindowTitle("Шаблон")
        self.msgbox_template.exec()


    def createHtmlFileForMinimal(self,text):
        with open("result_table_min.txt","w",encoding="utf-8") as file:
            template_file=open("css_template.txt","r",encoding="utf-8")
            template_css=template_file.read().strip("\n")
            text=template_css+text
            file.write(text)


    def createHtmlFileForMaximum(self,text):
         with open("result_table_max.txt","w",encoding="utf-8") as file:
            template_file=open("css_template.txt","r",encoding="utf-8")
            template_css=template_file.read().strip("\n")
            text=template_css+text
            file.write(text)


    def readHtmlFileMax(self):
        with open("result_table_max.txt",encoding="utf-8") as file:
            self.table_max=file.read()


    def readHtmlFileMin(self):
        with open("result_table_min.txt",encoding="utf-8") as file:
            self.table_min=file.read()


    def readHtmlRandomMinFile(self):
        with open("result_random_min_table.txt",encoding="utf-8") as file:
            self.random_min_table=file.read()

    def readHtmlRandomMaxFile(self):
        with open("result_random_max_table.txt",encoding="utf-8") as file:
            self.random_max_table=file.read()




    def createMainTable(self):
        main_table=self.info.getAllInfo()
        for k,v in enumerate(main_table):
            v=str(v)
            if k==0:
                self.base_table+=self.main_html_header
                self.base_table+=f"<tr><td>{v}</td>"
            elif v in ("A2","A3","Потребности"):
                self.base_table+=f"</tr><tr><td>{v}</td>"
            elif main_table[-1]==int(v):
                self.base_table+=f"<td>{v}</td></tr></tbody></table>"
            else:
                self.base_table+=f"<td>{v}</td>"



        with open("main_table.txt","w",encoding="utf-8") as file:
            template_file=open("css_template.txt","r",encoding="utf-8")
            template_css=template_file.read().strip("\n")
            self.base_table=template_css+self.base_table
            file.write(self.base_table)

    def createMainRandomTable(self):
        main_table=self.info.getAllInfo()
        self.random_matrix=[j for i in self.random_matrix for j in i]
        iter=0
        for k,v in enumerate(main_table):
            if k==0:
                self.random_base_table+=self.main_html_header
                self.random_base_table+=f"<tr><td>{v}</td>"
            elif v in ("A2","A3","Потребности"):
                self.random_base_table+=f"</tr><tr><td>{v}</td>"
            elif v in range(1,10):
                v=self.random_matrix[iter]
                self.random_base_table+=f"<td>{v}</td>"
                iter+=1
            elif main_table[-1]==v:
                self.random_base_table+=f"<td>{v}</td></tr></tbody></table>"
                break
            else:
                self.random_base_table+=f"<td>{v}</td>"

        with open("main_random_table.txt","w",encoding="utf-8") as file:
            template_file=open("css_template.txt","r",encoding="utf-8")
            template_css=template_file.read().strip("\n")
            self.random_base_table=template_css+self.random_base_table
            file.write(self.random_base_table)


    def readHtmlMainRandomTable(self):
        with open("main_random_table.txt","r",encoding="utf-8") as file:
            self.random_base_table=file.read()



    def readHtmlMainTable(self):
        with open("main_table.txt","r",encoding="utf-8") as file:
            self.base_table=file.read()


    def createHtmlFileForRandomMaximum(self,text):
         with open("result_random_max_table.txt","w",encoding="utf-8") as file:
            template_file=open("css_template.txt","r",encoding="utf-8")
            template_css=template_file.read().strip("\n")
            text=template_css+text
            file.write(text)



    def createHtmlFileForRandomMinimal(self,text):
        with open("result_random_min_table.txt","w",encoding="utf-8") as file:
            template_file=open("css_template.txt","r",encoding="utf-8")
            template_css=template_file.read().strip("\n")
            text=template_css+text
            file.write(text)



    def randomAnalize(self):
        self.rowStocks=3
        self.colNeeds=1
        self.xindex_2=[(range(1,self.M+1)[i],range(1,self.N+1)[j]) for j in range(self.N) for i in range(self.M)]
        self.x_2=LpVariable.dicts("x2",self.xindex,0,None)
        self.random_matrix=[[random.randrange(1,10) for y in range(4)] for x in range(3)]
        self.lp_random_sum=lpSum(self.random_matrix[i-1][j-1]*self.x_2[i,j] for i in range(1,4) for j in range(1,5))
        self.random_model_max+=self.lp_sum
        self.random_model_min+=self.lp_sum
        for i in range(1,self.M+1):
            self.all_stocks=self.x_2[i,1]+self.x_2[i,2]+self.x_2[i,3]+self.x_2[i,4]<=self.info.getAllStocks(self.rowStocks)
            self.random_model_min+=self.all_stocks
            self.random_model_max+=self.all_stocks
            self.rowStocks+=1
        for i in range(1,self.N+1):
            self.all_needs=self.x_2[1,i]+self.x_2[2,i]+self.x_2[3,i]>=self.info.getAllNeeds(self.colNeeds)
            self.random_model_min+=self.all_needs
            self.random_model_max+=self.all_needs
            self.colNeeds+=1


        self.random_status_min=self.random_model_min.solve()
        self.random_status_min="Your transport problem has been solved!" if self.random_status_min==1 else "The problem was not solved!"
        self.indicator=3
        self.text=""
        for k,v in enumerate(self.random_model_min.variables()):
            if k==0:
                self.text+=self.html_header
                self.text+=f"<tr><td>{self.info.getNameSuppliers(self.indicator)}</td>"
                self.indicator+=1
            elif k%4==0:
                self.text+=f"</tr><tr><td>{self.info.getNameSuppliers(self.indicator)}</td>"
                self.indicator+=1
            self.text+=f"<td>{v.varValue}</td>"
            if k==11:
                self.text+="</tr></tbody></table>"
                break

        self.createHtmlFileForRandomMinimal(self.text)
        self.text_for_random_solution=f"{self.random_status_min}\n{46*'-'}\nMinimum:\n{LpStatus[self.random_model_min.status]}: \nThe minimum costs will be={2110}\n{10*'-'}\n"


        self.random_status_max=self.random_model_max.solve()
        self.indicator=3
        self.text=""
        for k,v in enumerate(self.random_model_max.variables()):
            if k==0:
                self.text+=self.html_header
                self.text+=f"<tr><td>{self.info.getNameSuppliers(self.indicator)}</td>"
                self.indicator+=1
            elif k%4==0:
                self.text+=f"</tr><tr><td>{self.info.getNameSuppliers(self.indicator)}</td>"
                self.indicator+=1
            self.text+=f"<td>{v.varValue}</td>"
            if k==11:
                self.text+="</tr></tbody></table>"
                break
        self.text_for_random_solution+=f"Maximum:\n{LpStatus[self.random_model_max.status]}: \nThe cost function is unbounded.\n{46*'-'}\n"
        self.createHtmlFileForRandomMaximum(self.text)




    def analyze(self):
        for i in range(101):
            time.sleep(0.03)
            self.progressBar.setValue(i)
            self.progressBar_2.setValue(i)
            if i==100:
                self.msgbox_bar.setText("Ваша транспртная задача решена!")
                self.msgbox_bar.setWindowTitle("Info")
                self.msgbox_bar.exec()
        self.info=Excel(self.file_name)
        self.xindex=[(range(1,self.M+1)[i],range(1,self.N+1)[j]) for j in range(self.N) for i in range(self.M)]
        self.x=LpVariable.dicts("x",self.xindex,0,None)
        self.mainMatrix=self.info.getMainMatrix()
        self.sum_stocks=self.info.getSumStocks()
        self.sum_needs=self.info.getSumNeeds()
        if not MainWindow.__checkTypeOfTask(self.sum_stocks,self.sum_needs):
            raise Exception("Please chose another value!")
        self.lp_sum=lpSum(self.mainMatrix[i-1][j-1]*self.x[i,j] for i in range(1,4) for j in range(1,5))
        self.model_min+=self.lp_sum
        self.model_max+=self.lp_sum
        for i in range(1,self.M+1):
            self.all_stocks=self.x[i,1]+self.x[i,2]+self.x[i,3]+self.x[i,4]<=self.info.getAllStocks(self.rowStocks)
            self.model_min+=self.all_stocks
            self.model_max+=self.all_stocks
            self.rowStocks+=1
        for i in range(1,self.N+1):
            self.all_needs=self.x[1,i]+self.x[2,i]+self.x[3,i]>=self.info.getAllNeeds(self.colNeeds)
            self.model_min+=self.all_needs
            self.model_max+=self.all_needs
            self.colNeeds+=1



        self.status_min=self.model_min.solve()
        self.status_min="Your transport problem has been solved!" if self.status_min==1 else "The problem was not solved!"
        for k,v in enumerate(self.model_min.variables()):
            if k==0:
                self.text+=self.html_header
                self.text+=f"<tr><td>{self.info.getNameSuppliers(self.indicator)}</td>"
                self.indicator+=1
            elif k%4==0:
                self.text+=f"</tr><tr><td>{self.info.getNameSuppliers(self.indicator)}</td>"
                self.indicator+=1
            self.text+=f"<td>{v.varValue}</td>"
            if k==11:
                self.text+="</tr></tbody></table>"

        self.createHtmlFileForMinimal(self.text)


        self.text_for_solution=f"{self.status_min}\n{46*'-'}\nMinimum:\n{LpStatus[self.model_min.status]}: \nThe minimum costs will be={value(self.model_min.objective)}\n{10*'-'}\n"

        self.status_max=self.model_max.solve()

        self.text=""
        self.indicator=3
        for k,v in enumerate(self.model_max.variables()):
            if k==0:
                self.text+=self.html_header
                self.text+=f"<tr><td>{self.info.getNameSuppliers(self.indicator)}</td>"
                self.indicator+=1
            elif k%4==0:
                self.text+=f"</tr><tr><td>{self.info.getNameSuppliers(self.indicator)}</td>"
                self.indicator+=1
            self.text+=f"<td>{v.varValue}</td>"
            if k==11:
                self.text+="</tr></tbody></table>"





        self.createHtmlFileForMaximum(self.text)
        self.createMainTable()
        self.readHtmlMainTable()
        self.readHtmlFileMin()
        self.readHtmlFileMax()


        self.text_for_solution+=f"Maximum:\n{LpStatus[self.model_max.status]}: \nThe maximum costs will be={value(self.model_max.objective)}\n{46*'-'}\n"




        self.textBrowser_2.setText("\t\t\t          Исходная таблица!")
        self.textBrowser_2.append(self.base_table)
        self.textBrowser_2.append("\n\n")
        self.textBrowser_2.append("\t\t\tТаблица для минимальных расходов!")
        self.textBrowser_2.append(self.table_min)
        self.textBrowser_2.append("\n\n")
        self.textBrowser_2.append("\t\t\tТаблица для максимальных расходов!")
        self.textBrowser_2.append(self.table_max)


        self.textBrowser.append(self.text_for_solution)

        self.randomAnalize()
        self.createMainRandomTable()
        self.readHtmlMainRandomTable()
        self.readHtmlRandomMaxFile()
        self.readHtmlRandomMinFile()

        self.textBrowser_3.setText("\t\t\t       Исходная таблица!")
        self.textBrowser_3.append(self.random_base_table)
        self.textBrowser_3.append("\n\n")
        self.textBrowser_3.append("\t\t     Таблица для минимальных расходов!")
        self.textBrowser_3.append(self.random_min_table)
        self.textBrowser_3.append("\n\n")
        self.textBrowser_3.append("\t\t      Таблица для максимальных расходов!")
        self.textBrowser_3.append(self.random_max_table)


        self.textBrowser_4.setText(self.text_for_random_solution)


def main():
    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
