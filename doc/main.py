from docutils.core import publish_file
publish_file(source_path='preface.rst', destination_path='preface.html', writer_name='html', settings_overrides={'stylesheet_path': 'main.css'

})

s=r'tutorial\statistical_inference\supervised_learning.rst'
d=r'tutorial\statistical_inference\supervised_learning.html'
publish_file(source_path=s, destination_path=d, writer_name='html', settings_overrides={'stylesheet_path': 'main.css'

})