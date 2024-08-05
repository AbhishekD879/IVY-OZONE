package com.ladbrokescoral.cashout.socketio

import com.coral.bpp.api.exception.BppUnauthorizedException
import com.coral.bpp.api.model.bet.api.request.AccountHistoryRequest
import com.coral.bpp.api.model.bet.api.response.accountHistory.Paging
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel
import com.corundumstudio.socketio.HandshakeData
import com.corundumstudio.socketio.SocketIOClient
import com.ladbrokescoral.cashout.bpptoken.BppToken
import com.ladbrokescoral.cashout.bpptoken.BppTokenOperations
import com.ladbrokescoral.cashout.model.Code
import com.ladbrokescoral.cashout.model.response.ErrorBetResponse
import com.ladbrokescoral.cashout.model.response.InitialAccountHistoryBetResponse
import com.ladbrokescoral.cashout.payout.PayoutUpdatesPublisher
import com.ladbrokescoral.cashout.service.AccountHistoryService
import com.ladbrokescoral.cashout.service.BetUpdateService
import reactor.core.publisher.Mono
import reactor.core.scheduler.Schedulers
import spock.lang.Specification
class SocketIoControllerTest extends Specification {

  private SocketIoController controller
  private AccountHistoryService accountHistoryService
  private BetUpdateService betUpdateService
  private UUID sid = UUID.randomUUID()
  private Date connDate = new Date()
  private String bppToken = "abc"
  private String pagingBlockSize = "20"
  private String group = "BET"
  private String detailLevel = "DETAILED"
  private String settled = "N"
  private String fromDate = "2021-09-15 00:00:00"
  private String toDate = "2021-09-21 23:59:59"
  private SocketIOClient client = createClientMock(sid, bppToken)
  private SocketIOClient socketIOClient = createSocketIoClientMock(sid)
  static private betWithCashoutNotAvailable
  private BppTokenOperations bppTokenOperations
  private PayoutUpdatesPublisher payoutUpdatesPublisher
  private BppToken bppTokenWrapperMock
  def accountHistoryRequest =  Mock(AccountHistoryRequest)
  void setup() {
    betWithCashoutNotAvailable = new BetSummaryModel()
    betWithCashoutNotAvailable.id = "567"
    betWithCashoutNotAvailable.cashoutValue = "CASHOUT_SELN_NO_CASHOUT"
    accountHistoryRequest.getToken() >> bppToken
    accountHistoryRequest.getPagingBlockSize() >> pagingBlockSize
    accountHistoryRequest.getGroup() >> group
    accountHistoryRequest.getDetailLevel() >> detailLevel
    accountHistoryRequest.getSettled() >> settled
    accountHistoryRequest.getFromDate() >> fromDate
    accountHistoryRequest.getToDate() >> toDate
    accountHistoryService = Mock(AccountHistoryService)
    accountHistoryService.accountHistoryInitBets(accountHistoryRequest)
    betUpdateService = Mock(BetUpdateService)
    bppTokenOperations = Mock(BppTokenOperations)
    payoutUpdatesPublisher = Mock(PayoutUpdatesPublisher)
    bppTokenWrapperMock = Mock(BppToken)
    bppTokenWrapperMock.getToken() >> bppToken
    //bppTokenOperations.parseToken(_) >> bppTokenWrapperMock
    //bppTokenOperations.parseToken(bppToken) >> {throw new BppUnauthorizedException("Unauthorized")}
    controller = new SocketIoController(accountHistoryService, betUpdateService, bppTokenOperations,payoutUpdatesPublisher)
  }

  def "If token is invalidated then unauthorized is send to client and connection is closed"() {
    def ex = new BppUnauthorizedException("Unauthorized")
    given:
    mockAccountHistory(
        Mono.error({ ex })
        .subscribeOn(Schedulers.immediate()))
    when:
    controller.onConnect(client)
    then:
    0 * client.joinRoom(_)
    1 * client.sendEvent("initial", ErrorBetResponse.create(Code.fromException(ex)))
    1 * client.disconnect()
  }

  def "Test Catch Block for nextBets Action"() {
    given:
    def reqeust = [token:"abc" , pagingToken: "abcxyz", blockSize: "20", detailLevel: "DETAILED"]
    bppTokenOperations.parseToken(bppToken) >> { throw new BppUnauthorizedException("Unauthorized")}
    def ex = new BppUnauthorizedException("Unauthorized")
    when:
    controller.onEvent(socketIOClient,reqeust)
    then:
    0 * socketIOClient.joinRoom(_)
    1 * socketIOClient.sendEvent("nextBetsUpdate", ErrorBetResponse.create(Code.fromException(ex)))
    1 * socketIOClient.disconnect()
  }

