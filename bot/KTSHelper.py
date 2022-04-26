import xml.etree.cElementTree as ET
from datetime import date
import os
import logging

FORMAT = "[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
logging.basicConfig(filename='bot.log', level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

class KTSHelper:
    """
    Class to held tournament specific data and construct a KTS readable .Tournament file
    """
    def __init__(self, name: str, players: list) -> None:
        """
        takes a name for the tournament and a list of the players to participate formatted as "lastname,first name"
        constructs a valid xml that can be used in the KTS
        """
        self.xml = ET.Element("Tournament")
        ET.SubElement(self.xml, "Name").text = name
        ET.SubElement(self.xml, "ID").text = "X99-360236"
        ET.SubElement(self.xml, "TournamentStyleCode").text = "01"
        ET.SubElement(self.xml, "StructureCode").text = "01"
        ET.SubElement(self.xml, "EventTypeCode").text = "01"
        ET.SubElement(self.xml, "PlayerStructure").text = "01"
        ET.SubElement(self.xml, "ReferenceDateTime").text = "2003-01-02"
        ET.SubElement(self.xml, "Date").text = "2022-04-26"
        ET.SubElement(self.xml, "Time").text = date.today().strftime("%Y-%m-%d")
        ET.SubElement(self.xml, "CurrentRound").text = "0"
        ET.SubElement(self.xml, "TableOffset").text = "0"
        ET.SubElement(self.xml, "PlayoffRound").text = "0"
        ET.SubElement(self.xml, "SoftwareVersion").text = "3.0.0.0"
        ET.SubElement(self.xml, "Finalized").text = "False"
        staff = ET.SubElement(self.xml, "Staff")
        ET.SubElement(staff, "XmlStaffArray")
        ET.SubElement(self.xml, "PenaltyList")
        location = ET.SubElement(self.xml, "Location")
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
        self.players = ET.SubElement(self.xml, "TournamentPlayers")
        id = 9999000000
        for player in players:
            atts = player.split(",")
            name = atts[0]
            handle = atts[1]
            tourn_player = ET.SubElement(self.players, "TournPlayer")
            player_tag = ET.SubElement(tourn_player, "Player")
            ET.SubElement(player_tag, "ID").text = str(id)
            id+=1
            ET.SubElement(player_tag, "FirstName").text = handle
            ET.SubElement(player_tag, "LastName").text = name
            ET.SubElement(player_tag, "TeamPosition").text = "0"
            ET.SubElement(tourn_player, "DropRound").text = "0"
            ET.SubElement(tourn_player, "Rank").text = "1"
            ET.SubElement(tourn_player, "PlayoffPoints").text = "0"
            ET.SubElement(tourn_player, "Wins").text = "0"
            ET.SubElement(tourn_player, "Points").text = "0"
            ET.SubElement(tourn_player, "OpenDueling").text = "0"
            ET.SubElement(tourn_player, "DropReason").text = "Active"
            ET.SubElement(tourn_player, "AssignedSeat").text = "-1"
            ET.SubElement(tourn_player, "Notes")
        ET.SubElement(self.xml, "Matches")

    def get_xml(self) -> str:
        """
        Writes Tournament-xml to file and returns the filename/path
        """
        tournament_file = "teilnehmer.Tournament"
        try:
            os.remove(self.tournament_file)
        except FileNotFoundError:
            pass
        tree = ET.ElementTree(self.xml)
        tree.write(tournament_file, encoding="UTF-8", xml_declaration = True)
        return tournament_file
