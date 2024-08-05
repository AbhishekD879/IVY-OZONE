package com.coral.oxygen.middleware.pojos.model.output;

import com.coral.oxygen.middleware.pojos.model.cms.featured.Filename;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.io.Serializable;
import java.util.List;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;
import org.springframework.data.redis.core.index.Indexed;

@JsonInclude(JsonInclude.Include.NON_NULL)
@Data
@RedisHash(value = "${asset.management}", timeToLive = -1L)
public class AssetManagement implements Serializable {

  @Id private String id;
  @Indexed private Integer sportId;
  @Indexed private String teamName;
  private List<String> secondaryNames;
  private String primaryColour;
  private String secondaryColour;
  private boolean fiveASideToggle;
  private boolean highlightCarouselToggle;
  private Filename teamsImage;
}
