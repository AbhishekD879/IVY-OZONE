package com.ladbrokescoral.oxygen.cms.api.service.bpp.specialPages;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.io.Serializable;
import java.util.List;
import lombok.*;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class TierInfoDTO implements Serializable {
  private static final long serialVersionUID = 8700132876665387314L;

  private String tierName;
  private List<String> offerIdSeq;
  private List<Integer> freeBetPositionSequence;
}
