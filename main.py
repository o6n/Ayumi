#!/usr/bin/python3
# -*- coding: utf-8 -*-
## ~/.local/bin/removestar -i main.py
import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import (QAction, QApplication, QCalendarWidget, QLineEdit, QMainWindow,
								QShortcut, QTabWidget, QToolBar)
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView
from PyQt5.QtGui import QColor, QIcon, QKeySequence, QPalette

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.addressBar()
		self.toolsBar()
		self.showMaximized()

		##
		self.tabs = QTabWidget()
		self.tabs.setMovable(True)
		self.tabs.setTabsClosable(True)
		self.tabs.tabCloseRequested.connect(self.closeTab)

		self.openTab()
		self.setCentralWidget(self.tabs)

		QShortcut(QKeySequence("Ctrl+H"), self, self.goToHome)
		QShortcut(QKeySequence("Ctrl+T"), self, self.openTab)

	def addressBar(self):
		self.navigationbar = QToolBar("Navigation Bar") #create a navigation bar
		self.addToolBar(self.navigationbar) #add to navBar

		self.homeIcon = QIcon.fromTheme("go-home-symbolic")
		self.homeBtn = QAction(self.homeIcon, "Home", self)
		self.homeBtn.triggered.connect(self.goToHome)
		self.homeBtn.setShortcut(QKeySequence("Ctrl+H"))
		self.navigationbar.addAction(self.homeBtn)

		self.backIcon = QIcon.fromTheme("draw-arrow-back")
		self.backBtn = QAction(self.backIcon, "Back", self)
		self.backBtn.triggered.connect(lambda: self.tabs.currentWidget().back())
		self.navigationbar.addAction(self.backBtn)

		self.forwardIcon = QIcon.fromTheme("draw-arrow-forward")
		self.forwardBtn = QAction(self.forwardIcon, "Forward", self)
		self.forwardBtn.triggered.connect(lambda: self.tabs.currentWidget().forward())
		self.navigationbar.addAction(self.forwardBtn)

		self.reloadIcon = QIcon.fromTheme("system-reboot")
		self.reloadBtn = QAction(self.reloadIcon, "Reload", self)
		self.reloadBtn.triggered.connect(lambda: self.tabs.currentWidget().reload())
		self.navigationbar.addAction(self.reloadBtn)

		self.stopIcon = QIcon.fromTheme("process-stop")
		self.stopBtn = QAction(self.stopIcon, "Stop", self)
		self.stopBtn.triggered.connect(lambda: self.tabs.currentWidget().stop())
		self.navigationbar.addAction(self.stopBtn)

		self.tabIcon = QIcon.fromTheme("tab-new")
		self.tabBtn = QAction(self.tabIcon, "Open Tab", self)
		self.tabBtn.triggered.connect(self.openTab)
		self.navigationbar.addAction(self.tabBtn)

		## SEARCH BAR
		self.searchbar = QLineEdit()
		self.searchbar.setClearButtonEnabled(True)
		self.searchbar.returnPressed.connect(self.goToSearch)
		self.navigationbar.addWidget(self.searchbar)

		self.searchIcon = QIcon.fromTheme("system-search")
		self.searchBtn = QAction(self.searchIcon, "Search", self)
		self.searchBtn.triggered.connect(self.goToSearch)
		self.navigationbar.addAction(self.searchBtn)

	def toolsBar(self):
		self.toolbar = QToolBar("Navigation Bar") #create a navigation bar
		self.addToolBar(self.toolbar) #add to navBar

		self.scriptsIcon = QIcon.fromTheme("text-x-javascript")
		self.scriptsBtn = QAction(self.scriptsIcon, "Scripts Block", self)
		self.scriptsBtn.setCheckable(True) ## setting checkable to true
		self.scriptsBtn.triggered.connect(self.scriptsBlock)
		self.toolbar.addAction(self.scriptsBtn)

		self.imagesIcon = QIcon.fromTheme("image-x-generic")
		self.imagesBtn = QAction(self.imagesIcon, "Images Block", self)
		self.imagesBtn.setCheckable(True) ## setting checkable to true
		self.imagesBtn.triggered.connect(self.imagesBlock)
		self.toolbar.addAction(self.imagesBtn)

	def goToHome(self):
		self.tabs.currentWidget().setUrl(QUrl("https://github.com/o6n"))

	def goToSearch(self):
		url_string = self.searchbar.text().strip()
		if '.' in url_string:
			self.load_url_string(url_string)
		else:
			self.load_url(url_string)

	def load_url_string(self, url_string):
		url = QUrl.fromUserInput(url_string)
		if (url.isValid()):
			self.load_url(url)
		else:
			url = 'https://www.google.com/search?q=' + url_string
			self.tabs.currentWidget().page().setUrl(QUrl(url))

	def load_url(self, url):
		try:
			if url.isValid():
				self.tabs.currentWidget().page().setUrl(url)
		except:
			url = 'https://www.google.com/search?q=' + url
			self.tabs.currentWidget().page().setUrl(QUrl(url))

	def openTab(self):
		self.browser = QWebEngineView()
		self.browser.setUrl(QUrl("https://www.google.com/"))
		i = self.tabs.addTab(self.browser, "...")
		self.tabs.setCurrentIndex(i)
		## set a lambda as the slot for the urlChanged signal, accepting the qurl parameter that is sent by this signal.
		self.browser.urlChanged.connect(lambda qurl, browser=self.browser: self.updateSearchBar(qurl, browser))
		self.browser.loadFinished.connect(lambda _, i=i, browser=self.browser: self.tabs.setTabText(i, self.browser.page().title()))

		## Default browser settings
		self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
		self.browser.settings().setAttribute(QWebEngineSettings.AutoLoadImages, True)

		## Show link url's in status bar
		self.browser.page().linkHovered.connect(self.displayLink)

	def closeTab(self, i):
		if self.tabs.count() < 2:
			return
		self.tabs.removeTab(i)

	def updateSearchBar(self, q, browser=None):
		if self.browser != self.tabs.currentWidget():
			return ## If this signal is not from the current tab, ignore
		self.searchbar.setText(q.toString())
		self.searchbar.setCursorPosition(0)

	def displayLink(self, link):
		self.statusBar().showMessage(link)

	## BLOCK
	def scriptsBlock(self):
		if self.scriptsBtn.isChecked():
			self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, False)
	def imagesBlock(self):
		if self.imagesBtn.isChecked():
			self.browser.settings().setAttribute(QWebEngineSettings.AutoLoadImages, False)

def main():
	app = QApplication([])
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
