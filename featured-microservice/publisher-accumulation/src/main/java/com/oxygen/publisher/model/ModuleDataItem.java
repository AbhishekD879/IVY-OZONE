package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.databind.ser.std.NullSerializer;
import java.math.BigInteger;
import java.util.Collection;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Represents the Module Data Item model. Copied from Middleware Service.
 *
 * @author tvuyiv
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ModuleDataItem {

  private Integer id;
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
  private String classId;
  private String className;
  private String typeName;
  private String cashoutAvail;
  private String eventStatusCode;
  private Boolean isUS;
  private Boolean eventIsLive;
  private Integer displayOrder;
  private List<OutputMarket> markets;

  @JsonInclude(JsonInclude.Include.NON_EMPTY)
  private String marketSelector;

  @JsonProperty(access = JsonProperty.Access.WRITE_ONLY)
  @JsonSerialize(using = NullSerializer.class)
  private List<OutputMarket> primaryMarkets;

  private Comment comments;
  private InplayScoreBoardStats scoreBoardStats;
  private Boolean isStatsAvailable;
  private Boolean isStarted;
  private Boolean isFinished;
  private Boolean outright;
  private String responseCreationTime;
  private boolean liveStreamAvailable;
  private String drilldownTagNames;
  private String typeFlagCodes;
  private String typeId;
  private Clock initClock;
  private String ssName;
  private RacingFormEvent racingFormEvent;

  @Setter @Getter private Collection<AssetManagementDto> assetManagements;

  public ModuleDataItem(Integer id, String name, String startTime, String typeId) {
    this.id = id;
    this.name = name;
    this.startTime = startTime;
    this.typeId = typeId;
  }

  public List<OutputMarket> getPrimaryMarkets() {
    return primaryMarkets;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    if (!super.equals(o)) return false;

    ModuleDataItem that = (ModuleDataItem) o;

    return id.equals(that.id);
  }

  @Override
  public int hashCode() {
    int result = super.hashCode();
    result = 31 * result + id.hashCode();
    return result;
  }

  @JsonIgnore
  public ModuleDataItem cloneWithEmptyHREventTypes() {
    return new ModuleDataItem(id, name, startTime, typeId);
  }
}
