import random
from scipy.stats import shapiro, anderson
import os


def GetData(cnt_list_path, number_path):
    with open(cnt_list_path, 'r') as f:
        cnt_list = [int(line.strip()) for line in f]
    with open(number_path, 'r') as f:
        number = [int(line.strip()) for line in f]
    return cnt_list, number


def Verify_Gaussian(data, sample):
    rand_gen = random.SystemRandom()
    rand_gen.shuffle(data)
    sample_data = random.sample(data, sample)

    # 进行Shapiro-Wilk检验
    statistic, p_value = shapiro(sample_data)

    print(statistic, p_value)
    # 输出检验结果
    if p_value < 0.05:
        print("数据不符合正态分布")
    else:
        print("数据符合正态分布")

    # 进行Anderson-Darling检验
    result = anderson(sample_data)

    # 输出检验结果
    if result.statistic > result.critical_values[2]:
        print("数据不符合正态分布")
    else:
        print("数据符合正态分布")


P_name = ['192', '224', '256', '384', '521', '1279', '2281']

sample_number = 5000

if __name__ == "__main__":
    cwd = os.getcwd()
    copy_output_path = os.path.join(cwd, '..', 'Copy_Output')

    for idx in range(len(P_name)):
        cnt_list_path = os.path.join(copy_output_path, 'P_' + P_name[idx] + '_cnt_list.txt')
        number_path = os.path.join(copy_output_path, 'P_' + P_name[idx] + '_number.txt')
        cnt_list, number = GetData(cnt_list_path, number_path)

        data = []
        for i in range(len(cnt_list)):
            data += number[i] * [cnt_list[i]]

        print('----------------', 'P_'+P_name[idx], '-------------------')

        Verify_Gaussian(data, sample_number)
