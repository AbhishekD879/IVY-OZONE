package com.egalacoral.spark.liveserver;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.scoreboards.parser.api.YesNo;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.Accessors;

/** Created by Aliaksei Yarotski on 9/19/17. */
@JsonIgnoreProperties(ignoreUnknown = true)
public class BaseObject {

  @JsonProperty
  @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss.SSS")
  private Date publishedDate;

  @JsonProperty private String type;
  @JsonProperty private Event event;

  public void setPublishedDate(Date publishedDate) {
    this.publishedDate = publishedDate;
  }

  public Date getPublishedDate() {
    return publishedDate;
  }

  public void setType(String type) {
    this.type = type;
  }

  public String getType() {
    return type;
  }

  public void setEvent(Event event) {
    this.event = event;
  }

  public Event getEvent() {
    return event;
  }

  public static class Event {

    @JsonProperty private BigInteger eventId;

    @JsonProperty private ScoreBoardStats scoreBoardStats;
    @JsonProperty private Market market;
    @JsonProperty private Scoreboard scoreboard;
    @JsonProperty private Clock clock;

    @JsonProperty("names")
    private Name name;

    @JsonProperty("status")
    private String status; // : "A",

    @JsonProperty("displayed") // : "Y",
    private String displayed;

    @JsonProperty("result_conf") // : "N",
    private String resultConf;

    @JsonProperty("disporder")
    private Integer disporder; // : 0,

    @JsonProperty("start_time") // : "2017-09-21 12:30:00",
    private String startTime;

    @JsonProperty("start_time_xls")
    private Name startTimeXls;

    @JsonProperty("suspend_at")
    private String suspendAt; // : "",

    @JsonProperty("is_off")
    private String isOff; // : "Y",

    @JsonProperty("started")
    private String started; // : "Y",

    @JsonProperty("race_stage")
    private String raceStage; // : "",

    public String getDisplayed() {
      return displayed;
    }

    public void setDisplayed(String displayed) {
      this.displayed = displayed;
    }

    public String getResultConf() {
      return resultConf;
    }

    public void setResultConf(String resultConf) {
      this.resultConf = resultConf;
    }

    public Integer getDisporder() {
      return disporder;
    }

    public void setDisporder(Integer disporder) {
      this.disporder = disporder;
    }

    public String getStartTime() {
      return startTime;
    }

    public void setStartTime(String startTime) {
      this.startTime = startTime;
    }

    public Name getStartTimeXls() {
      return startTimeXls;
    }

    public void setStartTimeXls(Name startTimeXls) {
      this.startTimeXls = startTimeXls;
    }

    public String getSuspendAt() {
      return suspendAt;
    }

    public void setSuspendAt(String suspendAt) {
      this.suspendAt = suspendAt;
    }

    public String getIsOff() {
      return isOff;
    }

    public void setIsOff(String isOff) {
      this.isOff = isOff;
    }

    public String getStarted() {
      return started;
    }

    public void setStarted(String started) {
      this.started = started;
    }

    public String getRaceStage() {
      return raceStage;
    }

    public void setRaceStage(String raceStage) {
      this.raceStage = raceStage;
    }

    public String getStatus() {
      return status;
    }

    public void setStatus(String status) {
      this.status = status;
    }

    public Name getName() {
      return name;
    }

    public void setName(Name name) {
      this.name = name;
    }

    public Event eventId(BigInteger eventId) {
      this.eventId = eventId;
      return this;
    }

    public BigInteger getEventId() {
      return eventId;
    }

    public void setEventId(BigInteger eventId) {
      this.eventId = eventId;
    }

    public void setScoreBoardStats(ScoreBoardStats scoreBoardStats) {
      this.scoreBoardStats = scoreBoardStats;
    }

    public ScoreBoardStats getScoreBoardStats() {
      return scoreBoardStats;
    }

    public Event scoreBoardStats(ScoreBoardStats scoreBoardStats) {
      this.scoreBoardStats = scoreBoardStats;
      return this;
    }

    public Event market(Market market) {
      this.market = market;
      return this;
    }

    public Market getMarket() {
      return market;
    }

    public void setMarket(Market market) {
      this.market = market;
    }

    public Event scoreboard(Scoreboard scoreboard) {
      this.scoreboard = scoreboard;
      return this;
    }

    public Scoreboard getScoreboard() {
      return scoreboard;
    }

    public void setScoreboard(Scoreboard scoreboard) {
      this.scoreboard = scoreboard;
    }

    public Event clock(Clock clock) {
      this.clock = clock;
      return this;
    }

