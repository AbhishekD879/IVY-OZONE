package middleware.scheduler

import com.coral.oxygen.middleware.common.imdg.DistributedLock
import com.coral.oxygen.middleware.common.service.notification.MessagePublisher
import com.coral.oxygen.middleware.in_play.service.*
import com.coral.oxygen.middleware.in_play.service.config.InPlayDataProcessorConfig
import com.coral.oxygen.middleware.in_play.service.market.selector.MarketSelectorService
import com.coral.oxygen.middleware.scheduler.ConsumeInPlayDataScheduledTask
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.ladbrokescoral.lib.leader.LeaderStatus
import spock.lang.Specification

import java.util.concurrent.TimeUnit

class CounsumeInPlayDataScheduledTaskSpec extends Specification {
  ConsumeInPlayDataScheduledTask task
  InPlayDataProcessor dataProcessor

  InPlayDataConsumer consumer
  InPlayStorageService storageService
  MessagePublisher messagePublisher
  InplayLiveServerSubscriber inplayLiveServerSubscriber
  SiteServerApi siteServerApi
  DistributedLock lock
  MarketSelectorService marketSelectorService

  public static final Gson GSON = new GsonBuilder().setPrettyPrinting().create()


  def setup() throws InterruptedException {

    consumer = Mock(InPlayDataConsumer)
    storageService = Mock(InPlayStorageService)
    messagePublisher = Mock(MessagePublisher)
    inplayLiveServerSubscriber = Mock(InplayLiveServerSubscriber)
    siteServerApi = Mock(SiteServerApi)
    marketSelectorService = Mock(MarketSelectorService)

    InPlayDataProcessorConfig.InPlayDataProcessorBuilder builder =
        Mock(InPlayDataProcessorConfig.InPlayDataProcessorBuilder)
    builder.getStorageService() >> storageService
    builder.getMessagePublisher() >> messagePublisher
    builder.getConsumer() >> consumer
    builder.getGson() >> GSON
    builder.getInplayLiveServerSubscriber() >> inplayLiveServerSubscriber
    builder.getMarketSelectorService() >> marketSelectorService
    builder.getSiteServerApi() >> siteServerApi


    lock = Mock(DistributedLock)
    lock.tryLock(10, 10, TimeUnit.SECONDS) >> true
    LeaderStatus leaderStatus = new LeaderStatus()
    leaderStatus.setLeaderNode(true)
    dataProcessor = new InPlayDataProcessor(builder)
    task = new ConsumeInPlayDataScheduledTask(dataProcessor, leaderStatus)
  }
  def "Test exception saving is called when exception occurred"() throws InterruptedException {
    RuntimeException exception = new RuntimeException("Test error")
    consumer.consume() >> { throw exception }

    when:
    task.process()

    then:
    1 * storageService.saveError(exception)
  }
  def "Test slave action"() {
    given:
    LeaderStatus leaderStatus = new LeaderStatus()
    leaderStatus.setLeaderNode(false)
    when:
    task.process()
    then:
    noExceptionThrown()
  }
}
