from PySide import QtGui
from control_panel import ControlPanel
from input_select_widget import InputSelectWidget

class SwitcherControlPanel(ControlPanel):
	def __init__(self, device, parent):
		super(SwitcherControlPanel, self).__init__(device, parent)
		self.init_ui()

	def init_ui(self):
		hbox = QtGui.QHBoxLayout()

		input_selectors_labels_vbox = QtGui.QVBoxLayout()
		input_selectors_labels_vbox.addWidget(QtGui.QLabel("Program"))
		input_selectors_labels_vbox.addWidget(QtGui.QLabel("Preview"))

		input_selectors_vbox = QtGui.QVBoxLayout()
		self.program_select = InputSelectWidget(4)
		self.preview_select = InputSelectWidget(4)
		input_selectors_vbox.addWidget(self.program_select)
		input_selectors_vbox.addWidget(self.preview_select)
		self.program_select.setPressed(self.device.program_active_id.get_value())
		self.program_select.clicked.connect(self.change_program)
		self.preview_select.setPressed(self.device.preview_active_id.get_value())
		self.preview_select.clicked.connect(self.change_preview)

		takeButton = QtGui.QPushButton("Take")
		takeButton.clicked.connect(self.take)

		self.tbar = QtGui.QSlider()
		self.tbar.setTracking(True)
		self.tbar.setRange(0, 100)
		self.tbar.setValue(self.device.opacity.get_value()*100)
		self.device.opacity.changed.connect(self.opacity_changed)
		self.tbar.valueChanged.connect(self.change_opacity)

		hbox.addLayout(input_selectors_labels_vbox)
		hbox.addLayout(input_selectors_vbox)
		hbox.addWidget(self.tbar)
		hbox.addWidget(takeButton)
		self.setLayout(hbox)

		self.device.program_active_id.changed.connect(self.program_active_id_changed)
		self.device.preview_active_id.changed.connect(self.preview_active_id_changed)

	def take(self):
		self.device.take()

	def program_active_id_changed(self, program_active_id):
		self.program_select.setPressed(program_active_id)

	def preview_active_id_changed(self, preview_active_id):
		self.preview_select.setPressed(preview_active_id)

	def change_program(self, program_id):
		self.device.take(program_id)

	def change_preview(self, preview_id):
		self.device.preview(preview_id)

	def opacity_changed(self, opacity):
		self.tbar.setValue(opacity*100)

	def change_opacity(self, value):
		self.device.fade(value / 100.0)
