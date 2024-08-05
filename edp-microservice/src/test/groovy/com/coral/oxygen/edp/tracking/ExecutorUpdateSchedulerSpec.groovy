package com.coral.oxygen.edp.tracking

import com.coral.oxygen.edp.tracking.model.CategoryToUpcomingEvent
import spock.lang.Specification

class ExecutorUpdateSchedulerSpec extends Specification {

  UpdateScheduler updateScheduler
  Tracker<String, CategoryToUpcomingEvent> tracker = Mock()

  def setup() {
    updateScheduler = new ExecutorUpdateScheduler()
    updateScheduler.setTracker(tracker)
  }

  def "Test single scheduling"() {
    when: 'schedule refresh in one second'
    updateScheduler.schedule(0)
    sleep(200)
    then: 'trackers refreshData is called'
    1 * tracker.refreshData()
  }

  def "Test only one schedule will be triggered at the same second"() {
    when: 'schedule 2 refresh calls'
    updateScheduler.schedule(2000)
    updateScheduler.schedule(2000)
    sleep(2200)
    then: '#refreshData() is called only once'
    1 * tracker.refreshData()
  }
}
