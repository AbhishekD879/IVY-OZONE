package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class CouponMarketSelectorDto {
  @Id private String id;
  private String title;
  private String templateMarketName;
  private List<String> header;
}
