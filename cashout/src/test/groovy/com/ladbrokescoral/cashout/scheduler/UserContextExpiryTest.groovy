package com.ladbrokescoral.cashout.scheduler

import com.corundumstudio.socketio.HandshakeData
import com.corundumstudio.socketio.SocketIOClient
import com.corundumstudio.socketio.SocketIOServer
import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory
import com.ladbrokescoral.cashout.service.BetUpdateService
import spock.lang.Specification

import java.util.concurrent.ConcurrentHashMap

class UserContextExpiryTest extends Specification {
  private Date connDate = new Date()
  private BetUpdateService betUpdateService
  private UUID sid = UUID.randomUUID()
  private SocketIOClient socketIOClient = createSocketIoClientMock(sid)

  private  SocketIOServer socketIOServer
  private PurgeUserContextScheduler purgeUserContextScheduler;

  void setup() {

    betUpdateService = Mock(BetUpdateService)
    socketIOServer=Mock(SocketIOServer)
    purgeUserContextScheduler=new PurgeUserContextScheduler(betUpdateService,  socketIOServer)
  }


  def "ping with new SessionId and remove from context if expired with session client open "() {
    given:
    socketIOServer.getClient(socketIOClient.getSessionId())>>socketIOClient
    Map<UUID, UserRequestContextAccHistory> userMap=new ConcurrentHashMap<>()
    userMap.put(socketIOClient.getSessionId(),new UserRequestContextAccHistory())
    userMap.put(UUID.randomUUID(),new UserRequestContextAccHistory())
    betUpdateService.getUserContexts() >> userMap
    when:
    purgeUserContextScheduler.processUserContext()
    then:
    1 * betUpdateService.unsubscribeInInternalPubSub(socketIOClient.getSessionId())
  }


  def "ping with new SessionId and remove from context if expired"() {
    given:
    socketIOClient.isChannelOpen()>>true
    socketIOServer.getClient(socketIOClient.getSessionId())>>socketIOClient
    Map<UUID, UserRequestContextAccHistory> userMap=new ConcurrentHashMap<>()
    userMap.put(socketIOClient.getSessionId(),new UserRequestContextAccHistory())
    userMap.put(UUID.randomUUID(),new UserRequestContextAccHistory())
    betUpdateService.getUserContexts() >> userMap
    when:
    purgeUserContextScheduler.processUserContext()
    then:
    0 * betUpdateService.unsubscribeInInternalPubSub(socketIOClient.getSessionId())
  }


  private SocketIOClient createSocketIoClientMock(UUID sid) {
    def client = Mock(SocketIOClient)
    client.getSessionId() >> sid
    def data = Mock(HandshakeData)
    data.getTime() >> connDate
    client.getHandshakeData() >> data
    return client
  }
}
