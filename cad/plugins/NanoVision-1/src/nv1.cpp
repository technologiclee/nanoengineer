// Copyright 2007 Nanorex, Inc.  See LICENSE file for details.

#include "nv1.h"


/* CONSTRUCTOR */
nv1::nv1(NXEntityManager* entityManager, LogHandlerWidget* logHandlerWidget)
: QMainWindow() {
    this->entityManager = entityManager;
    
    setWindowIcon(QPixmap(":/Icons/eye-icon.png"));
    setWindowTitle(tr("NanoVision-1"));
    
    mainWindowTabs = new MainWindowTabWidget(this);
    setCentralWidget(mainWindowTabs);	
    
    resultsWindow = new ResultsWindow(entityManager, this);
    mainWindowTabs->vboxLayout->removeWidget(mainWindowTabs->widget);
    delete mainWindowTabs->widget;
    mainWindowTabs->vboxLayout->addWidget(resultsWindow);
    // resultsWindow->hide();
    
    createActions();
    createMenus();
    createToolBars();
    updateMenus();
    createStatusBar();
    
    readSettings();
    
    // Setup log dock widget
    QDockWidget* dock = new QDockWidget(tr("Log"), this);
    dock->setAllowedAreas(Qt::BottomDockWidgetArea);
    dock->setWidget(logHandlerWidget);
    addDockWidget(Qt::BottomDockWidgetArea, dock);
    
    fileName.clear();
}


/* DESTRUCTOR */
nv1::~nv1() {
}


/* FUNCTION: processCommandLine */
void nv1::processCommandLine(int argc, char *argv[]) {
    
	string filename, processType, processInit;
    NXCommandLine commandLine;
    if ((commandLine.SplitLine(argc, argv) > 0) &&
        (commandLine.HasSwitch("-f"))) {
		filename = commandLine.GetArgument("-f", 0);
		if (commandLine.GetArgumentCount("-p") == 2) {
			processType = commandLine.GetArgument("-p", 0);
			processInit = commandLine.GetArgument("-p", 1);
		}
		
	} else {
		checkForActiveJobs(filename, processType, processInit);
	}

	if (filename != "")
		loadFile(filename, processType, processInit);
}


/* FUNCTION: loadFile */
void nv1::loadFile(const string& filename, const string& processType,
				   const string& processInit) {
				
	QString message = tr("Opening file: %1").arg(filename.c_str());
	NXLOG_INFO("nv1", qPrintable(message));
	
	if (resultsWindow->loadFile(filename.c_str())) {
		statusBar()->showMessage(tr("File loaded"), 2000);
		resultsWindow->show();
	
		// Start job monitor
		JobMonitor* jobMonitor = 0;
		if ((processType != "") && (processInit != "")) {
			message =
			tr("Setting up job management with job handle info: %1 %2")
				.arg(processType.c_str()).arg(processInit.c_str());
			NXLOG_INFO("nv1", qPrintable(message));
			if (processType == "GMX") {
				jobMonitor = new GROMACS_JobMonitor(processInit.c_str());
			}
			if (jobMonitor != 0) {
				connect(jobMonitor,
						SIGNAL(startedMonitoring(const QString&,
												 const QString&,
												 const QString&)),
						this,
						SLOT(addMonitoredJob(const QString&,
											 const QString&,
											 const QString&)));
				connect(jobMonitor, SIGNAL(jobFinished(const QString&)),
						this, SLOT(removeMonitoredJob(const QString&)));
				connect(jobMonitor, SIGNAL(jobAborted(const QString&)),
						this, SLOT(removeMonitoredJob(const QString&)));
				jobMonitors[processInit.c_str()] = jobMonitor;
				jobMonitor->start();
			}
		}
	}
}


/* FUNCTION: closeEvent */
void nv1::closeEvent(QCloseEvent *event) {
    if (resultsWindow != 0)
        delete resultsWindow;
    
    writeSettings();
    event->accept();
}


