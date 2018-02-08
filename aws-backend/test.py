#!/usr/bin/env python3

import lambda_function

print("Testing function ability to read and decode a webpage")

res = lambda_function.lambda_handler({"src" : "%3C!doctype%20html%3E%0A%3Chtml%3E%0A%20%20%3Chead%3E%0A%20%20%20%20%3Ctitle%3EGetting%20Started%20Extension%27s%20Popup%3C%2Ftitle%3E%0A%20%20%3C%2Fhead%3E%0A%0A%20%20%3Cbody%3E%0A%0A%3C%2Fhtml%3E%0A"}, None)

if res['title'] == "Getting Started Extension's Popup":
    print("Pass")
else:
    print("Fail")