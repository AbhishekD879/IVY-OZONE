package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackToken;
import com.ladbrokescoral.oxygen.cms.util.BetToken;
import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import lombok.AccessLevel;
import lombok.Data;
import lombok.Getter;

@Data
public class BetPackDto {
  private String id;
  @NotNull private String betPackId;
  @NotNull private String betPackTitle;
  @NotNull private String brand;

  @NotNull private Double betPackPurchaseAmount;

  @NotNull private Double betPackFreeBetsAmount;

  @NotNull
  @Size(max = 50, message = "BetPackFrontDisplayDescription should be max of 50 chars")
  private String betPackFrontDisplayDescription;

  @NotEmpty private List<String> sportsTag;
  @NotNull private Instant betPackStartDate;
  @NotNull private Instant betPackEndDate;
  @NotNull private boolean futureBetPack;
  @NotNull private boolean filterBetPack;
  private List<String> filterList;
  @NotNull private boolean betPackActive;

  @NotNull
  @Size(max = 25, message = "TriggerID should be max of 25 chars")
  private String triggerID;

  @BetToken private List<BetPackToken> betPackTokenList;

  @NotNull private boolean betPackSpecialCheckbox;
  @NotNull private String betPackMoreInfoText;
  @NotNull private Instant maxTokenExpirationDate;
  private Double sortOrder;
  private Integer maxClaims;

  @Getter(AccessLevel.NONE)
  @NotNull
  private boolean isLinkedBetPack;

  private String linkedBetPackWarningText;

  @JsonProperty("isLinkedBetPack")
  public boolean isLinkedBetPack() {
    return isLinkedBetPack;
  }
}
