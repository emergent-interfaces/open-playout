from PySide import QtCore


class ObservableVariable(QtCore.QObject):
    changed = QtCore.Signal(object)

    def __init__(self, initial_value=None):
        super(ObservableVariable, self).__init__()
        self._value = initial_value

    def set_value(self, new_value):
        self._value = new_value
        self.changed.emit(new_value)

    def set_value_quietly(self, new_value):
        self._value = new_value

    def get_value(self):
        return self._value
