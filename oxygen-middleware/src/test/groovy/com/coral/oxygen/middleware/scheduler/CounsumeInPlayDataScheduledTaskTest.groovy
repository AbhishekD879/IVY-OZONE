package com.coral.oxygen.middleware.scheduler
import com.coral.oxygen.middleware.in_play.service.InPlayDataProcessor
import com.ladbrokescoral.lib.leader.LeaderStatus
import spock.lang.Specification

class CounsumeInPlayDataScheduledTaskTest extends Specification {
  private ConsumeInPlayDataScheduledTask task
  private LeaderStatus leaderStatus

  void setup() {
    leaderStatus = Mock(LeaderStatus)
    task = new ConsumeInPlayDataScheduledTask(Mock(InPlayDataProcessor), leaderStatus)
  }
  def "Exceptions in process task aren't propagated"() {
    given:
    leaderStatus.isLeaderNode() >> {args -> throw new RuntimeException()}
    when:
    task.process()
    then:
    noExceptionThrown()
  }

  def "Slave action test"() {
    given:
    LeaderStatus leaderStatus = new LeaderStatus()
    leaderStatus.setLeaderNode(false)
    leaderStatus.isLeaderNode() >> {args -> throw new RuntimeException()}
    when:
    task.process()
    then:
    noExceptionThrown()
  }
}
