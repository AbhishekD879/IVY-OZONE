package com.ladbrokescoral.oxygen.betpackmp.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.util.ArrayList;
import java.util.List;
import lombok.Builder;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Builder(toBuilder = true)
@Accessors(chain = true)
@JsonIgnoreProperties(ignoreUnknown = true)
public class Promotion {
  private String id;
  private String brand;
  private String claimedDate;
  private String customerRef;
  private String offerName;
  private String campaignRef;
  private String campaignName;
  private String creationDate;
  private String expiryDate;
  private String rewardTypeRef;
  private String amount;
  private String currencyRef;
  private String accountNumber;
  private String activationDate;
  private String rewardRef;
  private String status;
  @Builder.Default private List<ExternalRef> externalUID = new ArrayList<>();
  @Builder.Default private List<String> gameGroupRefs = new ArrayList<>();
  @Builder.Default private List<String> betFlavourRefs = new ArrayList<>();
}
