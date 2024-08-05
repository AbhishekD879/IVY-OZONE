package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "betreceiptbannertablets")
@Data
@EqualsAndHashCode(callSuper = true)
public class BetReceiptBannerTablet extends BannerEntity implements HasBrand {}
