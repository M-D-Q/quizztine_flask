
import re

string = '''<span class="answer-description">                                            
To view a template from deployment history:<br>1. Go to the resource group for your new resource group. Notice that the portal shows the result of the last deployment. Select this link.<br><img src="./AZ-104_files/0001100001.jpg" class="in-exam-image"><br>2
. You see a history of deployments for the group. In your case, the portal probably lists only one deployment. Select this deployment.<br><img src="./AZ-104_files/0001200001.jpg" class="in-exam-image"><br>3. The portal displays a summary of the deployment. The summary includes the status of the deployment and its operations and the values that you provided for parameters.
 To see the template that you used for the deployment, select View template.
 <br><img src="./AZ-104_files/0001300001.jpg" class="in-exam-image"><br>Reference:<br>https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-export-template                                        </span>'''

def replace_image_html(string_html):
    match = re.search(r'<img src="\./AZ-104_files/([0-9]+\...g)" class="in-exam-image">', string_html)
    if match :
        miaou = match.group(1)
        string_corrigee = r'''<img src="{{ url_for('static',filename='images/'''+str(miaou)+r'''') }}">'''
        new_string = re.sub(r'<img src="\./AZ-104_files/([0-9]+\...g)" class="in-exam-image">', string_corrigee, string_html)
        print(new_string)
        return(new_string)
    else :
        return(string_html)

    
def replace_liste_image_html(string_html):
    match_list = re.findall(r'<img src="\./AZ-104_files/([0-9]+\...g)" class="in-exam-image">', string_html)
    if len(match_list) > 0:
        for i in range(0,len(match_list)):
            miaou = match_list[i]
            #string_corrigee = r'''<img src="{{ url_for('static',filename='images/'''+str(miaou)+r'''') }}">'''
            string_corrigee = (f"<img src=\"/static/images/{miaou}\">")
            string_html = re.sub(r'<img src="\./AZ-104_files/([0-9]+\...g)" class="in-exam-image">', string_corrigee, string_html, count=1)
        return(string_html)
    else:
        return(string_html)

print(replace_liste_image_html(string))