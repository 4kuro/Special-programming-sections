import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import Slider, CheckButtons, Button

def generate_noise(mean, covarianse, length):
    return mean + covarianse * np.random.randn(length)

def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, start, end, step):
    x = np.arange(start, end, step)
    y = amplitude * np.sin(frequency * x + phase)
    noise = generate_noise(noise_mean, noise_covariance, len(x))
    return x, y, noise

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.35)

start = 0
end = 20
step = 0.1

amplitude_init = 1
frequency_init = 1
mean_init = 0.1
cov_init = 0.3

#x = np.arange(start, end, step)
x, y, noise = harmonic_with_noise(amplitude_init, frequency_init, 0, mean_init, cov_init, start, end, step)
filtered = pd.Series(y + noise).rolling(4).mean()
plot, = plt.plot(x, y, label='Harmonic')
plot_filtered, = plt.plot(x, filtered, label='Filtered')
plot_filtered.set_visible(False)
fig.legend()

ax1 = plt.axes([0.25, 0.1, 0.65, 0.03])
ax2 = plt.axes([0.25, 0.15, 0.65, 0.03])
ax3 = plt.axes([0.25, 0.2, 0.65, 0.03])
ax4 = plt.axes([0.25, 0.25, 0.65, 0.03])
ax5 = plt.axes([0.25, 0.3, 0.18, 0.1])
ax6 = plt.axes([0.5, 0.3, 0.18, 0.1])
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])

slider_amplitude = Slider(ax1, 'Amplitude', 0.1, 5, valinit=amplitude_init, valstep=0.1)
slider_frequency = Slider(ax2, 'Frequency', 0.01, 3, valinit=frequency_init, valstep=0.01)
slider_mean = Slider(ax3, 'Noise mean', -0.5, 0.5, valinit=mean_init, valstep=0.05)
slider_cov = Slider(ax4, 'Noise covariance', 0, 0.75, valinit=cov_init, valstep=0.01)
check_noise = CheckButtons(ax5, ['Show noise'])
check_filtered = CheckButtons(ax6, ['Show filtered'])
checked = False
checked_filtered = False
button = Button(resetax, 'Reset')

def update_harmonic(val):
    global y, checked, filtered
    filtered = pd.Series(y + noise).rolling(8).mean()
    _, y, _ = harmonic_with_noise(
        slider_amplitude.val,
        slider_frequency.val,
        0,
        slider_mean.val,
        slider_cov.val,
        start,
        end,
        step
    )
    update_plot()

def update_noise(val):
    global noise, filtered
    filtered = pd.Series(y + noise).rolling(8).mean()
    _, _, noise = harmonic_with_noise(
        slider_amplitude.val,
        slider_frequency.val,
        0,
        slider_mean.val,
        slider_cov.val,
        start,
        end,
        step
    )
    update_plot()

def update_checkbox(label):
    global filtered
    global checked
    checked = not checked
    filtered = pd.Series(y + noise).rolling(8).mean()
    update_plot()

def reset(event):
    slider_amplitude.reset()
    slider_frequency.reset()
    slider_cov.reset()
    slider_mean.reset()
    plot_filtered.set_visible(False)

def update_plot():
    global checked_filtered, checked
    plot.set_ydata(y + noise if checked else y)
    plot_filtered.set_ydata(filtered)
    plot_filtered.set_visible(checked_filtered and checked)
    fig.canvas.draw_idle()
    fig.legend()

def update_filtered(label):
    global filtered, checked_filtered
    checked_filtered = not checked_filtered
    filtered = pd.Series(y + noise).rolling(8).mean()
    update_plot()


slider_amplitude.on_changed(update_harmonic)
slider_frequency.on_changed(update_harmonic)
slider_mean.on_changed(update_noise)
slider_cov.on_changed(update_noise)
check_noise.on_clicked(update_checkbox)
check_filtered.on_clicked(update_filtered)
button.on_clicked(reset)

plt.show()