def css_to_xpath(css_selector):
    # Split the CSS selector by ' ' (descendant selector) and '>' (child selector)
    parts = css_selector.split(' ')

    xpath_parts = []
    is_child = False  # Flag to track child selectors

    for part in parts:
        # Check if the part is a direct child (>)
        if '>' in part:
            is_child = True
            part = part.replace('>', '')
        
        # Start building XPath for each element part
        xpath = ''

        # Check if part has an ID (e.g. #id)
        if '#' in part:
            tag_and_id = part.split('#')
            tag = tag_and_id[0]
            id_val = tag_and_id[1]
            xpath = f"{tag}[@id='{id_val}']"
        else:
            tag = part
            xpath = tag

        # Handle multiple classes in the part (e.g. .class1.class2)
        classes = part.split('.')
        if len(classes) > 1:  # More than one class (first element is the tag name)
            class_xpath = " and ".join([f"contains(@class, '{cls}')" for cls in classes[1:]])
            xpath = f"{xpath}[{class_xpath}]"

        # Add to the list of XPath parts, handle child vs descendant
        if is_child:
            xpath_parts.append(f"/{xpath}")
            is_child = False
        else:
            xpath_parts.append(f"{xpath}")

    # Join the parts into the final XPath expression
    return "".join(xpath_parts)


# Test the function
css_selector = "div.heading > p.id1 .class1.class2"
xpath = css_to_xpath(css_selector)
print("CSS Selector:", css_selector)
print("XPath:", xpath)
