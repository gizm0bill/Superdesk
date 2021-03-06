'''
Created on Feb 23, 2012

@package: ally actions gui 
@copyright: 2011 Sourcefabric o.p.s.
@license:  http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu
'''

from ..gui_action import defaults
from ..gui_action.service import addAction
from ..gui_core.gui_core import publishedURI
from ..gui_security import acl
from ally.container import ioc
from ally.internationalization import NC_
from distribution.container import app
from gui.action.api.action import Action
from superdesk.user.api.user import IUserService
from superdesk.media_archive.api.meta_data import IMetaDataUploadService
from ..superdesk_security.acl import filterAuthenticated
    
# --------------------------------------------------------------------

@ioc.entity   
def menuAction():
    return Action('user', Parent=defaults.menuAction(), Label=NC_('menu', 'Users'), NavBar='/users',
                  Script=publishedURI('superdesk/user/scripts/js/menu.js'))

@ioc.entity   
def modulesAction():
    return Action('user', Parent=defaults.modulesAction())

@ioc.entity   
def modulesUpdateAction():
    return Action('update', Parent=modulesAction(), Script=publishedURI('superdesk/user/scripts/js/modules-update.js'))

@ioc.entity   
def modulesListAction():
    return Action('list', Parent=modulesAction(), Script=publishedURI('superdesk/user/scripts/js/list.js'))

# @ioc.entity   
# def modulesAddAction():
#    return Action('add', Parent=modulesAction(), ScriptPath=getPublishedGui('superdesk/user/scripts/js/modules-add.js'))

# --------------------------------------------------------------------

@ioc.entity
def rightUserView():
    return acl.actionRight(NC_('security', 'Users view'), NC_('security', '''
    Allows read only access to users.'''))

@ioc.entity
def rightUserUpdate():
    return acl.actionRight(NC_('security', 'Users update'), NC_('security', '''
    Allows the update of users.'''))

# --------------------------------------------------------------------

@app.deploy
def registerActions():
    addAction(menuAction())
    addAction(modulesAction())
    addAction(modulesUpdateAction())
    addAction(modulesListAction())
    # addAction(modulesAddAction())

@acl.setup
def registerAclUserView():
    rightUserView().addActions(menuAction(), modulesAction(), modulesListAction())\
    .allGet(IUserService)
    
@acl.setup
def registerAclUserUpdate():
    rightUserUpdate().addActions(menuAction(), modulesAction(), modulesListAction(), modulesUpdateAction())\
    .all(IUserService)
    rightUserUpdate().byName(IMetaDataUploadService, IMetaDataUploadService.insert, filter=filterAuthenticated())
