'''
Created on Nov 24, 2011

@package: Newscoop
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the deployment of the distribution that contains this deploy.
'''

import os
import sys
import traceback

# --------------------------------------------------------------------

def findLibraries(folder):
    '''
    Finds all the libraries (that have extension .egg) if the provided folder.
    '''
    eggs = []
    for name in os.listdir(folder):
        fullPath = os.path.join(folder, name)
        if os.path.isfile(fullPath) and fullPath.endswith('.egg'): eggs.append(fullPath)
    return eggs

def findDirs(folder):
    '''
    Finds all the directories in the provided folder.
    '''
    dirs = []
    for name in os.listdir(folder):
        fullPath = os.path.join(folder, name)
        if os.path.isdir(fullPath): dirs.append(fullPath)
    return dirs

# --------------------------------------------------------------------

if __name__ == '__main__':
    import logging
    level = logging.WARN
    logging.basicConfig(level=level,
                    format='%(asctime)s %(levelname)s (%(threadName)s %(module)s.%(funcName)s %(lineno)d): %(message)s')
    
    applicationFrom, pluginsFrom = 'folder', 'folder'
    applicationProfile, pluginsProfile = False, False

    componentsConfig = {'serverType':'cherrypy', 'ajaxCrossDomain':True, 'phpZendSupport':True}
    # Loading the libraries
    for path in findLibraries(os.path.join(os.path.dirname(__file__), 'libraries')):
        if path not in sys.path: sys.path.append(path)
    # Loading the components.
    if applicationFrom == 'folder':
        for path in findDirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'components')):
            if path not in sys.path: sys.path.append(path)
    elif applicationFrom == 'egg':
        for path in findLibraries(os.path.join(os.path.dirname(__file__), 'components')):
            if path not in sys.path: sys.path.append(path)
    else: raise AssertionError('Invalid load from %s' % applicationFrom)
    
    
    # register the package extender.
    try:
        import package_extender
        package_extender.registerPackageExtender(False)
    except ImportError: traceback.print_exc()
    except: traceback.print_exc()
    
    try:
        import ally_deploy_application
        if applicationProfile:
            import profile
            profile.run('ally_application_deploy.deploy()', filename='output.stats')
        else: ally_deploy_application.deploy()
    except ImportError: traceback.print_exc()
    except: traceback.print_exc()
    else:
        # Loading the plugins. 
        if pluginsFrom == 'folder':
            for path in findDirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins')):
                if path not in sys.path: sys.path.append(path)
        elif pluginsFrom == 'egg':
            for path in findLibraries(os.path.join(os.path.dirname(__file__), 'plugins')):
                if path not in sys.path: sys.path.append(path)
        else: raise AssertionError('Invalid load from %s' % pluginsFrom)
        
        try:
            import ally_deploy_plugin
            if pluginsProfile:
                import profile
                profile.run('ally_deploy_plugin.deploy()', filename='output.stats')
            else: ally_deploy_plugin.deploy()
        except ImportError: traceback.print_exc()
        except: traceback.print_exc()
