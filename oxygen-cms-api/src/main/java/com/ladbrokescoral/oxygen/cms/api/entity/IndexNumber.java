package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.domain.Persistable;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "indexnumbers")
@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = {"id"})
public class IndexNumber implements Persistable<String> {

  @Id private String id;

  private String brand;

  private int indexNumber;

  @Override
  public boolean isNew() {
    return null == id;
  }
}
