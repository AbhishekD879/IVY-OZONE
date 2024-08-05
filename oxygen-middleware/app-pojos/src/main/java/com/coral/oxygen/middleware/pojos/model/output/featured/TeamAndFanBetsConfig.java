package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.cms.featured.TeamAndFanBets;
import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class TeamAndFanBetsConfig<T extends TeamAndFanBets> extends AbstractModuleData {
  private Integer noOfMaxSelections;
  private boolean enableBackedTimes;
  private List<String> fanzoneSegments;

  public TeamAndFanBetsConfig(T bets) {
    this.noOfMaxSelections = bets.getNoOfMaxSelections();
    this.enableBackedTimes = bets.isEnableBackedTimes();
  }

  @ChangeDetect
  public Integer getNoOfMaxSelections() {
    return noOfMaxSelections;
  }

  @ChangeDetect
  public List<String> getFanzoneSegments() {
    return fanzoneSegments;
  }

  @ChangeDetect
  public boolean isEnableBackedTimes() {
    return Boolean.TRUE.equals(enableBackedTimes);
  }

  public void setEnableBackedTimes(Boolean enableBackedTimes) {
    this.enableBackedTimes = enableBackedTimes;
  }
}
