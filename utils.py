# def is_html_response(resp) -> bool:
#     """
#     Returns True if response seems to be HTML
#     """
#     content_type = resp.headers['Content-Type'].lower()
#     return (resp.status_code == 200
#             and content_type is not None
#             and content_type.find('html') > -1)