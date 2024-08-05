package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import java.util.Map;
import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Positive;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class Upsell {

  /**
   * Assuming there're 4 Questions with 4 possible Answers each: { "questions[0].answers[0].id + ';'
   * + questions[1].answers[0].id": 11111111, // first selection id "questions[0].answers[0].id +
   * ';' + questions[1].answers[1].id": 22222222, // second selection id "questions[0].answers[0].id
   * + ';' + questions[1].answers[2].id": 33333333, // third selection id ...
   * "questions[2].answers[3].id + ';' + questions[3].answers[3].id": 16161616, // last selection id
   * }
   */
  @Valid private Map<@NotBlank String, @Positive Long> options;

  private Long defaultUpsellOption;
  private Filename fallbackImage;
  private String imageUrl;
}
