package com.ladbrokescoral.oxygen.buildyourbetms.util

import com.ladbrokescoral.oxygen.buildyourbetms.dto.LeaguesUpcomingDto
import spock.lang.Specification

class UtilTest extends Specification {

  def "test aggregate"() {
    given:
    def l1 = null
    def l2 = null
    when:
    def result = Util.aggregate(l1, l2)
    then:
    result == LeaguesUpcomingDto.builder().build();
  }

  def "today is null, upcoming is not"() {
    given:
    def l1 = LeaguesUpcomingDto.builder()
        .today(null)
        .upcoming(TestUtils.createLeagues(1L, 2L))
        .build();
    def l2 = LeaguesUpcomingDto.builder()
        .today(TestUtils.createLeagues(1L, 2L))
        .upcoming(null)
        .build();
    when:
    def result = Util.aggregate(l1, l2);
    then:
    def expected = LeaguesUpcomingDto.builder()
        .today(TestUtils.createLeagues(1L, 2L))
        .upcoming(TestUtils.createLeagues(1L, 2L))
        .build()
    result.getToday().sort()
    result.getUpcoming().sort()

    result == expected;
  }

  def "works"() {
    given:
    def l1 = LeaguesUpcomingDto.builder()
        .today(TestUtils.createLeagues(1L, 2L))
        .upcoming(TestUtils.createLeagues(2L, 3L))
        .build()
    def l2 = LeaguesUpcomingDto.builder()
        .today(TestUtils.createLeagues(4L, 5L))
        .upcoming(TestUtils.createLeagues(7L, 8L))
        .build()
    when:
    def result = Util.aggregate(l1, l2)
    then:
    def expected = LeaguesUpcomingDto.builder()
        .today(TestUtils.createLeagues(1L, 2L, 4L, 5L))
        .upcoming(TestUtils.createLeagues(2L, 3L, 7L, 8L))
        .build()
    result.getToday().sort()
    result.getUpcoming().sort()
    result == expected
  }
}
