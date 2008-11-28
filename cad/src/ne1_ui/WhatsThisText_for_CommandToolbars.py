# Copyright 2004-2007 Nanorex, Inc.  See LICENSE file for details. 
"""
WhatsThisText_for_CommandToolbars.py

This file provides functions for setting the "What's This" text
for widgets (typically QActions) in the Command Toolbar.

@author: Mark
@version:$Id$
@copyright: 2004-2007 Nanorex, Inc.  See LICENSE file for details.
"""

# Try to keep this list in order (by appearance in Command Toolbar). --Mark

# Command Toolbar Menus (i.e. Build, Tools, Move and Simulation ######

def whatsThisTextForCommandToolbarBuildButton(button):
    """
    "What's This" text for the Build button (menu).
    """
    button.setWhatsThis(
        """<b>Build</b>
        <p>
        The NanoEngineer-1 <i>Build commands</i> for constructing structures 
        interactively.
        </p>""")
    return

def whatsThisTextForCommandToolbarInsertButton(button):
    """
    "What's This" text for the Insert button (menu).
    """
    button.setWhatsThis(
        """<b>Insert</b>
        <p>
        The NanoEngineer-1 <i>Insert commands</i> for inserting reference
        geometry, part files or other external structures into the current
        model.
        </p>""")
    return

def whatsThisTextForCommandToolbarToolsButton(button):
    """
    Menu of Build tools.
    """
    button.setWhatsThis(
        """<b>Tools</b>
        <p>
        This is a drop down Tool menu. Clicking on the Tool button will add
        these tools to the Command Toolbar.
        </p>""")
    return

def whatsThisTextForCommandToolbarMoveButton(button):
    """
    "What's This" text for the Move button (menu).
    """
    button.setWhatsThis(
        """<b>Move</b>
        <p>
       This is a drop down menu of Move commands. Clicking on the Move button
       will add these commands to the Command Toolbar.
        </p>""")
    return

def whatsThisTextForCommandToolbarSimulationButton(button):
    """
    "What's This" text for the Simulation button (menu).
    """
    button.setWhatsThis(
        """<b>Simulation</b>
        <p>
        This is a drop down menu containing Simulation modes (Run Dynamics
        and Play Movie). The menu also contains the associated simulation jigs.
        Clicking on the Simulation button will add these items to the Command
        Explorer
        </p>""")
    return

# Build command toolbars ####################

def whatsThisTextForAtomsCommandToolbar(commandToolbar):
    """
    "What's This" text for widgets in the Build Atoms Command Toolbar.
    
    @note: This is a placeholder function. Currenly, all the tooltip text is 
           defined in BuildAtoms_Command.py.
    """
    return