/* FUNCTION: open */
void nv1::open() {
    QString importFileTypes = entityManager->getImportFileTypes().c_str();
    QString newFileName =
        QFileDialog::getOpenFileName(this, tr("Open File"), "",
                                     importFileTypes + ";;All Types (*)");
    if (!newFileName.isEmpty()) {
        // prevent re-opening of an opened file
        if(newFileName.compare(fileName) == 0) {
            QMessageBox::information(this, tr("Error"),tr("File already open"));
            return;
        }
        // close a previously opened file, if there is one such
        if(!fileName.isEmpty())
            close();
        if (resultsWindow->loadFile(newFileName)) {
            fileName = newFileName;
            statusBar()->showMessage(tr("File loaded"), 2000);
            QFileInfo fileInfo(fileName);
            setWindowTitle(tr("NanoVision-1: ") + fileInfo.fileName());
            resultsWindow->show();
        }
    }
}


/* FUNCTION: close */
void nv1::close() {
    resultsWindow->closeFile();
    setWindowTitle(tr("NanoVision-1"));
    fileName.clear();
}


/* FUNCTION: about */
void nv1::about() {
    QMessageBox::about(this,
                       tr("About NanoVision-1"),
                       tr("Nanorex NanoVision-1 0.1.0\n"
                          "Copyright 2008 Nanorex, Inc.\n"
                          "See LICENSE file for details."));
}


/* FUNCTION: updateMenus */
void nv1::updateMenus() {
    bool hasResultsWindow = resultsWindow->isVisible();
    windowCloseAction->setEnabled(hasResultsWindow);
    windowCloseAllAction->setEnabled(hasResultsWindow);
    windowTileAction->setEnabled(hasResultsWindow);
    windowCascadeAction->setEnabled(hasResultsWindow);
    windowArrangeAction->setEnabled(hasResultsWindow);
    windowNextAction->setEnabled(hasResultsWindow);
    windowPreviousAction->setEnabled(hasResultsWindow);
    windowSeparatorAction->setVisible(hasResultsWindow);
}


/* FUNCTION: updateWindowMenu */
void nv1::updateWindowMenu() {
    windowMenu->clear();
    windowMenu->addAction(windowCloseAction);
    windowMenu->addAction(windowCloseAllAction);
    windowMenu->addSeparator();
    windowMenu->addAction(windowTileAction);
    windowMenu->addAction(windowCascadeAction);
    windowMenu->addAction(windowArrangeAction);
    windowMenu->addSeparator();
    windowMenu->addAction(windowNextAction);
    windowMenu->addAction(windowPreviousAction);
    windowMenu->addAction(windowSeparatorAction);
    
    QList<QWidget*> windows = resultsWindow->workspace->windowList();
    windowSeparatorAction->setVisible(!windows.isEmpty());
    
    for (int index = 0; index < windows.size(); ++index) {
        DataWindow* window = qobject_cast<DataWindow*>(windows.at(index));
        
        QString windowTitle;
        if (window == 0) {
            windowTitle = "--";
            NXLOG_DEBUG("nv1::updateWindowMenu()", "window is null");
        } else
            windowTitle = window->windowTitle();
        
        QString text;
        if (index < 9)
            text = tr("&%1 %2").arg(index + 1).arg(windowTitle);
        else
            text = tr("%1 %2").arg(index + 1).arg(windowTitle);
        
        QAction *action  = windowMenu->addAction(text);
        action->setCheckable(true);
        action->setChecked(window == resultsWindow->activeDataWindow());
        connect(action, SIGNAL(triggered()), resultsWindow->windowMapper, 
                SLOT(map()));
        resultsWindow->windowMapper->setMapping(action, window);
    }
}


