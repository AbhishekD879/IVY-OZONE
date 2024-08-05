package com.ladbrokescoral.oxygen.cms.api.dto;

import com.egalacoral.spark.siteserver.model.Event;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.ContestPrize;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.PrizePool;
import java.time.Instant;
import java.util.List;
import lombok.Data;
import org.wildfly.common.annotation.NotNull;

@Data
public class ContestRequest {

  private String intialContestId;
  @NotNull private String name;
  private Filename icon;
  @NotNull private Instant startDate;
  private String event;
  @NotNull private String entryStake;

  @JsonProperty("isFreeBetsAllowed")
  private boolean freeBetsAllowed = true;

  private PrizePool prizePool;

  private List<ContestPrize> contestPrizes;

  private String sponsorText;
  private Filename sponsorLogo;
  private String maxEntries;
  private String maxEntriesPerUser;

  private String description;
  private String blurb;
  private String entryConfirmationText;
  private String nextContestId;
  private boolean display = false;
  private String brand;
  private boolean realAccount = true;
  private boolean testAccount;
  private boolean completed;
  private Instant utcStartDate;
  // to save events
  @JsonInclude(value = JsonInclude.Include.NON_EMPTY, content = JsonInclude.Include.NON_NULL)
  private List<Event> events;

  private boolean reportGenerated;
  private String entriesSize;
  private boolean enableServiceMsg;
  private String serviceMsg;

  @JsonProperty("isInvitationalContest")
  private boolean invitationalContest;

  @JsonProperty("isPrivateContest")
  private boolean privateContest;

  private String contestURL;
  private boolean crmPrizeIndicator = true;
  private String freebetOfferId;
  private String ticketOfferId;
}