def whatsThisTextForProteinCommandToolbar(commandToolbar):
    """
    "What's This" text for the Build Protein Command Toolbar
    """
    commandToolbar.exitModeAction.setWhatsThis(
        """<b>Exit Protein</b>
        <p>
        Exits <b>Build Protein</b>.
        </p>""")
    
    commandToolbar.modelProteinAction.setWhatsThis(
        """<b>Model Protein</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildProtein/ModelProtein.png\"><br> 
        Enter protein modeling mode. Modeling options are displayed to the right
        in the flyout toolbar.
        </p>""")
    
    commandToolbar.simulateProteinAction.setWhatsThis(
        """<b>Simulate Protein with Rosetta</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildProtein/Simulate.png\"><br> 
        Enter protein simulation mode using Rosetta. Rosetta is a collection of
        computational tools for the prediction and design of protein structures 
        and protein-protein interactions. A subset of Rosetta simulation options
        are available in NanoEngineer-1, including:
        <lo>
        Option 1
        Option 2
        </lo>
        </p>
        <p><a href=Rosetta_for_NanoEngineer-1> 
        Click here for more information about Rosetta for NanoEngineer-1</a>
        </p>""")
    
    commandToolbar.buildPeptideAction.setWhatsThis(
        """<b>Insert Peptide</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildProtein/InsertPeptide.png\"><br> 
        Insert a peptide chain by clicking two endpoints 
        in the 3D graphics area. The user can also specify different
        conformation options (i.e. Alpha helix, Beta sheet, etc.) in the 
        property manager.
        </p>""")
    
    commandToolbar.editRotamersAction.setWhatsThis(
        """<b>Edit Rotamers</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildProtein/Rotamers.png\"><br> 
        Edit rotamers in a peptide chain.
        </p>""")
    
    commandToolbar.compareProteinsAction.setWhatsThis(
        """<b>Compare Proteins</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildProtein/Compare.png\"><br> 
        Select two protein structures and compare them visually.
        </p>""")
    
    commandToolbar.displayProteinStyleAction.setWhatsThis(
        """<b>Edit (Protein Display) Style</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildProtein/EditProteinDisplayStyle.png\"><br> 
        Edit the Protein Display Style settings used whenever the 
        <b>Global Display Style</b> is set to <b>Protein</b>.
        </p>""")
    
    commandToolbar.rosetta_fixedbb_design_Action.setWhatsThis(
        """<b>Fixed Backbone Protein Sequence Design</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildProtein/FixedBackbone.png\"><br> 
        Design an optimized fixed backbone protein sequence using Rosetta.
        </p>""")
    
    commandToolbar.rosetta_backrub_Action.setWhatsThis(
        """<b>Backrub Motion</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildProtein/Backrub.png\"><br> 
        Design an optimized backbone protein sequence using Rosetta 
        with backrub motion allowed.
        </p>""")
    
    commandToolbar.editResiduesAction.setWhatsThis(
        """<b>Edit Residues</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildProtein/Residues.png\"><br> 
        Provides an interface to edit residues so that Rosetta can predict
        the optimized sequence of an initial sequence (peptide chain).
        </p>""")
    
    commandToolbar.rosetta_score_Action.setWhatsThis(
        """<b>Compute Rosetta Score</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildProtein/Score.png\"><br> 
        Produce the Rosetta score, which is useful for predicting errors in a 
        peptide/protein structure. </p>
        <p>
        The Rosetta scoring function is an all-atom force field that focuses 
        on short-range interactions (i.e., van der Waals packing, hydrogen 
        bonding and desolvation) while neglecting long-range electrostatics. 
        </p>""")
    
    return


