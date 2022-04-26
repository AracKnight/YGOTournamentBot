# YGOTournamentBot
This bot can be used to automate YGO Tournament signup.

You need a "#anmeldung" channel, in which only the bot can write but that everybody can see.

Upon using "!reset" in any text-channel it will clear all messages from the #anmeldung channel, and then recreate an Event Role you can use to grant access to tournament specific channels. Additionally it will post a sign-up post in #anmeldung.

Upon using "!teilnehmer" in any text-channel the bot will read who is currently reacting to the signup-post and then send a .Tournament file to this channel you can import into KTS.



To add this bot to your server use the following link:
https://discord.com/api/oauth2/authorize?client_id=968499475398160474&permissions=8858478656&scope=bot