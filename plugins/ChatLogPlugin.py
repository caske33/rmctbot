import os, csv
import datetime

import pyirc.Plugin

class ChatLogPlugin(pyirc.Plugin.Plugin):
	confFile = 'logging.conf'

	def __init__(self, bot):
		super().__init__(bot)
		self.loginfo = dict()
		if os.path.exists(ChatLogPlugin.confFile):
			with open(ChatLogPlugin.confFile, 'r') as f:
				for chan, logdir in csv.reader(f):
					bot.join(chan)
					self.loginfo[chan] = logdir
					
	def _writelog(self, chan, msg):
		if chan not in self.loginfo: return
		now = datetime.datetime.now(datetime.timezone.utc)
		dfile = os.path.join(self.loginfo[chan], now.strftime('%Y-%m-%d.txt'))
		with open(dfile, 'a') as log:
			t = now.strftime('%H:%M:%S')
			print('[{:s}] {:s}'.format(t, msg), file=log)

	def handleChat(self, chan, sender, msg):
		self._writelog(chan, '<{:s}> {:s}'.format(sender, msg))
		return True

	def onKick(self, chan, nick):
		self._writelog(chan, '{:s} was kicked from {:s}'.format(nick, chan))
		return True

	def onNickChange(self, oldnick, newnick):
		for chan,cinfo in self.bot.channels.items():
			if oldnick in cinfo.users:
				self._writelog(chan, '{:s} is now known as {:s}'.format(oldnick, newnick))
		return True

