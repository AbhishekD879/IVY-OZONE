package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.dto.BrandMenuItemDto;
import java.util.List;
import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "brandMenu")
@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class BrandMenuStructure extends SortableEntity implements HasBrand {

  @NotBlank private String brand;
  @Valid private List<BrandMenuItemDto> menu;
}
