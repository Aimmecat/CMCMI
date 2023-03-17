import random
from scipy.stats import shapiro, anderson

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