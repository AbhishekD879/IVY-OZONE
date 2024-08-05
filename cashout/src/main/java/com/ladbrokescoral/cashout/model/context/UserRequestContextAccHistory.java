package com.ladbrokescoral.cashout.model.context;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.service.BetWithSelectionsModel;
import com.ladbrokescoral.cashout.service.UserRequestContextBuilder;
import java.time.Duration;
import java.util.Collection;
import java.util.Date;
import java.util.List;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserRequestContextAccHistory {
  private String username;
  private Duration tokenExpiresIn;
  private String token;
  private List<BetSummaryModel> userBets;
  private IndexedSportsData indexedData;
  private Date connectionDate;

  @Setter(AccessLevel.NONE)
  private List<String> settledBets;

  public static UserRequestContextBuilder builder() {
    return new UserRequestContextBuilder();
  }

  public boolean isBetSettled(BetWithSelectionsModel b) {
    return this.settledBets.contains(b.getOriginalBet().getId());
  }

  public void addSettledBets(Collection<String> settledBetIds) {
    settledBets.addAll(settledBetIds);
  }
}
