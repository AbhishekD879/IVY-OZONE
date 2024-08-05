package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import org.springframework.web.multipart.MultipartFile;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Data
public class QuestionDetailsImages {

  private String questionId;
  private MultipartFile homeSvg;
  private MultipartFile awaySvg;
  private MultipartFile channel;
}
