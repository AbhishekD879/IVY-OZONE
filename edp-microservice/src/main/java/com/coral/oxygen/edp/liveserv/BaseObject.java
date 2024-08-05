package com.coral.oxygen.edp.liveserv;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.math.BigInteger;
import java.util.Date;
import java.util.List;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.Accessors;

@Getter
@Setter
public class BaseObject {

  @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "MMM dd, yyyy h:mm:ss a")
  private Date publishedDate;

  private String type;
  private Event event;

  @Getter
  @Setter
  @Accessors(chain = true)
  public static class Event {

    private Integer eventId;
    private Market market;
    private Scoreboard scoreboard;
    private Clock clock;

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

    @JsonProperty("start_time_xls") //
    private Name startTimeXls;

    @JsonProperty("suspend_at")
    private String suspendAt; // : "",

    @JsonProperty("is_off")
    private String isOff; // : "Y",

    @JsonProperty("started")
    private String started; // : "Y",

    @JsonProperty("race_stage")
    private String raceStage; // : "",

    private String eventFlagCodes;
  }

  @Getter
  @Setter
  @Accessors(chain = true)
  public static class Market {

    private Outcome outcome;

    private BigInteger marketId;

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

    @JsonProperty("ev_id")
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

    private String flags;
  }

  @Getter
  @Setter
  @Accessors(chain = true)
  public static class Outcome {
    @JsonProperty("ev_mkt_id")
    private BigInteger evMktId;

    @JsonProperty("names")
    private Name name;

    private String status;

    private String settled;

    private String result;

    private String displayed;

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

    @JsonProperty("hasPriceStream")
    private boolean hasPriceStream;

    private Price price;
  }

  @Getter
  @Setter
  public static class Scoreboard {

    @JsonProperty("min_periods")
    private Integer minPeriods;

    @JsonProperty("ALL")
    private List<EventDetails> all;

    @JsonProperty("SUBPERIOD")
    private List<EventDetails> subperiod;

    @JsonProperty("CURRENT")
    private List<EventDetails> current;
  }

  @Getter
  @Setter
  public static class EventDetails {
    @JsonProperty("ev_id")
    private Integer evId;

    @JsonProperty("ev_class_id")
    private Integer evClassId;

    @JsonProperty("period_code")
    private String periodCode;

    @JsonProperty("code")
    private String score;

    @JsonProperty("value")
    private String value;

    @JsonProperty("participant_id")
    private String participantId;

    @JsonProperty("role_code")
    private String roleCode;

    @JsonProperty("period_index")
    private String periodIndex;

    @JsonProperty("is_active")
    private String isActive;

    public EventDetails() {}

    public EventDetails(String roleCode, String value) {
      this.roleCode = roleCode;
      this.value = value;
    }

    public static EventDetails createHomeEventDetails(Integer value) {
      return new EventDetails("HOME", String.valueOf(value));
    }

    public static EventDetails createAwayEventDetails(Integer value) {
      return new EventDetails("AWAY", String.valueOf(value));
    }
  }

  @Getter
  @Setter
  public static class Name {
    @JsonProperty("en")
    private String en;
  }

  @Getter
  @Setter
  @Accessors(chain = true)
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
  }

  @Getter
  @Setter
  private static class Collection {
    @JsonProperty("collection_id")
    private String collectionId;
  }

  @Getter
  @Setter
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
  }

  @Getter
  @Setter
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
  }
}
