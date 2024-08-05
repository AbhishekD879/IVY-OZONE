package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import lombok.experimental.Accessors;
import org.hibernate.validator.constraints.SafeHtml;

@Data
@Accessors(chain = true)
public class SeoSitemapDto {
  @SafeHtml private String changefreq;
  private Double priority;
}