    public Clock getClock() {
      return clock;
    }

    public void setClock(Clock clock) {
      this.clock = clock;
    }
  }

  public static class ScoreBoardStats {

    @JsonProperty private Map<String, Object> stats;

    public void setStats(Map<String, Object> stats) {
      this.stats = stats;
    }

    public Map<String, Object> getStats() {
      return stats;
    }
  }

  public static class Market {

    @JsonProperty private Outcome outcome;
    @JsonProperty private Integer marketId;

    @JsonProperty("names")
    private Name name;

    @JsonProperty("group_names")
    private Name groupNames;

    @JsonProperty("ev_oc_grp_id")
    private String evOcGrpId;

    @JsonProperty("mkt_disp_code")
    private String mktDispCode;

    @JsonProperty("mkt_disp_layout_columns")
    private String mktDispLayoutColumns;

    @JsonProperty("mkt_disp_layout_order")
    private String mktDispLayoutOrder;

    @JsonProperty("mkt_type")
    private String mktType;

    @JsonProperty("mkt_sort")
    private String mktSort;

    @JsonProperty("mkt_grp_flags")
    private String mktGrpFlags;

    @JsonProperty(value = "ev_id")
    private Integer evId;

    @JsonProperty("status")
    private String status; // : "A",

    @JsonProperty("displayed")
    private String displayed; // : "Y",

    @JsonProperty("disporder")
    private Integer disporder;

    @JsonProperty("bir_index")
    private String birIndex;

    @JsonProperty("raw_hcap")
    private String rawHcap;

    @JsonProperty("hcap_values")
    private HcapValues hcapValues;

    @JsonProperty("ew_avail")
    private String ewAvail;

    @JsonProperty("ew_places")
    private String ewPlaces;

    @JsonProperty("ew_fac_num")
    private String ewFacNum;

    @JsonProperty("ew_fac_den")
    private String ewFacDen;

    @JsonProperty("bet_in_run")
    private String betInRun;

    @JsonProperty("lp_avail")
    private String lpAvail;

    @JsonProperty("sp_avail")
    private String spAvail;

    @JsonProperty("mm_coll_id")
    private String mmCollId;

    @JsonProperty("suspend_at")
    private String suspendAt;

    @JsonProperty("collections")
    private List<Collection> collections;

    public Market outcome(Outcome outcome) {
      this.outcome = outcome;
      return this;
    }

    public Outcome getOutcome() {
      return outcome;
    }

    public void setOutcome(Outcome outcome) {
      this.outcome = outcome;
    }

    public Market marketId(Integer marketId) {
      this.marketId = marketId;
      return this;
    }

    public Integer getMarketId() {
      return marketId;
    }

    public void setMarketId(Integer marketId) {
      this.marketId = marketId;
    }

    public Name getName() {
      return name;
    }

    public void setName(Name name) {
      this.name = name;
    }

    public Name getGroupNames() {
      return groupNames;
    }

    public void setGroupNames(Name groupNames) {
      this.groupNames = groupNames;
    }

    public String getEvOcGrpId() {
      return evOcGrpId;
    }

    public void setEvOcGrpId(String evOcGrpId) {
      this.evOcGrpId = evOcGrpId;
    }

    public String getMktDispCode() {
      return mktDispCode;
    }

    public void setMktDispCode(String mktDispCode) {
      this.mktDispCode = mktDispCode;
    }

    public String getMktDispLayoutColumns() {
      return mktDispLayoutColumns;
    }

    public void setMktDispLayoutColumns(String mktDispLayoutColumns) {
      this.mktDispLayoutColumns = mktDispLayoutColumns;
    }

    public String getMktDispLayoutOrder() {
      return mktDispLayoutOrder;
    }

    public void setMktDispLayoutOrder(String mktDispLayoutOrder) {
      this.mktDispLayoutOrder = mktDispLayoutOrder;
    }

    public String getMktType() {
      return mktType;
    }

    public void setMktType(String mktType) {
      this.mktType = mktType;
    }

    public String getMktSort() {
      return mktSort;
    }

    public void setMktSort(String mktSort) {
      this.mktSort = mktSort;
    }

    public String getMktGrpFlags() {
      return mktGrpFlags;
    }

    public void setMktGrpFlags(String mktGrpFlags) {
      this.mktGrpFlags = mktGrpFlags;
    }

    public Integer getEvId() {
      return evId;
    }

    public void setEvId(Integer evId) {
      this.evId = evId;
    }

    public String getStatus() {
      return status;
    }

