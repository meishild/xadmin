# import os
# from os.path import isfile
# from distutils.sysconfig import get_python_lib
#
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# path_list = [{
#     'pth_path': get_python_lib() + "/xadmin.pth",
#     'framework_path': BASE_DIR + "/framework/"
# }]
# for path in path_list:
#     if not isfile(path['pth_path']):
#         f = open(path['pth_path'], 'w')
#         f.write(path['framework_path'] + "\r")
#         f.close()
