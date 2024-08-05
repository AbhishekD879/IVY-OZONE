package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "posts")
@Data
@EqualsAndHashCode(callSuper = true)
public class Post extends AbstractEntity {

  private String slug;
  private String title;
  private List<PostCategory> categories;
  private String state;
}