/* FUNCTION: createActions */
void nv1::createActions() {
    
    openAction =
        new QAction(QIcon(":/Icons/File/Open.png"), tr("&Open..."), this);
    openAction->setShortcut(tr("Ctrl+O"));
    openAction->setStatusTip(tr("Open an existing file"));
    connect(openAction, SIGNAL(triggered()), this, SLOT(open()));
    
    closeAction =
        new QAction(QIcon(":/Icons/File/Close.png"), tr("&Close"), this);
    closeAction->setShortcut(tr("Ctrl+W"));
    closeAction->setStatusTip(tr("Close and open file"));
    connect(closeAction, SIGNAL(triggered()), this, SLOT(close()));
    
    exitAction = new QAction(tr("E&xit"), this);
    exitAction->setShortcut(tr("Ctrl+Q"));
    exitAction->setStatusTip(tr("Exit NanoVision-1"));
    connect(exitAction, SIGNAL(triggered()), qApp, SLOT(closeAllWindows()));
    
    windowCloseAction = new QAction(tr("Cl&ose"), this);
    windowCloseAction->setShortcut(tr("Ctrl+F4"));
    windowCloseAction->setStatusTip(tr("Close the active window"));
    connect(windowCloseAction, SIGNAL(triggered()),
            resultsWindow->workspace, SLOT(closeActiveWindow()));
    
    windowCloseAllAction = new QAction(tr("Close &All"), this);
    windowCloseAllAction->setStatusTip(tr("Close all the windows"));
    connect(windowCloseAllAction, SIGNAL(triggered()),
            resultsWindow->workspace, SLOT(closeAllWindows()));
    
    windowTileAction = new QAction(tr("&Tile"), this);
    windowTileAction->setStatusTip(tr("Tile the windows"));
    connect(windowTileAction, SIGNAL(triggered()), resultsWindow->workspace,
            SLOT(tile()));
    
    windowCascadeAction = new QAction(tr("&Cascade"), this);
    windowCascadeAction->setStatusTip(tr("Cascade the windows"));
    connect(windowCascadeAction, SIGNAL(triggered()), resultsWindow->workspace, 
            SLOT(cascade()));
    
    windowArrangeAction = new QAction(tr("Arrange &icons"), this);
    windowArrangeAction->setStatusTip(tr("Arrange the icons"));
    connect(windowArrangeAction, SIGNAL(triggered()), resultsWindow->workspace, 
            SLOT(arrangeIcons()));
    
    windowNextAction = new QAction(tr("Ne&xt"), this);
    windowNextAction->setStatusTip(tr("Move the focus to the next window"));
    connect(windowNextAction, SIGNAL(triggered()),
            resultsWindow->workspace, SLOT(activateNextWindow()));
    
    windowPreviousAction = new QAction(tr("Pre&vious"), this);
    windowPreviousAction->setStatusTip(tr("Move the focus to the previous "
                                          "window"));
    connect(windowPreviousAction, SIGNAL(triggered()),
            resultsWindow->workspace, SLOT(activatePreviousWindow()));
    
    windowSeparatorAction = new QAction(this);
    windowSeparatorAction->setSeparator(true);
    
    aboutAction = new QAction(tr("&About"), this);
    aboutAction->setStatusTip(tr("Show NanoVision-1's About box"));
    connect(aboutAction, SIGNAL(triggered()), this, SLOT(about()));
}


/* FUNCTION: createMenus */
void nv1::createMenus() {
    fileMenu = menuBar()->addMenu(tr("&File"));
    fileMenu->addAction(openAction);
    fileMenu->addAction(closeAction);
    fileMenu->addSeparator();
    fileMenu->addAction(exitAction);
    
    processMenu = menuBar()->addMenu(tr("&Job Management"));
    
    windowMenu = menuBar()->addMenu(tr("&Window"));
    updateWindowMenu();
    connect(windowMenu, SIGNAL(aboutToShow()), this, SLOT(updateWindowMenu()));
    
    menuBar()->addSeparator();
    
    helpMenu = menuBar()->addMenu(tr("&Help"));
    helpMenu->addAction(aboutAction);
}


/* FUNCTION: createToolBars */
void nv1::createToolBars() {
    fileToolBar = addToolBar(tr("File"));
    fileToolBar->addAction(openAction);
    fileToolBar->addAction(closeAction);
}


/* FUNCTION: createStatusBar */
void nv1::createStatusBar() {
    statusBar()->showMessage(tr("Ready"));
}


/* FUNCTION: readSettings */
void nv1::readSettings() {
    QSettings settings(QSettings::IniFormat, QSettings::UserScope,
                       "Nanorex", "NanoVision-1");
    QPoint pos = settings.value("Layout/Position", QPoint(200, 200)).toPoint();
    QSize size = settings.value("Layout/Size", QSize(400, 400)).toSize();
    resize(size);
    move(pos);
}


/* FUNCTION: writeSettings */
void nv1::writeSettings() {
    QSettings settings(QSettings::IniFormat, QSettings::UserScope,
                       "Nanorex", "NanoVision-1");
    settings.setValue("Layout/Position", pos());
    settings.setValue("Layout/Size", size());
}


