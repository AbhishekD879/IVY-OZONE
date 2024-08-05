package com.ladbrokescoral.cashout.service

import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet
import com.corundumstudio.socketio.BroadcastOperations
import com.corundumstudio.socketio.SocketIOServer
import com.ladbrokescoral.cashout.model.Code
import com.ladbrokescoral.cashout.model.response.CashoutData
import com.ladbrokescoral.cashout.model.response.ErrorBetResponse
import com.ladbrokescoral.cashout.model.response.UpdateBetResponse
import com.ladbrokescoral.cashout.model.response.UpdateCashoutResponse
import com.ladbrokescoral.cashout.service.updates.UserUpdateTriggerDto
import spock.lang.Specification

class SocketIoUserUpdatesContextTest extends Specification {
  SocketIOServer socketIoServer = Mock(SocketIOServer)
  UserUpdatesContext ctx = new SocketIoUserUpdatesContext(socketIoServer)
  BroadcastOperations roomOps

  void setup() {
    roomOps = Mock(BroadcastOperations)
    roomOps.getClients() >> []
  }

  def "BetUpdates are sent"() {
    def bet = new Bet()
    bet.betId = "111"
    def response = new UpdateBetResponse(bet)
    socketIoServer.getRoomOperations("123") >> roomOps
    when:
    ctx.sendBetUpdate("123", response)
    then:
    1 * roomOps.sendEvent("betUpdate", response)
  }

  def "Bet update errors are sent"() {
    def errResponse = new ErrorBetResponse(new ErrorBetResponse.Error(Code.UNAUTHORIZED_ACCESS))
    socketIoServer.getRoomOperations("123") >> roomOps
    when:
    ctx.sendBetUpdateError("123", errResponse)
    then:
    roomOps.sendEvent("betUpdate", errResponse)
  }

  def "Cashout updates are sent"() {
    def response = new UpdateCashoutResponse(CashoutData.builder().betId("111").build(), null)
    socketIoServer.getRoomOperations("123") >> roomOps
    when:
    ctx.sendCashoutUpdate("123", response)
    then:
    1 * roomOps.sendEvent("cashoutUpdate", response)
  }

  def "Nothing happens when empty dto supplied"() {
    when:
    ctx.triggerBetSettled(UserUpdateTriggerDto.builder().build())
    ctx.triggerCashoutSuspension(UserUpdateTriggerDto.builder().build())
    ctx.triggerBetSettled(null)
    ctx.triggerCashoutSuspension(null)
    ctx.triggerBetSettled(UserUpdateTriggerDto.builder().betIds(Collections.emptySet()).build())
    ctx.triggerCashoutSuspension(UserUpdateTriggerDto.builder().betIds(Collections.emptySet()).build())
    then:
    0 * _
  }

  def "Bet settled updates are sent"() {
    when:
    ctx.triggerBetSettled(UserUpdateTriggerDto.builder()
        .betIds(["123", "234"] as Set)
        .token("abc")
        .build())
    then:
    1 * socketIoServer.getRoomOperations("123") >> this.roomOps
    1 * socketIoServer.getRoomOperations("234") >> this.roomOps
    1 * roomOps.sendEvent("betUpdate", [settledBetUpdate("123")])
    1 * roomOps.sendEvent("betUpdate", [settledBetUpdate("234")])
  }

  def "Bet suspended updates are sent"() {
    when:
    ctx.triggerCashoutSuspension(UserUpdateTriggerDto.builder()
        .betIds(["123", "234"] as Set)
        .token("abc")
        .build())
    then:
    2 * socketIoServer.getRoomOperations("abc") >> this.roomOps
    1 * roomOps.sendEvent("betUpdate", [suspendedBetUpdate("123")])
    1 * roomOps.sendEvent("betUpdate", [suspendedBetUpdate("234")])
  }

  UpdateBetResponse settledBetUpdate(String betId) {
    def bet = new Bet()
    bet.setBetId(betId)
    bet.setCashoutValue("BET_SETTLED")
    bet.setSettled("Y")
    return new UpdateBetResponse(bet)
  }

  UpdateBetResponse suspendedBetUpdate(String betId) {
    def bet = new Bet()
    bet.setBetId(betId)
    bet.setCashoutValue("CASHOUT_SELN_SUSPENDED")
    bet.setCashoutStatus("Suspended by cashout microservice: bet has suspended selection(s)")
    return new UpdateBetResponse(bet)
  }
}
