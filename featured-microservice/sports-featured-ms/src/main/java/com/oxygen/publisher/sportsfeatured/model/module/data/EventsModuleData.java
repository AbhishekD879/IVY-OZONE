package com.oxygen.publisher.sportsfeatured.model.module.data;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.JsonSerializer;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.databind.ser.std.NullSerializer;
import com.oxygen.publisher.model.AssetManagementDto;
import com.oxygen.publisher.model.Clock;
import com.oxygen.publisher.model.Comment;
import com.oxygen.publisher.model.OutputMarket;
import com.oxygen.publisher.model.RacingFormEvent;
import java.io.IOException;
import java.math.BigInteger;
import java.util.Collection;
import java.util.List;
import java.util.UUID;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.SneakyThrows;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "uniqueId")
public class EventsModuleData extends AbstractModuleData {
  private String uniqueId;
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
  /*As part BMA-62182  new Fields at event level added from OB end to capture the same we have added
  below teamExtIds homeTeamExtIds awayTeamExtIds fields */
  private String teamExtIds;
  private String homeTeamExtIds;
  private String awayTeamExtIds;
  private Boolean eventIsLive;
  private Integer displayOrder;
  private List<OutputMarket> markets;

  @JsonProperty(access = JsonProperty.Access.WRITE_ONLY)
  @JsonSerialize(using = NullSerializer.class)
  private List<OutputMarket> primaryMarkets;

  private Comment comments;
  private Boolean isStarted;
  private Boolean isFinished;
  private Boolean outright;
  private String responseCreationTime;
  private boolean liveStreamAvailable;
  private String drilldownTagNames;
  private String typeFlagCodes;
  private String typeId;
  // BMA-62182: This property helps to holds the multiple TypeIds.
  private List<String> typeIds;
  private Clock initClock;
  private String ssName;
  private boolean buildYourBetAvailable;
  private String effectiveGpStartTime;

  @JsonInclude(Include.NON_NULL)
  private RacingFormEvent racingFormEvent;

  private String eventFlagCodes;

  @Setter @Getter private Collection<AssetManagementDto> assetManagements;

  private String bwinId;

  private Boolean bybAvailableEvent;

  /**
   * While sending the content to FE, EventsModuleData should be given a new UniqueID otherwise when
   * we have more than one HC contains the same Event then JsonIdentityInfo comes into place and
   * only first instance of EventsModuleData is going to be generated as a complete Object.
   *
   * @return clone of EventsModuleData
   */
  @SneakyThrows
  public final EventsModuleData cloneWithNewUniqueId() {
    EventsModuleData result = cloneEventModuleData();
    result.setUniqueId(UUID.randomUUID().toString());
    return result;
  }

  public EventsModuleData cloneEventModuleData() throws CloneNotSupportedException {

    return (EventsModuleData) this.clone();
  }

  /** It's required to return numeric id to the client for EventModuleData. */
  @Override
  @JsonSerialize(using = StringToLongSerializer.class)
  public String getId() {
    return super.getId();
  }

  private static class StringToLongSerializer extends JsonSerializer<String> {

    @Override
    public void serialize(String value, JsonGenerator generator, SerializerProvider serializers)
        throws IOException {
      generator.writeNumber(Long.parseLong(value));
    }
  }
}
