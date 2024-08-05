package com.coral.oxygen.middleware.pojos.model.output;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.IdHolder;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.math.BigInteger;
import java.util.*;
import lombok.*;

@SuppressWarnings("java:S2157")
@ToString(callSuper = false)
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "uniqueId")
public class EventsModuleData extends AbstractModuleData
    implements IdHolder, Serializable, Cloneable {

  @SerializedName("@type")
  @JsonProperty("@type")
  protected String type = "EventsModuleData";

  private String uniqueId;
  private Long id;
  private Integer marketsCount;
  private String name;
  private String nameOverride;
  private BigInteger outcomeId;
  private Long marketId;
  private Boolean outcomeStatus;
  private String eventSortCode;
  private String startTime;
  private String liveServChannels;
  private String liveServChildrenChannels;
  private String liveServLastMsgId;
  private String categoryId;
  private String categoryCode;
  private String categoryName;
  private String classId;
  private String className;
  private String typeName;
  private String cashoutAvail;
  private String eventStatusCode;
  private Boolean isUS;
  /*As part BMA-62182  new Fields at event level added from OB end to capture the same we have added
  below teamExtIds homeTeamExtIds awayTeamExtIds fields*/
  private String teamExtIds;
  private String homeTeamExtIds;
  private String awayTeamExtIds;
  private Boolean eventIsLive;
  private Integer displayOrder;
  private List<OutputMarket> markets;
  private List<OutputMarket> primaryMarkets;

  private Comment comments;
  private InplayScoreBoardStats scoreBoardStats;
  private Boolean isStatsAvailable;
  private Boolean isStarted;
  private Boolean isFinished;

  private Boolean outright;
  private String responseCreationTime;
  private boolean liveStreamAvailable;
  protected String drilldownTagNames;
  private String typeFlagCodes;
  protected String typeId;

  private Clock initClock;
  private String eventFlagCodes;

  protected boolean buildYourBetAvailable;

  private transient String ssName;
  private RacingFormEvent racingFormEvent;

  private String effectiveGpStartTime;

  private Set<String> moduleIds = new HashSet<>();

  public EventsModuleData() {
    this.uniqueId = UUID.randomUUID().toString();
  }

  @Setter @Getter private Collection<AssetManagement> assetManagements;

  private String bwinId;

  private Boolean bybAvailableEvent;

  public String getBwinId() {
    return bwinId;
  }

  public void setBwinId(String bwinId) {
    this.bwinId = bwinId;
  }

  public Boolean getBybAvailableEvent() {
    return bybAvailableEvent;
  }

  public void setBybAvailableEvent(Boolean bybAvailableEvent) {
    this.bybAvailableEvent = bybAvailableEvent;
  }

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public String getUniqueId() {
    return uniqueId;
  }

  public void setUniqueId(String uniqueId) {
    this.uniqueId = uniqueId;
  }

  @ChangeDetect
  public boolean isBuildYourBetAvailable() {
    return buildYourBetAvailable;
  }

  public void setBuildYourBetAvailable(boolean buildYourBetAvailable) {
    this.buildYourBetAvailable = buildYourBetAvailable;
  }

  @ChangeDetect
  public Integer getMarketsCount() {
    return marketsCount;
  }

  public void setMarketsCount(Integer marketsCount) {
    this.marketsCount = marketsCount;
  }

  @ChangeDetect
  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  @ChangeDetect
  public String getNameOverride() {
    return nameOverride;
  }

  public void setNameOverride(String nameOverride) {
    this.nameOverride = nameOverride;
  }

  @ChangeDetect
  public BigInteger getOutcomeId() {
    return outcomeId;
  }

  @ChangeDetect
  public Long getMarketId() {
    return marketId;
  }

  public void setOutcomeId(BigInteger outcomeId) {
    this.outcomeId = outcomeId;
  }

  @ChangeDetect
  public boolean isOutcomeStatus() {
    return Boolean.TRUE.equals(outcomeStatus);
  }

  public void setOutcomeStatus(Boolean outcomeStatus) {
    this.outcomeStatus = outcomeStatus;
  }

  @ChangeDetect
  public String getEventSortCode() {
    return eventSortCode;
  }

  public void setEventSortCode(String eventSortCode) {
    this.eventSortCode = eventSortCode;
  }

  @ChangeDetect
  public String getStartTime() {
    return startTime;
  }

  public void setStartTime(String startTime) {
    this.startTime = startTime;
  }

  @ChangeDetect
  public String getLiveServChannels() {
    return liveServChannels;
  }

  public void setLiveServChannels(String liveServChannels) {
    this.liveServChannels = liveServChannels;
  }

  @ChangeDetect
  public String getLiveServChildrenChannels() {
    return liveServChildrenChannels;
  }

  public void setLiveServChildrenChannels(String liveServChildrenChannels) {
    this.liveServChildrenChannels = liveServChildrenChannels;
  }

  @ChangeDetect
  public String getLiveServLastMsgId() {
    return liveServLastMsgId;
  }

  public void setLiveServLastMsgId(String liveServLastMsgId) {
    this.liveServLastMsgId = liveServLastMsgId;
  }

  @ChangeDetect
  public String getCategoryId() {
    return categoryId;
  }

  public void setCategoryId(String categoryId) {
    this.categoryId = categoryId;
  }

  @ChangeDetect
  public String getCategoryCode() {
    return categoryCode;
  }

  public void setCategoryCode(String categoryCode) {
    this.categoryCode = categoryCode;
  }

  @ChangeDetect
  public String getCategoryName() {
    return categoryName;
  }

  public void setCategoryName(String categoryName) {
    this.categoryName = categoryName;
  }

  @ChangeDetect
  public String getClassId() {
    return classId;
  }

  public void setClassId(String classId) {
    this.classId = classId;
  }

  @ChangeDetect
  public String getClassName() {
    return className;
  }

  public void setClassName(String className) {
    this.className = className;
  }

  @ChangeDetect
  public String getTypeName() {
    return typeName;
  }

  public void setTypeName(String typeName) {
    this.typeName = typeName;
  }

  @ChangeDetect
  public String getCashoutAvail() {
    return cashoutAvail;
  }

  public void setCashoutAvail(String cashoutAvail) {
    this.cashoutAvail = cashoutAvail;
  }

  @JsonProperty(value = "isUS")
  @ChangeDetect
  public Boolean getUS() {
    return isUS;
  }

  public void setUS(Boolean isUS) {
    this.isUS = isUS;
  }

  @ChangeDetect
  public Boolean getEventIsLive() {
    return eventIsLive;
  }

  public void setEventIsLive(Boolean eventIsLive) {
    this.eventIsLive = eventIsLive;
  }

  @ChangeDetect(compareCollection = true)
  public List<OutputMarket> getMarkets() {
    return markets == null ? Collections.emptyList() : markets;
  }

  public void setMarkets(List<OutputMarket> markets) {
    if (markets != null) {
      this.markets = new ArrayList<>(markets);
    }
  }

  public List<OutputMarket> getPrimaryMarkets() {
    return primaryMarkets == null ? Collections.emptyList() : primaryMarkets;
  }

  public void setPrimaryMarkets(List<OutputMarket> primaryMarkets) {
    if (primaryMarkets != null) {
      this.primaryMarkets = new ArrayList<>(primaryMarkets);
    }
  }

  @ChangeDetect(minor = true)
  public Comment getComments() {
    return comments;
  }

  public void setComments(Comment comments) {
    this.comments = comments;
  }

  public void setScoreBoardStats(InplayScoreBoardStats scoreBoardStats) {
    this.scoreBoardStats = scoreBoardStats;
  }

  public InplayScoreBoardStats getScoreBoardStats() {
    return scoreBoardStats;
  }

  @ChangeDetect
  public Integer getDisplayOrder() {
    return displayOrder;
  }

  public void setDisplayOrder(Integer displayOrder) {
    this.displayOrder = displayOrder;
  }

  public String getType() {
    return type;
  }

  public void setType(String type) {
    this.type = type;
  }

  public String getTeamExtIds() {
    return teamExtIds;
  }

  public void setTeamExtIds(String teamExtIds) {
    this.teamExtIds = teamExtIds;
  }

  public String getHomeTeamExtIds() {
    return homeTeamExtIds;
  }

  public void setHomeTeamExtIds(String homeTeamExtIds) {
    this.homeTeamExtIds = homeTeamExtIds;
  }

  public String getAwayTeamExtIds() {
    return awayTeamExtIds;
  }

  public void setAwayTeamExtIds(String awayTeamExtIds) {
    this.awayTeamExtIds = awayTeamExtIds;
  }

  @JsonProperty(value = "isStatsAvailable")
  @ChangeDetect
  public Boolean getStatsAvailable() {
    return isStatsAvailable;
  }

  public void setStatsAvailable(Boolean statsAvailable) {
    isStatsAvailable = statsAvailable;
  }

  @JsonProperty(value = "isStarted")
  @ChangeDetect
  public Boolean getStarted() {
    return isStarted;
  }

  public void setStarted(Boolean started) {
    isStarted = started;
  }

  public boolean isOutright() {
    return Boolean.TRUE.equals(outright);
  }

  public void setOutright(Boolean outright) {
    this.outright = outright;
  }

  public String getResponseCreationTime() {
    return responseCreationTime;
  }

  public void setResponseCreationTime(String responseCreationTime) {
    this.responseCreationTime = responseCreationTime;
  }

  @ChangeDetect
  public boolean isLiveStreamAvailable() {
    return liveStreamAvailable;
  }

  public void setLiveStreamAvailable(boolean liveStreamAvailable) {
    this.liveStreamAvailable = liveStreamAvailable;
  }

  @JsonProperty(value = "isFinished")
  @ChangeDetect
  public Boolean getFinished() {
    return isFinished;
  }

  public void setFinished(Boolean finished) {
    isFinished = finished;
  }

  @ChangeDetect
  public String getDrilldownTagNames() {
    return drilldownTagNames;
  }

  public void setDrilldownTagNames(String drilldownTagNames) {
    this.drilldownTagNames = drilldownTagNames;
  }

  @ChangeDetect
  public String getTypeFlagCodes() {
    return typeFlagCodes;
  }

  public void setTypeFlagCodes(String typeFlagCodes) {
    this.typeFlagCodes = typeFlagCodes;
  }

  @ChangeDetect
  public String getTypeId() {
    return typeId;
  }

  public void setTypeId(String typeId) {
    this.typeId = typeId;
  }

  @ChangeDetect
  public String getEventStatusCode() {
    return eventStatusCode;
  }

  public void setEventStatusCode(String eventStatusCode) {
    this.eventStatusCode = eventStatusCode;
  }

  public Clock getInitClock() {
    return initClock;
  }

  public void setInitClock(Clock initClock) {
    this.initClock = initClock;
  }

  public String getSsName() {
    return ssName;
  }

  public void setSsName(String ssName) {
    this.ssName = ssName;
  }

  @Override
  public String idForChangeDetection() {
    return id.toString();
  }

  public void setRacingFormEvent(RacingFormEvent racingFormEvent) {
    this.racingFormEvent = racingFormEvent;
  }

  public RacingFormEvent getRacingFormEvent() {
    return racingFormEvent;
  }

  public Set<String> getModuleIds() {
    return moduleIds;
  }

  public void addModuleId(String moduleId) {
    this.moduleIds.add(moduleId);
  }

  public String getEffectiveGpStartTime() {
    return effectiveGpStartTime;
  }

  public void setEffectiveGpStartTime(String effectiveGpStartTime) {
    this.effectiveGpStartTime = effectiveGpStartTime;
  }

  public String getEventFlagCodes() {
    return eventFlagCodes;
  }

  public void setEventFlagCodes(String eventFlagCodes) {
    this.eventFlagCodes = eventFlagCodes;
  }

  @SneakyThrows
  public final EventsModuleData cloneWithNewUniqueId() {
    EventsModuleData result = cloneEventModuleData();
    result.setUniqueId(UUID.randomUUID().toString());
    return result;
  }

  public void setMarketId(long marketId) {

    this.marketId = marketId;
  }

  public EventsModuleData cloneEventModuleData() throws CloneNotSupportedException {

    return (EventsModuleData) this.clone();
  }
}
