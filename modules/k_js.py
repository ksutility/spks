def j_toggle(clicking_name,hiding_css_selector):   
    return f'''
    <script>
        $("{hiding_css_selector}").hide();
        $("#{clicking_name}").click(function()'''+"{"+f"""
            $("{hiding_css_selector}").toggle();""" + '''
            })
    </script>  
    '''
