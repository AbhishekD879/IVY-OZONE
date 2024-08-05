package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.MarketType;
import java.time.Instant;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class StatisticContentDto {

  @Id private String id;

  @NotBlank(message = "should not be blank")
  private String brand;

  @NotBlank(message = "should not be blank")
  private String title;

  private MarketType marketType = MarketType.OB;

  private String marketDescription;

  private String content;

  private Boolean enabled = Boolean.TRUE;

  @NotBlank(message = "should not be blank")
  private String eventId;

  @NotBlank(message = "should not be blank")
  private String marketId;

  @NotNull(message = "should not be null")
  private Instant startTime;

  @NotNull(message = "should not be null")
  private Instant endTime;
}