    public void setStatus(String status) {
      this.status = status;
    }

    public String getDisplayed() {
      return displayed;
    }

    public void setDisplayed(String displayed) {
      this.displayed = displayed;
    }

    public Integer getDisporder() {
      return disporder;
    }

    public void setDisporder(Integer disporder) {
      this.disporder = disporder;
    }

    public String getBirIndex() {
      return birIndex;
    }

    public void setBirIndex(String birIndex) {
      this.birIndex = birIndex;
    }

    public String getRawHcap() {
      return rawHcap;
    }

    public void setRawHcap(String rawHcap) {
      this.rawHcap = rawHcap;
    }

    public HcapValues getHcapValues() {
      return hcapValues;
    }

    public void setHcapValues(HcapValues hcapValues) {
      this.hcapValues = hcapValues;
    }

    public String getEwAvail() {
      return ewAvail;
    }

    public void setEwAvail(String ewAvail) {
      this.ewAvail = ewAvail;
    }

    public String getEwPlaces() {
      return ewPlaces;
    }

    public void setEwPlaces(String ewPlaces) {
      this.ewPlaces = ewPlaces;
    }

    public String getEwFacNum() {
      return ewFacNum;
    }

    public void setEwFacNum(String ewFacNum) {
      this.ewFacNum = ewFacNum;
    }

    public String getEwFacDen() {
      return ewFacDen;
    }

    public void setEwFacDen(String ewFacDen) {
      this.ewFacDen = ewFacDen;
    }

    public String getBetInRun() {
      return betInRun;
    }

    public void setBetInRun(String betInRun) {
      this.betInRun = betInRun;
    }

    public String getLpAvail() {
      return lpAvail;
    }

    public void setLpAvail(String lpAvail) {
      this.lpAvail = lpAvail;
    }

    public String getSpAvail() {
      return spAvail;
    }

    public void setSpAvail(String spAvail) {
      this.spAvail = spAvail;
    }

    public String getMmCollId() {
      return mmCollId;
    }

    public void setMmCollId(String mmCollId) {
      this.mmCollId = mmCollId;
    }

    public String getSuspendAt() {
      return suspendAt;
    }

    public void setSuspendAt(String suspendAt) {
      this.suspendAt = suspendAt;
    }

    public List<Collection> getCollections() {
      return collections;
    }

    public void setCollections(List<Collection> collections) {
      this.collections = collections;
    }
  }

  public static class Outcome {
    @JsonProperty("ev_mkt_id")
    private Integer evMktId;

    @JsonProperty("names")
    private Name name;

    @JsonProperty("status")
    private String status;

    @JsonProperty("settled")
    private String settled;

    @JsonProperty("result")
    private String result;

    @JsonProperty("displayed")
    private String displayed;

    @JsonProperty("disporder")
    private Integer disporder;

    @JsonProperty("runner_num")
    private String runnerNum;

    @JsonProperty("fb_result")
    private String fbResult;

    @JsonProperty("lp_num")
    private String lpNum;

    @JsonProperty("lp_den")
    private String lpDen;

    @JsonProperty("cs_home")
    private String csHome;

    @JsonProperty("cs_away")
    private String csAway;

    @JsonProperty("unique_id")
    private String uniqueId;

    @JsonProperty("outcomeId")
    private BigInteger outcomeId;

    @JsonProperty("price")
    private Price price;

    public Outcome outcomeId(BigInteger outcomeId) {
      this.outcomeId = outcomeId;
      return this;
    }

    public BigInteger getOutcomeId() {
      return outcomeId;
    }

    public void setOutcomeId(BigInteger outcomeId) {
      this.outcomeId = outcomeId;
    }

    public Outcome price(Price price) {
      this.price = price;
      return this;
    }

    public Price getPrice() {
      return price;
    }

    public void setPrice(Price price) {
      this.price = price;
    }

    public Integer getEvMktId() {
      return evMktId;
    }

    public void setEvMktId(Integer evMktId) {
      this.evMktId = evMktId;
    }

    public Name getName() {
      return name;
    }

    public void setName(Name name) {
      this.name = name;
    }

    public String getStatus() {
      return status;
    }

    public void setStatus(String status) {
      this.status = status;
    }

    public String getSettled() {
      return settled;
    }

    public void setSettled(String settled) {
      this.settled = settled;
    }

    public String getResult() {
      return result;
    }

    public void setResult(String result) {
      this.result = result;
    }

    public String getDisplayed() {
      return displayed;
    }

