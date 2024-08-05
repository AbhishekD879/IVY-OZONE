package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "betreceiptbanners")
@Data
@EqualsAndHashCode(callSuper = true)
public class BetReceiptBanner extends BannerEntity implements HasBrand {

  private String fileUrl;
  private Boolean useUrl;
  private String directUrl;
  private Boolean useDirectUrl;
  private String directFileUrl;
  private Boolean useDirectFileUrl;
}
