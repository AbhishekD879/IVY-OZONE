package com.ladbrokescoral.cashout.service;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.model.context.IndexedSportsData;
import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;
import java.time.Duration;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.CopyOnWriteArrayList;

public class UserRequestContextBuilder {

  private String username;
  private Duration tokenExpiresIn;
  private String token;
  private List<BetSummaryModel> userBets = Collections.emptyList();
  private Date connectionDate;

  public UserRequestContextBuilder token(String token) {
    Objects.requireNonNull(token);
    this.token = token;
    return this;
  }

  public UserRequestContextBuilder userBets(List<BetSummaryModel> bets) {
    Objects.requireNonNull(bets);
    this.userBets = bets;
    return this;
  }

  public UserRequestContextBuilder connectionDate(Date date) {
    Objects.requireNonNull(date);
    this.connectionDate = date;
    return this;
  }

  public UserRequestContextAccHistory build() {
    return new UserRequestContextAccHistory(
        username,
        tokenExpiresIn,
        token,
        userBets,
        IndexedSportsData.constructIndexedData(userBets),
        connectionDate,
        new CopyOnWriteArrayList<>());
  }

  public UserRequestContextBuilder username(String username) {
    this.username = username;
    return this;
  }

  public UserRequestContextBuilder tokenExpiresIn(Duration timeLeftToExpire) {
    this.tokenExpiresIn = timeLeftToExpire;
    return this;
  }
}
