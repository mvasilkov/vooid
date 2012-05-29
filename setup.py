from distutils.core import setup

setup(
    name = 'vooid',
    packages = ['vooid', 'vooid.templatetags'],
    package_data = {'vooid': ['templates/vooid/*html']},
    version = '1.4',
    description = 'Very Own OpenID server',
    author = 'Ivan Sagalaev',
    author_email = 'maniac@softwaremaniacs.org',
    url = 'https://github.com/mvasilkov/vooid',
    keywords = ['django', 'openid', 'vooid'],
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Framework :: Django',
    ],
)
