import numpy as np
import openpyxl


def pi_evaluation(performance_indicator_id, is_weight):
    workbook = openpyxl.load_workbook("C:\Users\ereno\Desktop\4.1\bitirme projesi\excel_data.xlsm")

    w_pi = workbook["Data"]

    row = w_pi.range("B4").row
    # weight = col_b
    weight = w_pi.range("B4").column
    # normalized score = col_f = Average / Out of
    normalized_score = w_pi.range("F4").column
    # normalized std = col_g = std / Average
    normalized_std = w_pi.range("G4").column
    # PIs = col_H
    pis = w_pi.range("H4").column

    total_weight = 0
    pi_weight = 0
    result_count = 0
    j = 1

    results = np.zeros(500)
    std_devs = np.zeros(500)

    while w_pi.cells(row, weight).value != "":
        pi_ids = w_pi.cells(row, pis).value

        total_weight += w_pi.cells(row, weight).value

        position = pi_ids.find(performance_indicator_id)

        if position > 0:
            pi_weight += w_pi.cells(row, weight).value

            result_count += 1

            results[result_count] = w_pi.cells(row, normalized_score).value
            std_devs[result_count] = w_pi.cells(row, normalized_std).value

        row += 1

    workbook.close()

    if result_count > 1:
        bubble_sort(results, std_devs, j, result_count)

    if is_weight == 1:
        return pi_weight / 2
    elif is_weight == 0:
        return results[int(result_count / 2) + 1]
    elif is_weight == 2:
        return std_devs[int(result_count / 2) + 1]


def bubble_sort(arr, arr2, l, r):
    lng_min = l
    lng_max = r

    for i in range(lng_min, lng_max - 1):
        for j in range(i + 1, lng_max):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
                arr2[i], arr2[j] = arr2[j], arr2[i]
