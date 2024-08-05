package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.dto.BrandMenuItemDto;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

public class QuestionEngineMenuUpdate extends AbstractBrandMongoUpdate {

  public void initQuestionEngineMenu(MongockTemplate mongockTemplate, String brand) {
    updateBrandMenu(
        mongockTemplate,
        brand,
        BrandMenuItemDto.builder()
            .active(true)
            .path("/question-engine")
            .label("Question Engine")
            .icon("extension")
            .subMenu(initQuestionEngineMenuItems())
            .id(UUID.randomUUID().toString())
            .build());
  }

  private List<BrandMenuItemDto> initQuestionEngineMenuItems() {
    return Arrays.asList(
        createBrandMenuItemBuilder("Quiz", "/question-engine/quiz").build(),
        createBrandMenuItemBuilder("Splash Page", "/question-engine/splash-pages").build());
  }
}
