# show_urls_custom.py

import json
from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    # Command help text
    help = "Displays all URL patterns and associated views in the project."

    def add_arguments(self, parser):
        # Add command line arguments
        parser.add_argument(
            '--format',  # Argument name
            choices=['text', 'json'],  # Available choices for the argument
            default='text',  # Default value if not provided
            help='Output format (text or json). Default is text.'  # Help text for the argument
        )

    def handle(self, *args, **options):
        # Retrieve the URL resolver for the project
        resolver = get_resolver()
        # Extract URL patterns based on command line options
        url_patterns = self.extract_urls(resolver)
        # Determine output format based on command line options
        output_format = options['format']
        # Print URL patterns in the specified format
        if output_format == 'json':
            # Print as JSON
            self.stdout.write(json.dumps(url_patterns, indent=4))
        else:
            # Print as text
            self.print_urls(url_patterns)

    def extract_urls(self, resolver, parent_pattern=None, namespace=None):
        """
        Recursively extract URL patterns and associated information.

        Args:
            resolver: The URL resolver object.
            parent_pattern: The parent URL pattern if applicable.
            namespace: The namespace of the URL pattern.

        Returns:
            A list of dictionaries containing URL pattern information.
        """
        url_patterns = []
        # Traverse through the URL patterns
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                # Recursively call the function for nested URL patterns
                url_patterns.extend(
                    self.extract_urls(pattern, parent_pattern=pattern.pattern, namespace=namespace)
                )
            else:
                # Extract information for the current URL pattern
                try:
                    url = {
                        'pattern': str(pattern.pattern if parent_pattern is None else parent_pattern.regex.pattern),
                        'name': str(pattern.name),
                        'callback': str(pattern.callback),
                        'namespace': namespace,
                    }
                    url_patterns.append(url)
                except Exception as e:
                    # Log any errors that occur during extraction
                    self.stderr.write(f"Error extracting URL pattern: {e}")
        return url_patterns

    def print_urls(self, url_patterns):
        """
        Print the extracted URL patterns.

        Args:
            url_patterns: A list of dictionaries containing URL pattern information.
        """
        # Print header
        self.stdout.write("URL Patterns:\n")
        # Print each URL pattern
        for url in url_patterns:
            self.stdout.write(self.style.SUCCESS(f"\tPattern: {url['pattern']}"))
            self.stdout.write(self.style.SUCCESS(f"\tView: {url['callback']}"))
            self.stdout.write(self.style.SUCCESS(f"\tName: {url['name']}"))
            if url['namespace']:
                self.stdout.write(self.style.SUCCESS(f"\tNamespace: {url['namespace']}"))
            self.stdout.write("")
        # Print total count of URL patterns
        self.stdout.write(self.style.SUCCESS("Total URL Patterns: %d" % len(url_patterns)))
