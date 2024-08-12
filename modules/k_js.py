def toggle(clicking_name,hiding_name):   
    return f'''
    <script>
        $("#{hiding_name}").hide();
        $("#{clicking_name}").click(function()'''+"{"+f"""
            $("#{hiding_name}").toggle();""" + '''
            })
    </script>  
    '''