  def "Default OnConnect Method Call"(){
    given:
    bppTokenOperations.parseToken(_) >> bppTokenWrapperMock
    def accHistoryResponse = accountHistoryResponse()
    def betThatServiceShouldSubscribeOn = accHistoryResponse.getBets()
    mockAccountHistory(
        Mono.fromSupplier({ accHistoryResponse })
        .subscribeOn(Schedulers.immediate()))
    when:
    controller.onConnect(client)
    then:
    accHistoryResponse.getBets().size() == 3
    1 * client.joinRoom(bppToken)
    1 * client.joinRoom("123")
    1 * client.joinRoom("456")
    1 * client.joinRoom(betWithCashoutNotAvailable.id)
    0 * client.joinRoom(_)
    1 * betUpdateService.createSubscriptionInInternalPubSub(sid, bppTokenWrapperMock, connDate, betThatServiceShouldSubscribeOn)
  }

  def "If token is invalidated then unauthorized send to initialBets and connection is closed"() {
    def ex = new BppUnauthorizedException("Unauthorized")
    given:
    def reqeust = [token:"abc" , pagingToken: "abcxyz", blockSize: "20", detailLevel: "DETAILED", fromDate:"2021-09-15 00:00:00", toDate: "2021-09-21 23:59:59" ,settled:"N", group:"BET"]
    mockAccountHistory(
        Mono.error({ ex })
        .subscribeOn(Schedulers.immediate()))
    when:
    controller.onInitialEvent(socketIOClient,reqeust)
    then:
    0 * socketIOClient.joinRoom(_)
    1 * socketIOClient.sendEvent("initial", ErrorBetResponse.create(Code.fromException(ex)))
    1 * socketIOClient.disconnect()
  }

  def "Test Catch Block for initialBets Action"() {
    given:
    def reqeust = [token:"abc" , pagingToken: "abcxyz", blockSize: "20", detailLevel: "DETAILED", fromDate:"2021-09-15 00:00:00", toDate: "2021-09-21 23:59:59" ,settled:"N", group:"BET"]
    bppTokenOperations.parseToken(bppToken) >> { throw new BppUnauthorizedException("Unauthorized")}
    def ex = new BppUnauthorizedException("Unauthorized")
    when:
    controller.onInitialEvent(socketIOClient,reqeust)
    then:
    0 * socketIOClient.joinRoom(_)
    1 * socketIOClient.sendEvent("initial", ErrorBetResponse.create(Code.fromException(ex)))
    1 * socketIOClient.disconnect()
  }

  def "pushing onEvent initialBets"(){
    given:
    bppTokenOperations.parseToken(_) >> bppTokenWrapperMock
    def reqeust = [token:"abc" , pagingToken: "abcxyz", blockSize: "20", detailLevel: "DETAILED", fromDate:"2021-09-15 00:00:00", toDate: "2021-09-21 23:59:59" ,settled:"N", group:"BET"]
    def accHistoryResponse = accountHistoryResponse()
    def betThatServiceShouldSubscribeOn = accHistoryResponse.getBets()
    mockAccountHistory(
        Mono.fromSupplier({ accHistoryResponse })
        .subscribeOn(Schedulers.immediate()))
    when:
    controller.onInitialEvent(socketIOClient,reqeust)
    then:
    accHistoryResponse.getBets().size() == 3
    1 * socketIOClient.joinRoom(bppToken)
    1 * socketIOClient.joinRoom("123")
    1 * socketIOClient.joinRoom("456")
    1 * socketIOClient.joinRoom(betWithCashoutNotAvailable.id)
    0 * socketIOClient.joinRoom(_)
    1 * betUpdateService.createSubscriptionInInternalPubSub(sid, bppTokenWrapperMock, connDate, betThatServiceShouldSubscribeOn)
  }

  def "If token is invalidated then unauthorized send to nextBets and connection is closed"() {
    def ex = new BppUnauthorizedException("Unauthorized")
    given:
    def reqeust = [token:"abc" , pagingToken: "abcxyz", blockSize: "20", detailLevel: "DETAILED"]
    mockAccountHistory(
        Mono.error({ ex })
        .subscribeOn(Schedulers.immediate()))
    when:
    controller.onEvent(socketIOClient,reqeust)
    then:
    0 * socketIOClient.joinRoom(_)
    1 * socketIOClient.sendEvent("nextBetsUpdate", ErrorBetResponse.create(Code.fromException(ex)))
    1 * socketIOClient.disconnect()
  }

