from django import template
register = template.Library()
 
@register.filter("truncate_chars")
def truncate_chars(value, max_length):
    if len(value) <= max_length:
        return value
 
    truncd_val = value[:max_length]
    if value[max_length] != " ":
        rightmost_space = truncd_val.rfind(" ")
        if rightmost_space != -1:
            truncd_val = truncd_val[:rightmost_space]
 
    return truncd_val + "..."

@register.filter
def truncchar(value, arg):
    truncated1 = value.lower().replace('&nbsp;',' ')
    truncated2 = truncated1.replace('&amp;',"&")
    truncated3 = truncated2.replace('&quot;','"')
    truncated4 = truncated3.replace('&lt;','<')
    truncated5 = truncated4.replace('&gt;','>')
    truncated = truncated5.replace('&#39;',"'")
    if len(truncated) < arg:
        return truncated.title()
    else:
        return truncated.title()[:arg] + '...'
    
@register.filter("truncate_img")
def truncate_img(value, max_length):
    image_truncate = str(value).split('/')[-1]
    if len(image_truncate) <= max_length:
        return value
 
    truncd_val = image_truncate[:max_length]
    if image_truncate[max_length] != " ":
        rightmost_space = truncd_val.rfind(" ")
        if rightmost_space != -1:
            truncd_val = truncd_val[:rightmost_space]
    return truncd_val + "..." +image_truncate.split('.')[-1]