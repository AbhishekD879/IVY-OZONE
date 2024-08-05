package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "bankingmenus")
@Data
@EqualsAndHashCode(callSuper = true)
@CompoundIndex(name = "brand_linkTitle", def = "{'brand' : 1, 'linkTitle': 1}", unique = true)
public class BankingMenu extends RightMenu {}
