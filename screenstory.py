import sys, os
from datetime import datetime
from PyQt4 import QtGui, uic, QtCore


form_class, base_class = uic.loadUiType("screenstory.ui")


class ScreenstoryDialog(base_class, form_class):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        # Set up the user interface from Designer.
        self.setupUi(self)
        self.show()

        # get screen for capturing
        self.screen = QtGui.QApplication.desktop().winId()

        # snapshot path
        self.snapshot_path = "./snapshots"

        # setup time
        self.running = False
        self.timer = QtCore.QTimer()

        self.load_snapshots()

    def load_snapshots(self):
        """
            Load existing snapshots and categorize them in the tree
        """
        for filename in sorted([f for f in os.listdir(self.snapshot_path) if f.endswith(".png")], reverse=True):
            try:
                # find existing branch
                branch = self.tree_files.findItems(filename[:10], QtCore.Qt.MatchExactly)[0]
            except:
                # create a new branch
                branch = QtGui.QTreeWidgetItem()
                branch.setText(0, filename[:10])
                self.tree_files.addTopLevelItem(branch)

            # add item to branch
            twi = QtGui.QTreeWidgetItem()
            twi.setIcon(0, QtGui.QIcon(QtGui.QPixmap(self.snapshot_path + "/%s" % filename).scaled(100,100, QtCore.Qt.KeepAspectRatio)))
            twi.setText(1, filename[:19])
            branch.addChild(twi)


    def snapshot(self):
        """
            Make a screenshot and save it, show item in tree
        """
        # make a snapshot and save it
        timestamp  = datetime.now()
        filename = "%s/%s.png" % (self.snapshot_path, timestamp.strftime("%Y.%m.%d.%H.%M.%S"))
        QtGui.QPixmap.grabWindow(self.screen).save(filename, 'png')

        # reschedule next snapshot?
        if self.running:
            self.timer.singleShot(int(self.txt_interval.value())*60000, self.snapshot)

        try:
            # find existing branch
            branch = self.tree_files.findItems(timestamp.strftime("%Y.%m.%d"), QtCore.Qt.MatchExactly)[0]
        except:
            # create new branch
            branch = QtGui.QTreeWidgetItem()
            branch.setText(0, "Today")

            self.tree_files.addTopLevelItem(branch)

        # add item to branch
        twi = QtGui.QTreeWidgetItem()
        twi.setIcon(0, QtGui.QIcon(QtGui.QPixmap(os.getcwd() + "/%s" % filename).scaled(100,100, QtCore.Qt.KeepAspectRatio)))
        twi.setText(1, timestamp.strftime("%Y.%m.%d.%H.%M.%S"))
        branch.insertChild(0, twi)


    def start(self):
        """
            Run if not running, stop if it does
        """
        if not self.running:
            print "start!"
            self.btn_start.setText("stop!")
            self.running = True
            self.snapshot()
        else:
            print "stop!"
            self.btn_start.setText("start!")
            self.running = False



# run app
app = QtGui.QApplication(sys.argv)
window = ScreenstoryDialog()
sys.exit(app.exec_())
