package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.math.BigInteger;
import java.util.List;
import java.util.Map;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/** Created by Aliaksei Yarotski on 9/19/17. */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class BaseObject {
  private String publishedDate; // pattern = "MMM dd, yyyy H:mm:ss A"
  private String type;
  private Event event;

  @Data
  @Builder
  @NoArgsConstructor
  @AllArgsConstructor
  @JsonInclude(JsonInclude.Include.NON_NULL)
  public static class Event {

    private Integer eventId;
    @JsonProperty private ScoreBoardStats scoreBoardStats;
    private Market market;
    private Scoreboard scoreboard;
    private Clock clock;
    private Name names;
    private String status; // : "A",
    private String displayed; // : "Y",

    @JsonProperty("result_conf")
    private String resultConf; // : "N",

    @JsonProperty("disporder")
    private Integer displayOrder; // : 0,

    @JsonProperty("start_time")
    private String startTime; // : "2017-09-21 12:30:00",

    @JsonProperty("start_time_xls")
    private Name startTimeXls;

    @JsonProperty("suspend_at")
    private String suspendAt; // : "",

    @JsonProperty("is_off")
    private String isOff; // : "Y",

    private String started; // : "Y",

    @JsonProperty("race_stage")
    private String raceStage; // : "",

    private String eventFlagCodes;
  }

  @Data
  @Builder
  @NoArgsConstructor
  @AllArgsConstructor
  @JsonInclude(Include.NON_NULL)
  public static class ScoreBoardStats {
    @JsonProperty private Map<String, Object> stats;
  }

  @Data
  @Builder
  @NoArgsConstructor
  @AllArgsConstructor
  @JsonInclude(JsonInclude.Include.NON_NULL)
  public static class Market {

    private Outcome outcome;
    private Integer marketId;
    private Name names;

    @JsonProperty("group_names")
    private Name groupNames;

    @JsonProperty("ev_oc_grp_id")
    private String evOcGroupId;

    @JsonProperty("mkt_disp_code")
    private String dispCode;

    @JsonProperty("mkt_disp_layout_columns")
    private String dispLayoutColumns;

    @JsonProperty("mkt_disp_layout_order")
    private String dispLayoutOrder;

    @JsonProperty("mkt_type")
    private String type;

    @JsonProperty("mkt_sort")
    private String sort;

    @JsonProperty("mkt_grp_flags")
    private String groupFlags;

    @JsonProperty("ev_id")
    private Integer eventId;

    private String status; // : "A",
    private String displayed; // : "Y",
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

    private List<Collection> collections;

    private String flags;
  }

  @Data
  @Builder
  @NoArgsConstructor
  @AllArgsConstructor
  @JsonInclude(JsonInclude.Include.NON_NULL)
  public static class Outcome {
    @JsonProperty("ev_mkt_id")
    private Integer marketId;

    private Name names;
    private String status;
    private String settled;
    private String result;
    private String displayed;
    private Integer disporder;

    @JsonProperty("runner_num")
    private String runnerNumber;

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

    private BigInteger outcomeId;
    private boolean hasPriceStream;
    private Price price;
  }

  @Data
  @JsonInclude(JsonInclude.Include.NON_NULL)
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

  @Data
  @JsonInclude(JsonInclude.Include.NON_NULL)
  public static class EventDetails {
    @JsonProperty("ev_id")
    private Integer eventId;

    @JsonProperty("ev_class_id")
    private Integer classId;

    @JsonProperty("period_code")
    private String periodCode;

    private String code;
    private String value;

    @JsonProperty("participant_id")
    private String participantId;

    @JsonProperty("role_code")
    private String roleCode;

    @JsonProperty("period_index")
    private String periodIndex;

    @JsonProperty("is_active")
    private String isActive;
  }

  @Data
  @JsonInclude(JsonInclude.Include.NON_NULL)
  public static class Name {
    private String en;
  }

  @Data
  @JsonInclude(JsonInclude.Include.NON_NULL)
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

  @Data
  @JsonInclude(JsonInclude.Include.NON_NULL)
  private static class Collection {
    @JsonProperty("collection_id")
    private String collectionId;
  }

  @Data
  @JsonInclude(JsonInclude.Include.NON_NULL)
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

  @Data
  @JsonInclude(JsonInclude.Include.NON_NULL)
  public static class Clock {
    @JsonProperty("ev_id")
    private Integer eventId;

    @JsonProperty("last_update")
    private String lastUpdate;

    @JsonProperty("period_code")
    private String periodCode;

    @JsonProperty("period_index")
    private String periodIndex;

    private String state;

    @JsonProperty("clock_seconds")
    private String clockSeconds;

    @JsonProperty("last_update_secs")
    private String lastUpdateSeconds;

    @JsonProperty("start_time_secs")
    private String startTimeSeconds;

    @JsonProperty("offset_secs")
    private String offsetSeconds;
  }
}
