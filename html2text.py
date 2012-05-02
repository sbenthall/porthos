from subprocess import Popen, PIPE

def bytes_to_text(html):
        elinks=Popen(["elinks", "-dump", "-no-references", "-no-numbering", "-dump-charset", "utf-8"], stdin=PIPE, stdout=PIPE)
        txt, _ = elinks.communicate(input=html.encode('utf8'))
        return txt.decode('utf8', 'ignore')
