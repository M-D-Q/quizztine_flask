
import re

string = '''<p class="card-text">
                                        
                                        
                                            HOTSPOT -<br>You have an Azure Active Directory (Azure AD) tenant.<br>You need to create a conditional access policy that requires all users to use multi-factor authentication when they access the Azure portal.<br>Which three settings should you configure? To answer, select the appropriate settings in the answer area.<br>NOTE: Each correct selection is worth one point.<br>Hot Area:<br><img src="./AZ-104_files/0007300001.png" class="in-exam-image"><br>
                                        
                                    </p>'''

def replace_image_html(string_html):
    match = re.search(r'<img src="\./AZ-104_files/(.+)" class="in-exam-image">', string_html)
    if match :
        miaou = match.group(1)
        string_corrigee = r'''<img src="{{ url_for('static',filename='images/'''+str(miaou)+r'''') }}">'''
        print(string_corrigee)
        new_string = re.sub(r'<img src="\./AZ-104_files/.+" class="in-exam-image">', string_corrigee, string_html)
        print(new_string)
        return(new_string)
    else :
        return(string_html)

    
replace_image_html(string)