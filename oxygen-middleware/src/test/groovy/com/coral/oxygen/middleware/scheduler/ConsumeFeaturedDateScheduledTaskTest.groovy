package com.coral.oxygen.middleware.scheduler

import com.coral.oxygen.middleware.featured.consumer.FeaturedDataConsumer
import com.coral.oxygen.middleware.featured.service.FeaturedDataProcessor
import com.ladbrokescoral.lib.leader.LeaderStatus
import spock.lang.Specification

class ConsumeFeaturedDateScheduledTaskTest extends Specification {
  private ConsumeFeaturedDateScheduledTask task
  private LeaderStatus leaderStatus

  void setup() {
    leaderStatus = Mock(LeaderStatus)
    task = new ConsumeFeaturedDateScheduledTask(Mock(FeaturedDataConsumer),
        Mock(FeaturedDataProcessor),
        this.leaderStatus)
  }
  def "Exceptions in process task aren't propagated"() {
    given:
    leaderStatus.isLeaderNode() >> {args -> throw new RuntimeException()}
    when:
    task.process()
    then:
    noExceptionThrown()
  }

  def "Test the 'process' method when leaderStatus is true"() {
    given:
    def featuredDataConsumer = Mock(FeaturedDataConsumer)
    def dataProcessor = Mock(FeaturedDataProcessor)
    LeaderStatus leaderStatus = new LeaderStatus()
    leaderStatus.setLeaderNode(true)
    ConsumeFeaturedDateScheduledTask localTask = new ConsumeFeaturedDateScheduledTask(Mock(FeaturedDataConsumer),
        Mock(FeaturedDataProcessor),
        leaderStatus)
    when:
    localTask.process()

    then:
    noExceptionThrown()
  }
  def "Test the 'process' method when leaderStatus is false"() {
    given:
    LeaderStatus leaderStatus = new LeaderStatus()
    leaderStatus.setLeaderNode(false)
    ConsumeFeaturedDateScheduledTask localTask = new ConsumeFeaturedDateScheduledTask(Mock(FeaturedDataConsumer),
        Mock(FeaturedDataProcessor),
        leaderStatus)
    when:
    localTask.process()

    then:
    noExceptionThrown()
  }
}
