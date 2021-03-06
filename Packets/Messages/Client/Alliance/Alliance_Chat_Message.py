from Packets.Messages.Server.Alliance.Alliance_Chat_Server_Message import AllianceChatServerMessage
from Packets.Messages.Server.AllianceBot.Alliance_Bot_Chat_Server_Message import AllianceBotChatServerMessage
from Packets.Messages.Server.Out_Of_Sync_Message import OutOfSyncMessage
from Database.DataBase import DataBase

from Utils.Reader import BSMessageReader


class AllianceChatMessage(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client
        self.bot_msg = ''
        self.send_ofs = False

    def decode(self):
        self.msg = self.read_string()

        if self.msg.lower() == '/stats':
            self.bot_msg = f'Server status:\nBuild version: 1.1 (for v26.165)\nFingerprint SHA: {self.player.patch_sha}'

        elif self.msg.lower() == '/reset':
            self.send_ofs = True
            DataBase.replaceValue(self, 'gold', 99999)
            DataBase.replaceValue(self, 'gems', 99999)
            DataBase.replaceValue(self, 'tickets', 99999)

        elif self.msg.lower().startswith('/gems'):
            try:
                newGems = self.msg.split(" ", 4)[1:]
                DataBase.replaceValue(self, 'gems', int(newGems[0]))
                self.send_ofs = True
            except:
                pass

        elif self.msg.lower().startswith('/gold'):
            try:
                newGold = self.msg.split(" ", 4)[1:]
                DataBase.replaceValue(self, 'gold', int(newGold[0]))
                self.send_ofs = True
            except:
                pass

        elif self.msg.lower().startswith('/tickets'):
            try:
                newTickets = self.msg.split(" ", 7)[1:]
                DataBase.replaceValue(self, 'tickets', int(newTickets[0]))
                self.send_ofs = True
            except:
                pass

        elif self.msg.lower().startswith('/starpoints'):
            try:
                newStarpoints = self.msg.split(" ", 10)[1:]
                DataBase.replaceValue(self, 'starpoints', int(newStarpoints[0]))
                self.send_ofs = True
            except:
                pass

        elif self.msg.lower() == '/help':
            self.bot_msg = 'Club Commands\n/stats - show server status\n/reset - reset all resources\n/gems [int] - add gems to your account, where int is the number of gems\n/gold [int] - add gold to your account, where int is the number of gold\n/tickets [int] - add tickets to your account, where int is the number of tickets\n/starpoints [int] - add starpoints to your account, where int is the number of starpoints'




    def process(self):
        AllianceChatServerMessage(self.client, self.player, self.msg).send()
        self.player.message_tick += 1

        if self.bot_msg != '':
            AllianceBotChatServerMessage(self.client, self.player, self.bot_msg).send()
            self.player.message_tick += 1

        if self.send_ofs:
            OutOfSyncMessage(self.client, self.player, 'Changes have been applied').send()
