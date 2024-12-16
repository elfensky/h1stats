# made by SacredSky and posted in the Helldivers Discord
from flask import Flask, render_template_string, request
import requests, urllib3
 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
victory_list = [0,0,0,0]
faction_name_list = ["Bugs", "Cyborgs", "Illuminates", "Super Earth"]
 
app = Flask(__name__)
 
@app.route('/', methods=['GET'])
def fetch_stats():
    response_current_war = requests.post("https://api.helldiversgame.com/1.0/", data={"action":"get_campaign_status"}, verify=False).json()
    attack_string = ""
    defend_string = "No defend event in progress<br>"
    campaign_string = ""
    if 'defend_event' in response_current_war and 'status' in response_current_war['defend_event']:
        if response_current_war['defend_event']['status'] == 'active':
            p = response_current_war['defend_event']['points'] / float(response_current_war['defend_event']['points_max'])
            defend_string = "Defending on " + faction_name_list[
                response_current_war['defend_event']['enemy']] + ": <b>" + str(
                response_current_war['defend_event']['points']) + "/" + str(
                response_current_war['defend_event']['points_max']) + "</b> (" + "{:.1%}".format(p) + ")<br>"
        else:
            defend_string += "Last event is <b>" + response_current_war['defend_event']['status'] + "</b> in " + \
                             faction_name_list[response_current_war['defend_event']['enemy']] + ": " + str(
                response_current_war['defend_event']['points']) + "/" + str(
                response_current_war['defend_event']['points_max']) + "<br>"
    if 'attack_events' in response_current_war:
        for ae in response_current_war['attack_events']:
            if 'status' in ae and ae['status'] == 'active':
                p = ae['points'] / float(ae['points_max'])
                attack_string += "Attacking on " + faction_name_list[
                    ae['enemy']] + ": <b>" + str(
                    ae['points']) + "/" + str(
                    ae['points_max']) + "</b> (" + "{:.1%}".format(p) + ")<br>"
            else:
                attack_string += "Last event is <b>" + ae['status'] + "</b> in " + \
                                 faction_name_list[ae['enemy']] + ": " + str(
                    ae['points']) + "/" + str(
                    ae['points_max']) + "<br>"
    if 'campaign_status' in response_current_war:
        for i in range(3):
            ae = response_current_war['campaign_status'][i]
            if 'status' in ae and ae['status'] == 'active':
                p = ae['points'] / float(ae['points_max'])
                campaign_string += faction_name_list[i] + " is <b>active</b>: <b>" + str(
                    ae['points']) + "/" + str(
                    ae['points_max']) + "</b> (" + "{:.1%}".format(p) + ")"
            else:
                campaign_string += faction_name_list[
                                       i] + " is <b>" + ae['status'] + "</b>"
            campaign_string+=" current players: "+str(response_current_war['statistics'][i]['players'])+"<br>"
    # Generate HTML output
    html_template = """
    <html>
        <head><title>Current Helldivers 1 Stats</title></head>
        <body>
            <h1>Current Defend Events</h1>
            <div>{{ defend_string|safe }}</div>
            <h1>Current Attack Events</h1>
            <div>{{ attack_string|safe }}</div>
            <h1>Current Campaign</h1>
            <div>{{ campaign_string|safe }}</div>
        </body>
    </html>
    """
    return render_template_string(html_template, defend_string=defend_string, attack_string=attack_string, campaign_string=campaign_string)
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)