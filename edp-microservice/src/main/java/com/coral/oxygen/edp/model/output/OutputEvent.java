package com.coral.oxygen.edp.model.output;

import static java.util.stream.Collectors.toList;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.math.BigInteger;
import java.util.Collection;
import java.util.List;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.util.CollectionUtils;

@Slf4j
@Builder(toBuilder = true)
@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class OutputEvent {

  private Long id;
  private Long millisUntilStart;
  private Integer marketsCount;
  private String name;
  private String nameOverride;
  private BigInteger outcomeId;
  private Boolean outcomeStatus;
  private String eventSortCode;
  private String startTime;
  private String liveServChannels;
  private String liveServChildrenChannels;
  private String liveServLastMsgId;
  private String categoryId;
  private String categoryCode;
  private String categoryName;
  private String className;

  private String typeName;
  private String cashoutAvail;
  private String eventStatusCode;
  private String classId;
  private Boolean isUS;

  private Boolean eventIsLive;
  private Integer displayOrder;

  private List<OutputMarket> markets;

  private Comment comments;
  private Boolean isStarted;
  private Boolean isFinished;

  private Boolean outright;
  private String responseCreationTime;
  private boolean liveStreamAvailable;
  protected String drilldownTagNames;
  protected String typeId;
  private String eventFlagCodes;

  private Clock initClock;

  @JsonIgnore private String ssName;

  @Getter(AccessLevel.NONE)
  @JsonIgnore
  private Collection<List<OutputMarket>> marketsByTemplateMarket;

  public OutputEvent getCopyWithMarketLimit(int marketLimit) {
    OutputEvent result = this.toBuilder().build();
    if (!CollectionUtils.isEmpty(marketsByTemplateMarket)) {
      result.setMarkets(
          marketsByTemplateMarket.stream()
              .limit(marketLimit)
              .flatMap(Collection::stream)
              .collect(toList()));
    } else {
      result.setMarkets(
          this.getMarkets().subList(0, marketsCount < marketLimit ? marketsCount : marketLimit));
    }
    return result;
  }
}
