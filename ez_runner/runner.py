# https://www.pythonguis.com/tutorials/multithreading-pyside6-applications-qthreadpool/
import sys

try:
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
except:
    try:
        from PySide2.QtCore import *
        from PySide2.QtWidgets import *
        from PySide2.QtGui import *
    except:
        raise ModuleNotFoundError("ez_runner needs either PySide2 or PySide6 to run")


class Communicator(QObject):
    starting = Signal()
    done = Signal()
    result = Signal(object)
    error = Signal(list)
    progress = Signal(int)


class Runner(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.communicator = Communicator()

        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.kwargs["progress_callback"] = self.communicator.progress

    def run(self):
        self.communicator.starting.emit()
        try:
            result = self.func(*self.args, **self.kwargs)
        except:
            exception_type, value = sys.exc_info()[:2]
            self.communicator.error.emit([exception_type, value])
        else:
            self.communicator.result.emit(result)
        finally:
            self.communicator.done.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    def say_something(something, **kwargs):
        print(f"{something}")
        return f"I have said: {something}"

    def starting():
        print("I have begun working")

    def ended():
        print("I have ended")

    def error(err):
        print(err[0])
        print(err[1])

    def show_result(result):
        print(result)

    threadpool = QThreadPool()
    runner = Runner(say_something, "hello there")

    runner.communicator.starting.connect(starting)
    runner.communicator.done.connect(ended)
    runner.communicator.error.connect(error)
    runner.communicator.result.connect(show_result)

    threadpool.start(runner)
    app.exec_()
