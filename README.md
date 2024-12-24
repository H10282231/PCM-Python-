# Pulse Code Modulation (PCM)

## Overview

This project implements a signal processing class called Pulse Code Modulation (PCM) that simulates continuous and sampled signals, performs A-law encoding and decoding, computes the quantization error, and generates corresponding plots for time-domain, frequency-domain, and quantization errors. The results are saved as images and exported to an Excel file. This script demonstrates basic concepts of signal processing such as signal sampling, encoding, decoding, and quantization error analysis.

## Requirements

To run this project, you need to have the following Python libraries installed:

- `numpy`: For numerical operations and signal generation
- `matplotlib`: For plotting graphs
- `pandas`: For handling data and saving to Excel
- `scipy`: For FFT computations

You can install the required libraries using the following command:

```bash
pip install numpy matplotlib pandas scipy
```

## Class Overview

### `SignalProcessor` Class

This class encapsulates the signal processing operations, including signal generation, frequency spectrum computation, A-law encoding and decoding, quantization error computation, and plotting.

#### Methods:

- **`__init__(self, fs_cont=0.01, fs=20, duration=10)`**:
   Initializes the signal processor with continuous-time signal sampling interval (`fs_cont`), discrete sampling frequency (`fs`), and signal duration (`duration`).
- **`compute_spectrum(self)`**:
   Computes the frequency spectrum of both the continuous-time and sampled signals using FFT.
- **`plot_signals(self)`**:
   Plots the time-domain and frequency-domain representations of both the continuous and sampled signals.
- **`A_law_encoding(self, signal, A)`**:
   Applies A-law encoding to the input signal with a given parameter `A`.
- **`A_law_decoding(self, encoded_signal, A)`**:
   Decodes the A-law encoded signal back to the original signal.
- **`quantization_error(self, original_signal, decoded_signal)`**:
   Computes the quantization error between the original signal and the decoded signal.
- **`encode_decode(self, A=87.6)`**:
   Performs A-law encoding and decoding, and calculates the quantization error and Mean Squared Error (MSE).
- **`plot_encoding_decoding(self, A=87.6)`**:
   Plots the encoded signal, decoded signal, and quantization error.
- **`save_to_excel(self, filename='results/编译码数据.xlsx')`**:
   Saves the encoded, decoded signals, and quantization error to an Excel file.

## Usage

1. **Signal Generation and Spectrum Calculation**

   The `SignalProcessor` class generates both a continuous-time signal and a sampled signal. The frequency spectra of both signals are computed using the Fast Fourier Transform (FFT).

   Example:

   ```python
   processor = SignalProcessor()
   processor.plot_signals()
   ```

   This will generate two figures showing the time-domain and frequency-domain plots for the continuous and sampled signals.

2. **A-law Encoding and Decoding**

   The `encode_decode` method performs A-law encoding and decoding. The quantization error and Mean Squared Error (MSE) are calculated for the sampled signal.

   Example:

   ```python
   processor.plot_encoding_decoding()
   ```

   This will generate two figures:

   - The first figure shows the encoded and decoded signals.
   - The second figure shows the quantization error.

3. **Saving Results to Excel**

   The `save_to_excel` method saves the encoded signal, decoded signal, and quantization error to an Excel file.

   Example:

   ```python
   processor.save_to_excel()
   ```

   This will save the data to an Excel file named `编译码数据.xlsx`.

## Output Files

1. **Signal Plots**:
   - `results/1.原始信号时频域.png`: Time and frequency-domain plots for the original signal.
   - `results/2.抽样信号时频域（{fs}Hz采样）.png`: Time and frequency-domain plots for the sampled signal.
   - `results/3.编码信号与译码信号.png`: A comparison of the encoded and decoded signals.
   - `results/4.量化误差图.png`: The quantization error plot.
2. **Excel File**:
   - `results/编译码数据.xlsx`: An Excel file containing the time, encoded signal, decoded signal, and quantization error.

## Customization

You can modify the following parameters to experiment with different signal properties and encoding parameters:

- **`fs_cont`**: Continuous-time sampling interval (seconds). Default is `0.01`.
- **`fs`**: Sampling frequency for the discrete-time signal (Hz). Default is `20`.
- **`duration`**: Duration of the signal (seconds). Default is `10`.
- **`A`**: A-law encoding parameter. Default is `87.6`.

## Example

```python
if __name__ == '__main__':
    processor = SignalProcessor(fs_cont=0.005, fs=10, duration=15)

    # Plot time-domain and frequency-domain signals
    processor.plot_signals()

    # Plot encoded and decoded signals, and quantization error
    processor.plot_encoding_decoding(A=90)

    # Save the data to an Excel file
    processor.save_to_excel('results/编解码数据_90.xlsx')
```

## Conclusion

This project demonstrates the fundamental concepts of signal processing, including continuous and discrete signal representation, A-law encoding and decoding, and the analysis of quantization errors. It generates visualizations and saves the results in both images and Excel files for further analysis.