import numpy as np
import xlrd
from openpyxl import load_workbook

def read_xlsx_xlrd(path, cell):
    '''

    :param path: STR path of xlsx file
    :param cell: NDARRAY target location of cell
    :return: STR contents of cell
    '''
    chart = xlrd.open_workbook(path)
    first_sheet = chart.sheet_by_index(0)
    cell_list = first_sheet.row_slice(rowx=cell[0], start_colx=cell[1], end_colx = cell[2])
    cell_array = np.asarray(cell_list)
    cell_string = ''.join(map(str, cell_array))
    tmp = cell_string.replace('text:\'', '')
    cell_final = tmp.replace('\'', '')
    return cell_final


if __name__ == '__main__':
    path = ('Data/Competency model 2 dimensional.xlsx')
    cell = [3, 1, 2]
    print((read_xlsx_xlrd(path, cell)))
