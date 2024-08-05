package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import lombok.Builder;
import lombok.EqualsAndHashCode;
import lombok.Singular;
import lombok.ToString;

@EqualsAndHashCode(callSuper = true)
@ToString
public class ModularIdsContentDto extends BaseModularContentDto {
  @Singular
  @JsonProperty("eventsIds")
  private List<Integer> eventsIds;

  @Singular
  @JsonProperty("outcomesIds")
  private List<BigInteger> outcomesIds;

  @Singular
  @JsonProperty("enhMultiplesIds")
  private List<Integer> enhMultiplesIds;

  @Singular
  @JsonProperty("typeIds")
  private List<Integer> typeIds;

  @Singular
  @JsonProperty("racingEventsIds")
  private List<Integer> racingEventsIds;

  @Singular
  @JsonProperty("marketIds")
  private List<Integer> marketIds;

  @Builder(toBuilder = true)
  public ModularIdsContentDto(
      SportPageId sportPageId,
      List<Integer> eventsIds,
      List<BigInteger> outcomesIds,
      List<Integer> enhMultiplesIds,
      List<Integer> typeIds,
      List<Integer> racingEventsIds,
      List<Integer> marketIds) {
    this.sportPageId = sportPageId;
    this.eventsIds = eventsIds;
    this.outcomesIds = outcomesIds;
    this.enhMultiplesIds = enhMultiplesIds;
    this.typeIds = typeIds;
    this.racingEventsIds = racingEventsIds;
    this.marketIds = marketIds;
  }

  public ModularIdsContentDto addEventsIdsItem(Integer eventsIdsItem) {
    if (this.eventsIds == null) {
      this.eventsIds = new ArrayList<>();
    }
    this.eventsIds.add(eventsIdsItem);
    return this;
  }

  /**
   * Get eventsIds
   *
   * @return eventsIds
   */
  public List<Integer> getEventsIds() {
    return eventsIds;
  }

  public ModularIdsContentDto addOutcomesIdsItem(BigInteger outcomesIdsItem) {
    if (this.outcomesIds == null) {
      this.outcomesIds = new ArrayList<>();
    }
    this.outcomesIds.add(outcomesIdsItem);
    return this;
  }

  /**
   * Get outcomesIds
   *
   * @return outcomesIds
   */
  public List<BigInteger> getOutcomesIds() {
    return outcomesIds;
  }

  public ModularIdsContentDto addEnhMultiplesIdsItem(Integer enhMultiplesIdsItem) {
    if (this.enhMultiplesIds == null) {
      this.enhMultiplesIds = new ArrayList<>();
    }
    this.enhMultiplesIds.add(enhMultiplesIdsItem);
    return this;
  }

  /**
   * Get enhMultiplesIds
   *
   * @return enhMultiplesIds
   */
  public List<Integer> getEnhMultiplesIds() {
    return enhMultiplesIds;
  }

  public ModularIdsContentDto addTypeIdsItem(Integer typeIdsItem) {
    if (this.typeIds == null) {
      this.typeIds = new ArrayList<>();
    }
    this.typeIds.add(typeIdsItem);
    return this;
  }

  /**
   * Get typeIds
   *
   * @return typeIds
   */
  public List<Integer> getTypeIds() {
    return typeIds;
  }

  public ModularIdsContentDto addRacingEventsIdsItem(Integer racingEventsIdsItem) {
    if (this.racingEventsIds == null) {
      this.racingEventsIds = new ArrayList<>();
    }
    this.racingEventsIds.add(racingEventsIdsItem);
    return this;
  }

  /**
   * Get racingEventsIds
   *
   * @return racingEventsIds
   */
  public List<Integer> getRacingEventsIds() {
    return racingEventsIds;
  }

  public List<Integer> getMarketIds() {
    return marketIds;
  }

  public ModularIdsContentDto addMarketIdsItem(Integer marketIdsItem) {
    if (this.marketIds == null) {
      this.marketIds = new ArrayList<>();
    }
    this.marketIds.add(marketIdsItem);
    return this;
  }
}
