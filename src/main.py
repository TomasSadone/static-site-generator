
import helpers

def main():
    helpers.copy_contents("static", "public")
    helpers.generate_pages_recursive("content", "template.html", "public")


main()