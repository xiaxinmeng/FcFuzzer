sendmsg = getattr(socket.socket, 'sendmsg', False)

def writelines(self, lines):
    if not sendmsg:
        return self.write(b''.join(sendmsg))