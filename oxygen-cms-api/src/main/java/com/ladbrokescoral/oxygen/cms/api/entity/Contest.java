package com.ladbrokescoral.oxygen.cms.api.entity;

import com.egalacoral.spark.siteserver.model.Event;
import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.Instant;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;
import org.wildfly.common.annotation.NotNull;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "contests")
@Data
@EqualsAndHashCode(callSuper = true)
public class Contest extends SortableEntity implements HasBrand {

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
