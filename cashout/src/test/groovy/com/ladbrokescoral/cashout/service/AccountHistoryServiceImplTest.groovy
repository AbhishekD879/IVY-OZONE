package com.ladbrokescoral.cashout.service

import com.coral.bpp.api.model.bet.api.request.AccountHistoryRequest
import spock.lang.Specification

import java.time.Clock
import java.time.LocalDateTime
import java.time.Month
import java.time.ZoneOffset

class AccountHistoryServiceImplTest extends Specification {
  private BppService bppService = Mock(BppService)
  private AccountHistoryService service = new AccountHistoryServiceImpl(bppService, 20)

  def "Test detailed account history with open bets only (exclude settled)"() {
    given:
    def expectedRequest = AccountHistoryRequest.builder()
        .token("abc")
        .pagingBlockSize("20")
        .settled("N")
        .detailLevel("DETAILED")
        .group("BET")
        .fromDate("2019-02-10 20:10:05")
        .toDate("2020-02-11 20:10:05")
        .build()

    def instant = LocalDateTime.of(2020, Month.FEBRUARY, 10, 20, 10, 5).toInstant(ZoneOffset.UTC)
    service.setSystemUTC(Clock.fixed(instant, ZoneOffset.UTC))
    when:
    service.getDetailedAccountHistoryWithOpenBetsOnly("abc")
    then:
    1 * bppService.accountHistoryOpenBets(expectedRequest)
  }
}
