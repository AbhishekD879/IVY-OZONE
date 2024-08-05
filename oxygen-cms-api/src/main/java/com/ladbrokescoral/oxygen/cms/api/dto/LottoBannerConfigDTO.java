package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.LottoConfig;
import java.util.List;
import javax.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
@AllArgsConstructor
public class LottoBannerConfigDTO {

  @NotNull private String globalBannerLink;
  @NotNull private String globalBannerText;
  private List<LottoConfig> lottoConfig;
  @NotNull private List<String> ids;
  private Integer dayCount;
}
