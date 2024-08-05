package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.Pattern;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = EventHub.COLLECTION_NAME)
@Data
@EqualsAndHashCode(callSuper = true)
@CompoundIndex(name = "brand_index_number", def = "{'brand' : 1, 'indexNumber': 1}", unique = true)
public class EventHub extends SortableEntity implements HasBrand {

  public static final String COLLECTION_NAME = "eventhubs";

  @Brand private String brand;

  private Boolean disabled = false;

  @NotEmpty
  @Pattern(regexp = "^[a-zA-Z0-9_ ]*$", message = "should contain only letters, digits and spaces")
  private String title;

  @NotEmpty private Integer indexNumber;
}
