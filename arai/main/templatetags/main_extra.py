from django import template

register = template.Library()

@register.filter
def page_window(page, last, size=7):
    if page < size // 2 + 1:
        return range(1, min(size+1, last + 1))
    else:
        return range(page - size // 2, min(last + 1, page + 1 + size // 2))

@register.filter
def add_page_num(request, page):
    """
    Update page number variable to a url that may or may not have other GET variables
    """
    vars = request.GET.copy()
    vars["page"] = page
    var_string = "&".join([f"{k}={v}" for k, v in vars.items()])
    return f"{request.path}?{var_string}"

@register.filter
def path_to_key(path):
    return path.replace("/", "")