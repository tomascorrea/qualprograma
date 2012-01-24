#gem 'chunky_png','=0.12.0'
#require 'lemonade'

sass_dir = "src"
css_dir = "../website/core/static/stylesheets"
images_dir = "../website/core/static/images"

http_path = "/"
http_css_path = "/static/stylesheets/"
http_images_path = "/static/images/"

project_type = :stand_alone
#output_style = :compressed
output_style = :expanded
environment = :production
relative_assets = false
sass_options = {:debug_info => true}
