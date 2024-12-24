import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.fft import fft, fftshift
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

# Now, when plotting, Chinese characters should display correctly


class SignalProcessor:
    def __init__(self, fs_cont=0.01, fs=20, duration=10):
        self.fs_cont = fs_cont  # 连续时间采样间隔 (秒)
        self.fs = fs  # 抽样频率 (Hz)
        self.duration = duration  # 信号持续时间 (秒)

        # 连续时间信号
        self.t_cont = np.arange(0, self.duration, self.fs_cont)
        self.signal_cont = 0.1 * np.cos(0.15 * np.pi * self.t_cont) + \
                           1.5 * np.sin(2.5 * np.pi * self.t_cont) + \
                           0.5 * np.cos(4 * np.pi * self.t_cont)

        # 抽样信号
        self.fs_sample = 1 / self.fs
        self.t_sample = np.arange(0, self.duration, self.fs_sample)
        self.signal_sample = 0.1 * np.cos(0.15 * np.pi * self.t_sample) + \
                             1.5 * np.sin(2.5 * np.pi * self.t_sample) + \
                             0.5 * np.cos(4 * np.pi * self.t_sample)

    def compute_spectrum(self):
        # 原始模拟信号的频谱计算
        n_cont = len(self.signal_cont)
        f_cont = self.fs_cont * np.fft.fftfreq(n_cont, d=self.fs_cont)
        signal_cont_f = fftshift(fft(self.signal_cont))

        # 抽样信号的频谱计算
        n_sample = len(self.signal_sample)
        f_sample = self.fs * np.fft.fftfreq(n_sample, d=self.fs_sample)
        signal_sample_f = fftshift(fft(self.signal_sample))

        return f_cont, signal_cont_f, f_sample, signal_sample_f

    def plot_signals(self):
        # 绘制时域和频域图形
        f_cont, signal_cont_f, f_sample, signal_sample_f = self.compute_spectrum()

        # 原始信号图
        plt.figure(figsize=(10, 8))
        plt.subplot(2, 1, 1)
        plt.plot(self.t_cont, self.signal_cont)
        plt.title('原模拟信号')
        plt.xlabel('时间 (秒)')
        plt.ylabel('信号幅度')

        plt.subplot(2, 1, 2)
        plt.plot(f_cont, np.abs(signal_cont_f))
        plt.title('原模拟信号频谱')
        plt.xlabel('频率 (Hz)')
        plt.ylabel('幅度')
        plt.tight_layout()
        plt.savefig('results/1.原始信号时频域.png', dpi=300)

        # 抽样信号图
        plt.figure(figsize=(10, 8))
        plt.subplot(2, 1, 1)
        plt.stem(self.t_sample, self.signal_sample, 'r')
        plt.title(f'抽样信号 ({self.fs} Hz采样)')
        plt.xlabel('时间 (秒)')
        plt.ylabel('信号幅度')

        plt.subplot(2, 1, 2)
        plt.plot(f_sample, np.abs(signal_sample_f))
        plt.title(f'抽样信号频谱 ({self.fs} Hz采样)')
        plt.xlabel('频率 (Hz)')
        plt.ylabel('幅度')
        plt.tight_layout()
        plt.savefig(f'results/2.抽样信号时频域（{self.fs}Hz采样）.png', dpi=300)

    def A_law_encoding(self, signal, A):
        # A 律编码公式
        return np.sign(signal) * np.log1p(A * np.abs(signal)) / np.log1p(A)

    def A_law_decoding(self, encoded_signal, A):
        # A 律解码公式
        return np.sign(encoded_signal) * (np.expm1(np.abs(encoded_signal) * np.log1p(A)) / A)

    def quantization_error(self, original_signal, decoded_signal):
        # 计算量化误差
        return original_signal - decoded_signal

    def encode_decode(self, A=87.6):
        # A律编码和解码
        signal_sample_normalized = self.signal_sample / np.max(np.abs(self.signal_sample))  # 归一化处理
        encoded_signal = self.A_law_encoding(signal_sample_normalized, A)

        # 转换为8位PCM码
        encoded_8bit = np.round((encoded_signal + 1) * 127)

        decoded_signal = self.A_law_decoding(encoded_signal, A)

        quantization_error = self.quantization_error(self.signal_sample, decoded_signal)

        MSE = np.mean(quantization_error ** 2)

        # 输出编码信息和量化误差
        return encoded_8bit, decoded_signal, quantization_error, MSE

    def plot_encoding_decoding(self, A=87.6):
        encoded_8bit, decoded_signal, quantization_error, MSE = self.encode_decode(A)

        # 绘制编码信号与译码信号对比图
        plt.figure(figsize=(10, 8))
        plt.subplot(2, 1, 1)
        plt.plot(self.t_sample, self.A_law_encoding(self.signal_sample / np.max(np.abs(self.signal_sample)), A), 'b',
                 linewidth=1.5)
        plt.title('A律编码后的信号')
        plt.xlabel('时间 (秒)')
        plt.ylabel('编码信号幅度')

        plt.subplot(2, 1, 2)
        plt.plot(self.t_sample, decoded_signal, 'r', linewidth=1.5)
        plt.title('译码信号')
        plt.xlabel('时间 (秒)')
        plt.ylabel('幅度')
        plt.tight_layout()
        plt.savefig('results/3.编码信号与译码信号.png', dpi=300)

        # 绘制量化误差图
        plt.figure(figsize=(10, 6))
        plt.plot(self.t_sample, quantization_error, 'g', linewidth=1.5)
        plt.title('量化误差')
        plt.xlabel('时间 (秒)')
        plt.ylabel('误差幅度')
        plt.savefig('results/4.量化误差图.png', dpi=300)

    def save_to_excel(self, filename='results/编译码数据.xlsx'):
        encoded_8bit, decoded_signal, quantization_error, _ = self.encode_decode()

        # 创建包含编码、解码和量化误差数据的表格
        data = {
            'Time': self.t_sample,
            '8位编码': encoded_8bit,
            '译码值': decoded_signal,
            '量化误差': quantization_error
        }
        df = pd.DataFrame(data)

        # 保存数据到 Excel 文件
        df.to_excel(filename, index=False)
        print(f"数据已保存到 Excel 文件: {filename}")


if __name__ == '__main__':
    processor = SignalProcessor()

    # 绘制原始信号和抽样信号的时频域图
    processor.plot_signals()

    # 绘制编码和解码信号对比图及量化误差图
    processor.plot_encoding_decoding()

    # 保存编解码数据到 Excel 文件
    processor.save_to_excel()