    public void setDisplayed(String displayed) {
      this.displayed = displayed;
    }

    public Integer getDisporder() {
      return disporder;
    }

    public void setDisporder(Integer disporder) {
      this.disporder = disporder;
    }

    public String getRunnerNum() {
      return runnerNum;
    }

    public void setRunnerNum(String runnerNum) {
      this.runnerNum = runnerNum;
    }

    public String getFbResult() {
      return fbResult;
    }

    public void setFbResult(String fbResult) {
      this.fbResult = fbResult;
    }

    public String getLpNum() {
      return lpNum;
    }

    public void setLpNum(String lpNum) {
      this.lpNum = lpNum;
    }

    public String getLpDen() {
      return lpDen;
    }

    public void setLpDen(String lpDen) {
      this.lpDen = lpDen;
    }

    public String getCsHome() {
      return csHome;
    }

    public void setCsHome(String csHome) {
      this.csHome = csHome;
    }

    public String getCsAway() {
      return csAway;
    }

    public void setCsAway(String csAway) {
      this.csAway = csAway;
    }

    public String getUniqueId() {
      return uniqueId;
    }

    public void setUniqueId(String uniqueId) {
      this.uniqueId = uniqueId;
    }
  }

  public static class Scoreboard {

    @JsonProperty("min_periods")
    private Integer minPeriods;

    @JsonProperty("ALL")
    private List<EventDetails> all;

    @JsonProperty("SUBPERIOD")
    private List<EventDetails> subperiod;

    @JsonProperty("CURRENT")
    private List<EventDetails> current;

    public Integer getMinPeriods() {
      return minPeriods;
    }

    public void setMinPeriods(Integer minPeriods) {
      this.minPeriods = minPeriods;
    }

    public List<EventDetails> getAll() {
      return all;
    }

    public List<EventDetails> all() {
      if (all == null) {
        all = new ArrayList<>();
      }
      return all;
    }

    public void setAll(List<EventDetails> all) {
      this.all = all;
    }

    public List<EventDetails> getSubperiod() {
      return subperiod;
    }

    public void setSubperiod(List<EventDetails> subperiod) {
      this.subperiod = subperiod;
    }

    public List<EventDetails> getCurrent() {
      return current;
    }

    public List<EventDetails> current() {
      if (current == null) {
        current = new ArrayList<>();
      }
      return current;
    }

    public List<EventDetails> subperiod() {
      if (subperiod == null) {
        subperiod = new ArrayList<>();
      }
      return subperiod;
    }

    public void setCurrent(List<EventDetails> current) {
      this.current = current;
    }
  }

  @Getter
  @Setter
  @AllArgsConstructor(access = AccessLevel.PRIVATE)
  public static class EventDetails {
    @JsonProperty("ev_id")
    private Integer evId;

    @JsonProperty("ev_class_id")
    private Integer evClassId;

    @JsonProperty("period_code")
    private String periodCode;

    @JsonProperty("code")
    private String code;

    @JsonProperty("value")
    private String value;

    @JsonProperty("participant_id")
    private String participantId;

    @JsonProperty("role_code")
    private String roleCode;

    @JsonProperty("period_index")
    private String periodIndex;

    @JsonProperty("is_active")
    private YesNo active;

    private EventDetails(String roleCode) {
      this.roleCode = roleCode;
    }

    public static EventDetailsBuilder builder() {
      return new EventDetailsBuilder();
    }

    @Setter
    @Accessors(fluent = true)
    public static class EventDetailsBuilder {
      private static final String SCORE_CODE = "SCORE";

      private Integer evId;
      private Integer evClassId;
      private String periodCode;
      private String code;
      private String value;
      private String participantId;
      private String periodIndex;
      private YesNo active;

      EventDetailsBuilder() {}

      public EventDetails buildHomeEventScore() {
        return new EventDetails(
            evId,
            evClassId,
            periodCode,
            SCORE_CODE,
            value,
            participantId,
            "HOME",
            periodIndex,
            active);
      }

      public EventDetails buildAwayEventScore() {
        return new EventDetails(
            evId,
            evClassId,
            periodCode,
            SCORE_CODE,
            value,
            participantId,
            "AWAY",
            periodIndex,
            active);
      }
    }
  }

  public static class Name {
    @JsonProperty("en")
    private String en;

    public String getEn() {
      return en;
    }

    public void setEn(String en) {
      this.en = en;
    }
  }

  public static class Price {
    @JsonProperty("lp_den")
    @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
    private String lpDen;

    @JsonProperty("lp_num")
    @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
    private String lpNum;

