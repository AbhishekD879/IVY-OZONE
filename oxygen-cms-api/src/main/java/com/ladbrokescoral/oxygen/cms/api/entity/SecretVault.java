package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonView;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.view.Views;
import java.io.Serializable;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.domain.Persistable;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "secretvault")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SecretVault implements Persistable<String>, Serializable {

  @Id
  @JsonView(Views.GetAll.class)
  private String key;

  private String value;

  @Override
  public String getId() {
    return key;
  }

  @Override
  public boolean isNew() {
    return false;
  }
}
