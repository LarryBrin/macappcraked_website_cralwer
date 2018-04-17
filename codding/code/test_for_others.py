import os
from twisted.internet import reactor, defer

def read_mail(mailitems):
    print mailitems
    return "this %s is junk" % mailitems

def shred_mail(mailitems):
    print 'buzzzzz: %s' % mailitems
    reactor.stop()

def wait_for_mail(d=None):
    if not d:
        d = defer.Deferred()
    if not os.path.isfile('mail'):
        reactor.callLater(1, wait_for_mail, d)
    else:
        d.callback('letter')
    return d

deferred = wait_for_mail()
deferred.addCallback(read_mail)
deferred.addCallback(shred_mail)
reactor.callLater(60, reactor.stop)
reactor.run()
