from Packets.Messages.Server.Gameroom.TeamGameroomDataMessage import TeamGameroomDataMessage

from Utils.Reader import BSMessageReader

class TeamSetLocationMessage(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.read_Vint()
        self.player.mapID = self.read_Vint()


    def process(self):
        TeamGameroomDataMessage(self.client, self.player).send()