/* FUNCTION: addMonitoredJob */
void nv1::addMonitoredJob(const QString& processType, const QString& id,
						  const QString& title) {
    QString actionTitle = tr("Abort %1").arg(title);
    abortJobAction =
        new QAction(QIcon(":/Icons/File/Open.png"), actionTitle, this);
    abortJobAction->setStatusTip(tr("Abort a running job"));
    
    QSignalMapper* signalMapper = new QSignalMapper(this);
    connect(abortJobAction, SIGNAL(triggered()), signalMapper, SLOT(map()));
    signalMapper->setMapping(abortJobAction, id);
    connect(signalMapper, SIGNAL(mapped(const QString &)),
            this, SLOT(abortJob(const QString&)));
    
	// Write job details to a file for later resumption of monitoring
	QSettings settings(QSettings::IniFormat, QSettings::UserScope,
					   "Nanorex", "NanoVision-1");
	QFileInfo fileInfo(settings.fileName());
	QDir dir(fileInfo.absolutePath().append("/Jobs"));
	if (!dir.exists()) {
		dir.cdUp();
		dir.mkdir("Jobs");
	}
	QString jobFilename =
		dir.absolutePath().append("/Jobs/").append(processType)
			.append("_").append(id);
	QFile jobFile(jobFilename);
	if (jobFile.open(QIODevice::WriteOnly)) {
		jobFile.write(qPrintable(resultsWindow->currentFile()));
		jobFile.close();
	}
	// TODO: catch/emit errors
	
    processMenu->addAction(abortJobAction);
}


/* FUNCTION: removeMonitoredJob */
void nv1::removeMonitoredJob(const QString& id) {
    processMenu->removeAction(abortJobAction);
    delete abortJobAction;
    
    JobMonitor* jobMonitor = jobMonitors[id];
    if (jobMonitor->isFinished())
        delete jobMonitor;
    else
        NXLOG_INFO("nv1::removeMonitoredJob",
                   "jobMonitor wasn't finished - MEMORY LEAK");
}


/* FUNCTION: abortJob */
void nv1::abortJob(const QString& id) {
    jobMonitors[id]->abortJob();
}


/* FUNCTION: checkForActiveJobs
 *
 * Check if there are any active jobs and ask the user which, if any to
 * connect to. Populate the given variables.
 */
void nv1::checkForActiveJobs(string& filename, string& processType,
							 string& processInit) {

	// Get a list of active jobs
	QSettings settings(QSettings::IniFormat, QSettings::UserScope,
					   "Nanorex", "NanoVision-1");
	QFileInfo fileInfo(settings.fileName());
	QDir dir(fileInfo.absolutePath().append("/Jobs"));
	if (!dir.exists()) {
		dir.cdUp();
		dir.mkdir("Jobs");
	}
	bool jobActive;
	QStringList activeJobs;
	QStringList fileList = dir.entryList(QDir::Files);
	QStringList::const_iterator constIterator;
	for (constIterator = fileList.constBegin();
		 constIterator != fileList.constEnd(); ++constIterator) {
		jobActive = false;
		if ((*constIterator).startsWith("GMX")) {
			QString pid = (*constIterator).mid(4);
			jobActive = GROMACS_JobMonitor::CheckJobActive(pid);
		}
		if (jobActive)
			activeJobs.append(*constIterator);
		else
			; // Delete job file
	}
	
	// Show a selector dialog
	int jobSelectionResult = QDialog::Rejected;
	QString selectedJob;
	if (!activeJobs.empty()) {
		JobSelectorDialog jobSelectorDialog;
		jobSelectorDialog.addActiveJobs(activeJobs);
		jobSelectorDialog.exec();
		jobSelectionResult = jobSelectorDialog.result();
		if (jobSelectionResult == QDialog::Accepted)
			selectedJob = jobSelectorDialog.getSelection();
	}
	
	if (jobSelectionResult == QDialog::Accepted) {
		
		// TODO: make this handle more than just "GMX_<pid>"
		processType = "GMX";
		processInit = qPrintable(selectedJob.mid(4));
		
		QString jobFilename = dir.absolutePath().append("/").append(selectedJob);
		QFile jobFile(jobFilename);
		if (jobFile.open(QIODevice::ReadOnly)) {
			char buffer[512];
			if (jobFile.readLine(buffer, sizeof(buffer)) != -1) {
				filename = buffer;
			}
			jobFile.close();
		}
	}
}

