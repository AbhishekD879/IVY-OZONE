package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.time.Instant;
import java.util.List;
import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "specialPages")
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class EuroLoyal extends SpecialPage {

  private Instant startDate;
  private Instant endDate;
  private List<TierInfo> tierInfo;
  private String howItWorks;
  private String termsAndConditions;
  private String fullTermsURI;
}
