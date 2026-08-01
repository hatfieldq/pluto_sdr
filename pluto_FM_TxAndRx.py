#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
import sip



class pluto_FM_TxAndRx(gr.top_block, Qt.QWidget):

    def __init__(self, device='default'):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "pluto_FM_TxAndRx")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Parameters
        ##################################################
        self.device = device

        ##################################################
        # Variables
        ##################################################
        self.tx_enable = tx_enable = 0
        self.rx_enable = rx_enable = 1
        self.variable_0 = variable_0 = 0
        self.tx_tuning = tx_tuning = int(99.9e6)
        self.tx_samp_rate = tx_samp_rate = 48000
        self.tx_check = tx_check = tx_enable
        self.tuning = tuning = int(101.9e6)
        self.samp_rate = samp_rate = int(2.048e6)
        self.rx_check = rx_check = rx_enable
        self.rf_decim = rf_decim = 32
        self.pluto_samp_rate = pluto_samp_rate = 2400000
        self.interp_0 = interp_0 = 5
        self.interp = interp = 3
        self.deviation = deviation = 75000
        self.decim = decim = 1
        self.bandwidth = bandwidth = 200000
        self.audio_decim = audio_decim = 4
        self.attenuation = attenuation = 88

        ##################################################
        # Blocks
        ##################################################

        self._tx_tuning_range = qtgui.Range(int(81.1e6), int(107.9e6), int(0.1e6), int(99.9e6), 200)
        self._tx_tuning_win = qtgui.RangeWidget(self._tx_tuning_range, self.set_tx_tuning, "Tx Station Frequency", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tx_tuning_win)
        _tx_check_check_box = Qt.QCheckBox("Start Transmitting")
        self._tx_check_choices = {True: 1, False: 0}
        self._tx_check_choices_inv = dict((v,k) for k,v in self._tx_check_choices.items())
        self._tx_check_callback = lambda i: Qt.QMetaObject.invokeMethod(_tx_check_check_box, "setChecked", Qt.Q_ARG("bool", self._tx_check_choices_inv[i]))
        self._tx_check_callback(self.tx_check)
        _tx_check_check_box.stateChanged.connect(lambda i: self.set_tx_check(self._tx_check_choices[bool(i)]))
        self.top_layout.addWidget(_tx_check_check_box)
        self._tuning_range = qtgui.Range(int(81.1e6), int(107.9e6), int(0.1e6), int(101.9e6), 200)
        self._tuning_win = qtgui.RangeWidget(self._tuning_range, self.set_tuning, "Station Frequency", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tuning_win)
        _rx_check_check_box = Qt.QCheckBox("Receive and Listen")
        self._rx_check_choices = {True: 1, False: 0}
        self._rx_check_choices_inv = dict((v,k) for k,v in self._rx_check_choices.items())
        self._rx_check_callback = lambda i: Qt.QMetaObject.invokeMethod(_rx_check_check_box, "setChecked", Qt.Q_ARG("bool", self._rx_check_choices_inv[i]))
        self._rx_check_callback(self.rx_check)
        _rx_check_check_box.stateChanged.connect(lambda i: self.set_rx_check(self._rx_check_choices[bool(i)]))
        self.top_layout.addWidget(_rx_check_check_box)
        self._attenuation_range = qtgui.Range(0, 89, 1, 88, 200)
        self._attenuation_win = qtgui.RangeWidget(self._attenuation_range, self.set_attenuation, "Attentuation Changer", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._attenuation_win)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=interp_0,
                decimation=decim,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=interp,
                decimation=rf_decim,
                taps=[],
                fractional_bw=0)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            tuning, #fc
            samp_rate, #bw
            "Receive Signal", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            tx_samp_rate, #bw
            "Transmitted Signal", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                tx_samp_rate,
                15000,
                3000,
                window.WIN_HAMMING,
                6.76))
        self.iio_pluto_source_0 = iio.fmcomms2_source_fc32('' if '' else iio.get_pluto_uri(), [True, True], 32768)
        self.iio_pluto_source_0.set_len_tag_key('packet_len')
        self.iio_pluto_source_0.set_frequency(tuning)
        self.iio_pluto_source_0.set_samplerate(samp_rate)
        self.iio_pluto_source_0.set_gain_mode(0, 'slow_attack')
        self.iio_pluto_source_0.set_gain(0, 64)
        self.iio_pluto_source_0.set_quadrature(True)
        self.iio_pluto_source_0.set_rfdc(True)
        self.iio_pluto_source_0.set_bbdc(True)
        self.iio_pluto_source_0.set_filter_params('Auto', '', 0, 0)
        self.iio_pluto_sink_0 = iio.fmcomms2_sink_fc32('ip:192.168.2.1' if 'ip:192.168.2.1' else iio.get_pluto_uri(), [True, True], 32768, False)
        self.iio_pluto_sink_0.set_len_tag_key('')
        self.iio_pluto_sink_0.set_bandwidth(bandwidth)
        self.iio_pluto_sink_0.set_frequency(int(tx_tuning))
        self.iio_pluto_sink_0.set_samplerate(pluto_samp_rate)
        self.iio_pluto_sink_0.set_attenuation(0, attenuation)
        self.iio_pluto_sink_0.set_filter_params('Auto', '', 0, 0)
        self.blocks_selector_1 = blocks.selector(gr.sizeof_float*1,0,rx_check)
        self.blocks_selector_1.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,tx_check,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.audio_source_0 = audio.source(tx_samp_rate, "pipewire", True)
        self.audio_sink_0 = audio.sink(48000, device, True)
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=tx_samp_rate,
        	quad_rate=(tx_samp_rate  * 10),
        	tau=(75e-6),
        	max_dev=75e3,
        	fh=(-1.0),
        )
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=192e3,
        	audio_decimation=audio_decim,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.blocks_selector_1, 0))
        self.connect((self.analog_wfm_tx_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.audio_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_selector_1, 1), (self.audio_sink_0, 0))
        self.connect((self.blocks_selector_1, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_tx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_selector_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pluto_FM_TxAndRx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_device(self):
        return self.device

    def set_device(self, device):
        self.device = device

    def get_tx_enable(self):
        return self.tx_enable

    def set_tx_enable(self, tx_enable):
        self.tx_enable = tx_enable
        self.set_tx_check(self.tx_enable)

    def get_rx_enable(self):
        return self.rx_enable

    def set_rx_enable(self, rx_enable):
        self.rx_enable = rx_enable
        self.set_rx_check(self.rx_enable)

    def get_variable_0(self):
        return self.variable_0

    def set_variable_0(self, variable_0):
        self.variable_0 = variable_0

    def get_tx_tuning(self):
        return self.tx_tuning

    def set_tx_tuning(self, tx_tuning):
        self.tx_tuning = tx_tuning
        self.iio_pluto_sink_0.set_frequency(int(self.tx_tuning))

    def get_tx_samp_rate(self):
        return self.tx_samp_rate

    def set_tx_samp_rate(self, tx_samp_rate):
        self.tx_samp_rate = tx_samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.tx_samp_rate, 15000, 3000, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.tx_samp_rate)

    def get_tx_check(self):
        return self.tx_check

    def set_tx_check(self, tx_check):
        self.tx_check = tx_check
        self._tx_check_callback(self.tx_check)
        self.blocks_selector_0.set_input_index(self.tx_check)

    def get_tuning(self):
        return self.tuning

    def set_tuning(self, tuning):
        self.tuning = tuning
        self.iio_pluto_source_0.set_frequency(self.tuning)
        self.qtgui_sink_x_0.set_frequency_range(self.tuning, self.samp_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.iio_pluto_source_0.set_samplerate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(self.tuning, self.samp_rate)

    def get_rx_check(self):
        return self.rx_check

    def set_rx_check(self, rx_check):
        self.rx_check = rx_check
        self._rx_check_callback(self.rx_check)
        self.blocks_selector_1.set_output_index(self.rx_check)

    def get_rf_decim(self):
        return self.rf_decim

    def set_rf_decim(self, rf_decim):
        self.rf_decim = rf_decim

    def get_pluto_samp_rate(self):
        return self.pluto_samp_rate

    def set_pluto_samp_rate(self, pluto_samp_rate):
        self.pluto_samp_rate = pluto_samp_rate
        self.iio_pluto_sink_0.set_samplerate(self.pluto_samp_rate)

    def get_interp_0(self):
        return self.interp_0

    def set_interp_0(self, interp_0):
        self.interp_0 = interp_0

    def get_interp(self):
        return self.interp

    def set_interp(self, interp):
        self.interp = interp

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.iio_pluto_sink_0.set_bandwidth(self.bandwidth)

    def get_audio_decim(self):
        return self.audio_decim

    def set_audio_decim(self, audio_decim):
        self.audio_decim = audio_decim

    def get_attenuation(self):
        return self.attenuation

    def set_attenuation(self, attenuation):
        self.attenuation = attenuation
        self.iio_pluto_sink_0.set_attenuation(0,self.attenuation)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--device", dest="device", type=str, default='default',
        help="Set Device Name [default=%(default)r]")
    return parser


def main(top_block_cls=pluto_FM_TxAndRx, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(device=options.device)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
