package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
public class PopularAccaWidgetDto extends AbstractDto {
  private String title;
  private String cardCta;
  private String cardCtaAfterAdd;
  private List<PopularAccaWidgetDataDto> data = new ArrayList<>();
  private Map<String, Boolean> displayOn = new HashMap<>();
  private Map<Integer, String> categoryIds = new HashMap<>();
}