  def "pushing onEvent nextBets"(){
    given:
    bppTokenOperations.parseToken(_) >> bppTokenWrapperMock
    def reqeust = [token:"abc" , pagingToken: "abcxyz", blockSize: "20", detailLevel: "DETAILED"]
    def accHistoryResponse = accountHistoryResponse()
    def betThatServiceShouldSubscribeOn = accHistoryResponse.getBets()
    mockAccountHistory(
        Mono.fromSupplier({ accHistoryResponse })
        .subscribeOn(Schedulers.immediate()))
    when:
    controller.onEvent(socketIOClient,reqeust)
    then:
    accHistoryResponse.getBets().size() == 3
    1 * socketIOClient.joinRoom(bppToken)
    1 * socketIOClient.joinRoom("123")
    1 * socketIOClient.joinRoom("456")
    1 * socketIOClient.joinRoom(betWithCashoutNotAvailable.id)
    0 * socketIOClient.joinRoom(_)
    1 * betUpdateService.createSubscriptionInInternalPubSub(sid, bppTokenWrapperMock, connDate, betThatServiceShouldSubscribeOn)
  }

  def "If token parsing produces error then unauthorized is send to client and connection is closed"() {
    when:
    controller.onConnect(client)
    then:
    bppTokenOperations.parseToken(_) >> {t -> throw new BppUnauthorizedException("Unauthorized")}
    0 * client.joinRoom(_)
    1 * client.sendEvent("initial", ErrorBetResponse.create(Code.fromException(new BppUnauthorizedException("Unauthorized"))))
    1 * client.disconnect()
  }

  def "If accountHistory is returned then everything is proxied to UI but subscribed only on cashout available bets"() {
    given:
    bppTokenOperations.parseToken(_) >> bppTokenWrapperMock
    def accHistoryResponse = accountHistoryResponse()
    def betThatServiceShouldSubscribeOn = accHistoryResponse.getBets()
    mockAccountHistory(
        Mono.fromSupplier({ accHistoryResponse })
        .subscribeOn(Schedulers.immediate()))
    when:
    controller.onConnect(client)
    then:
    accHistoryResponse.getBets().size() == 3
    1 * client.joinRoom(bppToken)
    1 * client.joinRoom("123")
    1 * client.joinRoom("456")
    1 * client.joinRoom(betWithCashoutNotAvailable.id)
    0 * client.joinRoom(_)
    1 * betUpdateService.createSubscriptionInInternalPubSub(sid, bppTokenWrapperMock, connDate, betThatServiceShouldSubscribeOn)
  }

  def "Internal subscription is removed on disconnect"() {
    when:
    controller.onDisconnect(client)
    then:
    1 * betUpdateService.unsubscribeInInternalPubSub(sid)
  }

  private static InitialAccountHistoryBetResponse accountHistoryResponse() {
    def model = new BetSummaryModel()
    model.id = "456"
    model.cashoutValue = "CASHOUT_SELN_SUSPENDED"
    def model2 = new BetSummaryModel()
    model2.id = "123"
    model2.cashoutValue = "2.0"
    def resp = [
      model,
      model2,
      betWithCashoutNotAvailable
    ]
    def paging = new Paging()
    paging.token = "abc"
    paging.blockSize = "20"

    def initAccResp = new InitialAccountHistoryBetResponse(resp,null, null, paging,"abc","1")

    return initAccResp
  }
  private SocketIOClient createSocketIoClientMock(UUID sid) {
    def client = Mock(SocketIOClient)
    client.getSessionId() >> sid
    def data = Mock(HandshakeData)
    data.getTime() >> connDate
    client.getHandshakeData() >> data
    return client
  }
  private SocketIOClient createClientMock(UUID sid, String bppToken) {
    def pagingBlockSize = "20"
    def group = "BET"
    def detailLevel = "DETAILED"
    def settled = "N"
    def fromDate = "2021-09-15 00:00:00"
    def toDate = "2021-09-21 23:59:59"
    def client = Mock(SocketIOClient)
    client.getSessionId() >> sid
    def data = Mock(HandshakeData)
    data.getSingleUrlParam("token") >> bppToken
    data.getSingleUrlParam("pagingBlockSize") >> pagingBlockSize
    data.getSingleUrlParam("group") >> group
    data.getSingleUrlParam("detailLevel") >> detailLevel
    data.getSingleUrlParam("settled") >> settled
    data.getSingleUrlParam("fromDate") >> fromDate
    data.getSingleUrlParam("toDate") >> toDate
    data.getTime() >> connDate
    client.getHandshakeData() >> data
    return client
  }

  def mockAccountHistory(Mono mono) {
    accountHistoryService.accountHistoryInitBets(_) >> mono
  }

  def mockCatchBlock(Mono mono) {
    bppTokenOperations.parseToken(bppToken) >> mono
  }
}
