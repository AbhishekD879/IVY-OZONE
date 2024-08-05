package com.oxygen.publisher.model;

import static com.oxygen.publisher.model.PageType.customized;
import static org.assertj.core.api.Assertions.assertThat;

import org.junit.Test;

public class PageTypeTest {

  @Test
  public void shouldParseCustomizedPageId() {
    // given
    Integer expectedSport = 0;
    String prefix = customized.getPrefix();
    String pageId = prefix + expectedSport;

    // when
    Integer receivedSportId = customized.getHandler().getSportId(pageId);

    // then
    assertThat(receivedSportId).isEqualTo(expectedSport);
  }
}
