import xml.etree.cElementTree as ET
from datetime import date
import os
import logging

FORMAT = "[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
logging.basicConfig(filename='bot.log', level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


def get_xml(name: str, players: list) -> str:
    """
    takes a name for the tournament and a list of the players to participate formatted as "lastname,first name"
    constructs a valid xml that can be used in the KTS
    """
    xml = ET.Element("Tournament")
    ET.SubElement(xml, "Name").text = name
    ET.SubElement(xml, "ID").text = "X99-360236"
    ET.SubElement(xml, "TournamentStyleCode").text = "01"
    ET.SubElement(xml, "StructureCode").text = "01"
    ET.SubElement(xml, "EventTypeCode").text = "01"
    ET.SubElement(xml, "PlayerStructure").text = "01"
    ET.SubElement(xml, "ReferenceDateTime").text = "2003-01-02"
    ET.SubElement(xml, "Date").text = "2022-04-26"
    ET.SubElement(xml, "Time").text = date.today().strftime("%Y-%m-%d")
    ET.SubElement(xml, "CurrentRound").text = "0"
    ET.SubElement(xml, "TableOffset").text = "0"
    ET.SubElement(xml, "PlayoffRound").text = "0"
    ET.SubElement(xml, "SoftwareVersion").text = "3.0.0.0"
    ET.SubElement(xml, "Finalized").text = "False"
    staff = ET.SubElement(xml, "Staff")
    ET.SubElement(staff, "XmlStaffArray")
    ET.SubElement(xml, "PenaltyList")
    location = ET.SubElement(xml, "Location")
    ET.SubElement(location, "Id").text = "535afeba-3a06-432a-890f-bc87366bdbd1"
    ET.SubElement(location, "Name")
    ET.SubElement(location, "Address1")
    ET.SubElement(location, "Address2")
    ET.SubElement(location, "City")
    ET.SubElement(location, "State")
    ET.SubElement(location, "Country")
    ET.SubElement(location, "Zip")
    ET.SubElement(location, "Phone")
    ET.SubElement(location, "WebSite")
    players_tag = ET.SubElement(xml, "TournamentPlayers")
    player_id = 9999000000
    for player in players:
        atts = player.split("#")
        name = atts[0]
        handle = atts[1]
        tournament_player = ET.SubElement(players_tag, "TournPlayer")
        player_tag = ET.SubElement(tournament_player, "Player")
        ET.SubElement(player_tag, "ID").text = str(player_id)
        player_id += 1
        ET.SubElement(player_tag, "FirstName").text = '#' + handle
        ET.SubElement(player_tag, "LastName").text = name
        ET.SubElement(player_tag, "TeamPosition").text = "0"
        ET.SubElement(tournament_player, "DropRound").text = "0"
        ET.SubElement(tournament_player, "Rank").text = "1"
        ET.SubElement(tournament_player, "PlayoffPoints").text = "0"
        ET.SubElement(tournament_player, "Wins").text = "0"
        ET.SubElement(tournament_player, "Points").text = "0"
        ET.SubElement(tournament_player, "OpenDueling").text = "0"
        ET.SubElement(tournament_player, "DropReason").text = "Active"
        ET.SubElement(tournament_player, "AssignedSeat").text = "-1"
        ET.SubElement(tournament_player, "Notes")
    ET.SubElement(xml, "Matches")
    tournament_file = "teilnehmer.Tournament"
    try:
        os.remove(tournament_file)
    except FileNotFoundError:
        pass
    ET.ElementTree(xml).write(tournament_file, encoding="UTF-8", xml_declaration=True)
    return tournament_file