    @JsonProperty("ps_den")
    @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
    private String psDen;

    @JsonProperty("ps_num")
    @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
    private String psNum;

    @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
    private String status;

    @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
    @JsonProperty("stream_type")
    private String priceStreamType;

    public String getLpDen() {
      return lpDen;
    }

    public void setLpDen(String lpDen) {
      this.lpDen = lpDen;
    }

    public String getLpNum() {
      return lpNum;
    }

    public void setLpNum(String lpNum) {
      this.lpNum = lpNum;
    }

    public Price lpDen(String lpDen) {
      this.lpDen = lpDen;
      return this;
    }

    public Price lpNum(String lpNum) {
      this.lpNum = lpNum;
      return this;
    }

    public String getPsDen() {
      return psDen;
    }

    public void setPsDen(String psDen) {
      this.psDen = psDen;
    }

    public String getPsNum() {
      return psNum;
    }

    public void setPsNum(String psNum) {
      this.psNum = psNum;
    }

    public Price psDen(String psDen) {
      this.psDen = psDen;
      return this;
    }

    public Price psNum(String psNum) {
      this.psNum = psNum;
      return this;
    }

    public String getStatus() {
      return status;
    }

    public void setStatus(String status) {
      this.status = status;
    }

    public String getPriceStreamType() {
      return priceStreamType;
    }

    public void setPriceStreamType(String priceStreamType) {
      this.priceStreamType = priceStreamType;
    }
  }

  private static class Collection {
    @JsonProperty("collection_id")
    private String collectionId;

    public String getCollectionId() {
      return collectionId;
    }

    public void setCollectionId(String collectionId) {
      this.collectionId = collectionId;
    }
  }

  public static class HcapValues {
    @JsonProperty("H")
    private String h;

    @JsonProperty("A")
    private String a;

    @JsonProperty("B")
    private String b;

    @JsonProperty("L")
    private String l;

    @JsonProperty("E")
    private String e;

    public String getH() {
      return h;
    }

    public void setH(String h) {
      this.h = h;
    }

    public String getA() {
      return a;
    }

    public void setA(String a) {
      this.a = a;
    }

    public String getB() {
      return b;
    }

    public void setB(String b) {
      this.b = b;
    }

    public String getL() {
      return l;
    }

    public void setL(String l) {
      this.l = l;
    }

    public String getE() {
      return e;
    }

    public void setE(String e) {
      this.e = e;
    }
  }

  public static class Clock {
    @JsonProperty("ev_id")
    private Integer evId;

    @JsonProperty("last_update")
    private String lastUpdate;

    @JsonProperty("period_code")
    private String periodCode;

    @JsonProperty("period_index")
    private String periodIndex;

    @JsonProperty("state")
    private String state;

    @JsonProperty("clock_seconds")
    private String clockSeconds;

    @JsonProperty("last_update_secs")
    private String lastUpdateSecs;

    @JsonProperty("start_time_secs")
    private String startTimeSecs;

    @JsonProperty("offset_secs")
    private String offsetSecs;

    public void setEvId(Integer evId) {
      this.evId = evId;
    }

    public Integer getEvId() {
      return evId;
    }

    public String getLastUpdate() {
      return lastUpdate;
    }

    public void setLastUpdate(String lastUpdate) {
      this.lastUpdate = lastUpdate;
    }

    public String getPeriodCode() {
      return periodCode;
    }

    public void setPeriodCode(String periodCode) {
      this.periodCode = periodCode;
    }

    public String getPeriodIndex() {
      return periodIndex;
    }

    public void setPeriodIndex(String periodIndex) {
      this.periodIndex = periodIndex;
    }

    public String getState() {
      return state;
    }

    public void setState(String state) {
      this.state = state;
    }

    public String getClockSeconds() {
      return clockSeconds;
    }

    public void setClockSeconds(String clockSeconds) {
      this.clockSeconds = clockSeconds;
    }

    public String getLastUpdateSecs() {
      return lastUpdateSecs;
    }

    public void setLastUpdateSecs(String lastUpdateSecs) {
      this.lastUpdateSecs = lastUpdateSecs;
    }

    public String getStartTimeSecs() {
      return startTimeSecs;
    }

    public void setStartTimeSecs(String startTimeSecs) {
      this.startTimeSecs = startTimeSecs;
    }

    public String getOffsetSecs() {
      return offsetSecs;
    }

    public void setOffsetSecs(String offsetSecs) {
      this.offsetSecs = offsetSecs;
    }
  }
}
