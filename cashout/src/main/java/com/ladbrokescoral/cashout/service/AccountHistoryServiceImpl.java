package com.ladbrokescoral.cashout.service;

import com.coral.bpp.api.model.bet.api.request.AccountHistoryRequest;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.model.response.InitialAccountHistoryBetResponse;
import java.time.Clock;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class AccountHistoryServiceImpl implements AccountHistoryService {

  public static final DateTimeFormatter ACCOUNT_HISTORY_DATE_FORMAT =
      DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss").withZone(ZoneOffset.UTC);
  private BppService bppService;
  private final int defaultPagingBlockSize;
  private Clock systemUTC = Clock.systemUTC();

  @Autowired
  public AccountHistoryServiceImpl(
      BppService bppService,
      @Value("${accountHistoryRequest.pagingBlockSize:20}") int defaultPagingBlockSize) {
    this.bppService = bppService;
    this.defaultPagingBlockSize = defaultPagingBlockSize;
  }

  @Override
  public Mono<InitialAccountHistoryBetResponse> accountHistoryInitBets(
      AccountHistoryRequest accountHistoryRequest) {
    return bppService.accountHistory(accountHistoryRequest);
  }

  @Override
  public Mono<List<BetSummaryModel>> getDetailedAccountHistoryWithOpenBetsOnly(String bppToken) {
    return bppService.accountHistoryOpenBets(
        AccountHistoryRequest.builder()
            .token(bppToken)
            .pagingBlockSize(String.valueOf(defaultPagingBlockSize))
            .group("BET")
            .detailLevel("DETAILED")
            .settled("N")
            .fromDate(
                ACCOUNT_HISTORY_DATE_FORMAT.format(ZonedDateTime.now(systemUTC).minusYears(1)))
            .toDate(ACCOUNT_HISTORY_DATE_FORMAT.format(ZonedDateTime.now(systemUTC).plusDays(1)))
            .build());
  }

  // for testing
  protected void setSystemUTC(Clock clock) {
    this.systemUTC = clock;
  }
}
