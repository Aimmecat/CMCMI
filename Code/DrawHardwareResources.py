import matplotlib.pyplot as plt
import numpy as np

latency_lut = [1.95, 2.56, 1.87, 2.45, 2.32, 22.08, 7.93]

latency_slices = [1.95, 2.56, 1.87, 2.45, 2.32, 47.00, 7.93]

LUT = [4.2, 4.1, 2.7, 2.7, 5.8, 1.1, 2.3]

Slices = [0.712, 1.132, 0.456, 0.854, 1.480, 0.915, 0.592]

alg_lut = ['CT-IMI(Ultrascale)', 'CT-IMI(Vertex-7)', 'CT-CMMI(Ultrascale)', 'CT-CMMI(Vertex-7)', 'Hossain(Vertex-7)',
           'Murat(Spartan-6)', 'Mrabet(Vertex-5)']

alg_slices = ['CT-IMI(Ultrascale)', 'CT-IMI(Vertex-7)', 'CT-CMMI(Ultrascale)', 'CT-CMMI(Vertex-7)', 'Hossain(Vertex-7)',
              'Deshpande(Ultrascale)', 'Mrabet(Vertex-5)']

color_list = ['green', '#FF6347', '#FF69B4', '#B8860B', '#A0522D', '#1E90FF', 'blue']

symbol = ['*', '^', '+', 'o', 'x', 'v', 's']

if __name__ == "__main__":
    fig, ax = plt.subplots(1, 2)

    for idx in range(len(latency_lut)):
        ax[0].plot(latency_lut[idx], LUT[idx], symbol[idx], markersize=12, color=color_list[idx], label=alg_lut[idx])
    ax[0].legend(fontsize=15)
    ax[0].set_xlabel("Latency(μs)", fontsize=15)
    ax[0].set_ylabel("LUT numbers(×10³)", fontsize=15)
    ax[0].set_title("The differences of LUT and Latency between each design", fontsize=15)
    ax[0].set_xticks(np.linspace(1.5, 23, 9))
    ax[0].set_yticks(np.linspace(0.5, 6, 9))
    ax[0].grid(alpha=0.4)

    for idx in range(len(latency_lut)):
        ax[1].plot(latency_slices[idx], Slices[idx], symbol[idx], markersize=12, color=color_list[idx], label=alg_slices[idx])
    ax[1].legend(fontsize=15)
    ax[1].set_xlabel("Latency(μs)", fontsize=15)
    ax[1].set_ylabel("Slice numbers(×10³)", fontsize=15)
    ax[1].set_title("The differences of Slice and Latency between each design", fontsize=15)
    ax[1].set_xticks(np.linspace(1.5, 48, 9))
    ax[1].set_yticks(np.linspace(0.25, 1.7, 9))
    ax[1].grid(alpha=0.4)

    plt.show()
