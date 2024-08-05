package com.ladbrokescoral.oxygen.cms.api.service.bpp.specialPages;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.io.Serializable;
import java.time.Instant;
import java.util.List;
import lombok.*;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class SpecialPageDTO implements Serializable {
  private static final long serialVersionUID = 8700132876665387314L;
  private String pageName;
  private String brand;

  @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
      timezone = "UTC")
  private Instant startDate;

  @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
      timezone = "UTC")
  private Instant endDate;

  private List<TierInfoDTO> tierInfo;
  private String howItWorks;
  private String termsAndConditions;
  private String fullTermsURI;
}
