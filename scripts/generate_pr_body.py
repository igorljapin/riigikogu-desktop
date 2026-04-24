# Script to generate a pull request body

"""
This script can be used to generate a pull request body based on the changes that are made.
"""

def generate_pr_body(changes):
    body = """## Pull Request

### Description

This pull request includes the following changes:
"""
    for change in changes:
        body += f'- {change}
'
    return body
