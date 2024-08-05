package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import java.util.List;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "qeQuickLinks")
public class QEQuickLinks extends AbstractEntity implements HasBrand {

  @NotBlank private String brand;
  private String title;

  private List<QELink> links;
}
