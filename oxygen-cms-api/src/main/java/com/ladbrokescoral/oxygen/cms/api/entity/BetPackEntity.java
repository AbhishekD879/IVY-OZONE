package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.ladbrokescoral.oxygen.cms.util.BetToken;
import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Data
@Document(collection = "betpack-marketplace")
@EqualsAndHashCode(callSuper = false)
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
@SuppressWarnings("java:S1820")
public class BetPackEntity extends SortableEntity implements HasBrand {
  @Indexed(unique = true)
  @NotNull
  private String betPackId;

  @NotNull private String betPackTitle;
  @NotNull private String brand;
  @NotNull private Double betPackPurchaseAmount;
  @NotNull private Double betPackFreeBetsAmount;
  @NotNull private String betPackFrontDisplayDescription;
  @NotEmpty private List<String> sportsTag;
  @NotNull private Instant betPackStartDate;
  @NotNull private Instant betPackEndDate;
  @NotNull private boolean futureBetPack;
  @NotNull private boolean filterBetPack;
  private List<String> filterList;
  @NotNull private boolean betPackActive;
  @NotNull private String triggerID;
  @BetToken private List<BetPackToken> betPackTokenList;
  @NotNull private boolean betPackSpecialCheckbox;
  @NotNull private String betPackMoreInfoText;
  @NotNull private Instant maxTokenExpirationDate;
  private Integer maxClaims;

  private boolean isLinkedBetPack;
  private String linkedBetPackWarningText;
}
