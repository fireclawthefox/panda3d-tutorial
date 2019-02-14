from setuptools import setup

exclude = [
    # build stuff
    'build/**',
    'build',
    'dist/**',
    'dist',
    '**/*.py',
    'setup.py',
    'requirements.txt']

setup(
    name='Tatakai no ikimono',
    author = "Fireclaw the Fox",
    author_email = "info@grimfang-studio.org",
    options = {
        'build_apps': {
            'include_patterns': ['**/*'],
            'exclude_patterns': exclude,
            'gui_apps': {
                'tatakai-no-ikimono': 'main.py',
            },
            'plugins': [
                'pandagl',
                'p3openal_audio'
            ]
        }
    }
)
