package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "sportsfeaturedtab")
@Data
@EqualsAndHashCode(callSuper = true)
public class SportsFeaturedTab extends AbstractEntity {
  @NotBlank private String name;
  @NotBlank private String brand;
  @NotBlank private String path;
  private String categoryId;
  private List<SimpleModule> modules = new ArrayList<>();
  private boolean disabled;

  public Optional<SimpleModule> getModule(String id) {
    return modules.stream().filter(m -> m.getId().equals(id)).findAny();
  }
}
