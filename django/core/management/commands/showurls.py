from django.core.management.base import BaseCommand
#from django.urls import URLResolver, URLPattern
from django.urls import get_resolver


class Command(BaseCommand):
    help = "Displays all URLs configured in your Django project"

    def add_arguments(self, parser):
        parser.add_argument(
            "--app",
            nargs="*",
            type=str,
            help="Specify an app to display the URLs for.",
        )
        parser.add_argument(
            "--format",
            "-f",
            action="store",
            dest="format",
            default="list",
            help=(
                "The format to display the URLs. Options are 'list' and 'json'."
            ),
        )

    def handle(self, *args, **options):
        resolver = get_resolver()
        self.print_urls(resolver, options["app"])

    def print_urls(self, resolver, app_name=None, prefix=""):
        for url_pattern in resolver.url_patterns:
            if hasattr(url_pattern, "url_patterns"):
                    self.print_urls(url_pattern, prefix + url_pattern.pattern.regex.pattern) 
            else:
                if app_name:
                    if app_name[0] in url_pattern.lookup_str:
                        try:
                            self.stdout.write(prefix + url_pattern.pattern.regex.pattern)
                        except Exception as e:
                            self.stderr.write(f"Error: {e}")
                else:
                    try:
                        self.stdout.write(prefix + url_pattern.pattern.regex.pattern)
                    except Exception as e:
                        self.stderr.write(f"Error: {e}")
                    