def whatsThisTextForDnaCommandToolbar(commandToolbar):
    """
    "What's This" text for the Build DNA Command Toolbar
    """
    commandToolbar.exitModeAction.setWhatsThis(
        """<b>Exit DNA</b>
        <p>
        Exits <b>Build DNA</b>.
        </p>""")
    
    commandToolbar.dnaDuplexAction.setWhatsThis(
        """<b>Insert DNA</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildDna/InsertDna.png\"><br>
        Insert a DNA duplex by clicking two endpoints in the graphics area.
        </p>""")
    
    commandToolbar.breakStrandAction.setWhatsThis(
        """<b>Break Strands</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildDna/BreakStrand.png\"><br>
        This command provides an interactive mode where the user can 
        break strands by clicking on a bond in a DNA strand. </p>
        <p>
        You can also join strands while in this command by dragging and 
        dropping strand arrow heads onto their strand conjugate 
        (i.e. 3' on to 5' and vice versa). </p>
        <p>
        <img source=\"ui/actions/Help/HotTip.png\"><br>
        <b>Hot Tip:</b> Changing the <b>Global display style</b> to <b>CPK</b>  
        results in faster interactive graphics while in this command.
        </p>""")
    
    commandToolbar.joinStrandsAction.setWhatsThis(
        """<b>Join Strands</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildDna/JoinStrands.png\"><br>
        This command provides an interactive mode where the user can
        join strands by dragging and dropping strand arrow heads onto their 
        strand conjugate (i.e. 3' on to 5' and vice versa). </p>
        <p>
        <img source=\"ui/actions/Help/HotTip.png\"><br>
        <b>Hot Tip:</b> Changing the <b>Global display style</b> to <b>CPK</b>  
        results in faster interactive graphics while in this command.
        </p>""")
    
    commandToolbar.convertDnaAction.setWhatsThis(
        """<b>Convert DNA </b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildDna/ConvertDna.png\"><br>
        Converts the selected DNA from PAM3 to PAM5 or PAM5 to PAM3. The only
        reason to convert to PAM5 is to get more accurate minimizations of DNA 
        nanostructures.</p>
        <p>
        Here is the protocol for producing more accurate minimizations:<br>
        1. Make sure the current model is saved.
        2. Select <b>File > Save As...</b> to save the model under a new name (i.e. <i>model_name</i>_minimized).<br>
        3. Select <b>Build > DNA > Convert</b> to convert the entire model from PAM3 to PAM5.<br>
        4. Select <b>Tools > Minimize Energy</b>.<br>
        5. In the Minimize Energy dialog, select <b>GROMACS with ND1 force field</b> as the Physics engine.<br>
        6. Click the <b>Minimize Energy</b> button.<br>
        7. After minimize completes, convert from PAM5 to PAM3.</p>
        <p>
        Next, visually inspect the model for structural distortions such as 
        puckering, warping, or other unwanted strained areas that will require 
        model changes to correct. Model changes should be made in a version
        of the model that hasn't been minimized. You can either click
        <b>Edit > Undo</b> or save this model and reopen the previous 
        version.</p>
        <p>
        <img source=\"ui/actions/Help/HotTip.png\"><br>
        <b>Hot Tip:</b> Changing the <b>Global display style</b> to <b>CPK</b> or 
        <b>DNA Cylinder</b> may make the model easier to visually inspect.</p>
        <p>
        <a href=PAM3_and_PAM5_Model_Descriptions>Click here for a technical 
        overview of the NanoEngineer-1 PAM3 and PAM5 reduced models.</a>
        </p>""")
    
    commandToolbar.orderDnaAction.setWhatsThis(
        """<b>Order DNA</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildDna/OrderDna.png\"><br>
        Produces a comma-separated value (.CSV) text file containing all  
        DNA strand sequences in the model.</p>
        <p>
        <img source=\"ui/actions/Help/HotTip.png\"><br>
        <b>Hot Tip:</b> This file can be used to order 
        oligos from suppliers of custom oligonucleotides such as 
        Integrated DNA Technologies and Gene Link.
        </p>""")
        
    commandToolbar.editDnaDisplayStyleAction.setWhatsThis(
        """<b>Edit (DNA Display) Style</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildDna/EditDnaDisplayStyle.png\"><br>
        Edit the DNA Display Style settings used whenever the <b>Global Display
        Style</b> is set to <b>DNA Cylinder</b>. These settings also apply
        to DNA strands and segments that have had their display style set
        to <b>DNA Cylinder</b>.
        </p>""")    
    
    commandToolbar.makeCrossoversAction.setWhatsThis(
        """<b>Make Crossovers</b>
        <p>
        <img source=\"ui/actions/Command Toolbar/BuildDna/MakeCrossovers.png\"><br>
        Creates crossovers interactively between two or more selected DNA 
        segments.</p>
        <p>
        To create crossovers, select the DNA segments to be searched for 
        potential crossover sites. Transparent green spheres indicating 
        potential crossover sites are displayed as you move (rotate or 
        translate) a DNA segment. After you are finished moving a DNA segment, 
        crossover sites are displayed as a pair of white cylinders that can 
        be highlighted/selected. Clicking on a highlighted crossover site 
        makes a crossover.
        </p>""") 
    
    return

def whatsThisTextForNanotubeCommandToolbar(commandToolbar):
    """
    "What's This" text for widgets in the Build Nanotube Command Toolbar.
    """
    commandToolbar.exitModeAction.setWhatsThis(
        """<b>Exit Nanotube</b>
        <p>
        Exits <b>Build Nanotube</b>.
        </p>""")
    
    commandToolbar.insertNanotubeAction.setWhatsThis(
        """<b>Insert Nanotube</b>
        <p>
        Displays the Insert Nanotube Property Manager
        </p>""")
    return

def whatsThisTextForCrystalCommandToolbar(commandToolbar):
    """
    "Tool Tip" text for widgets in the Build Crystal (crystal) Command Toolbar.
    """
    return

# Move command toolbar ####################

def whatsThisTextForMoveCommandToolbar(commandToolbar):
    """
    "What's This" text for widgets in the Move Command Toolbar.
    """
    return

def whatsThisTextForMovieCommandToolbar(commandToolbar):
    """
    "What's This" text for widgets in the Movie Command Toolbar.
    """
    return
