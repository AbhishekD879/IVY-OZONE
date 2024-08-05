package com.ladbrokescoral.oxygen.questionengine.service.impl;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.from;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.collect.ImmutableMap;
import com.ladbrokescoral.oxygen.questionengine.configuration.properties.ApplicationProperties;
import com.ladbrokescoral.oxygen.questionengine.dto.AbstractQuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.UpsellDto;
import com.ladbrokescoral.oxygen.questionengine.dto.UpsellPriceDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.UpsellConfigurationDto;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import org.apache.commons.io.IOUtils;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class UpsellServiceTest {

  @Mock
  private SiteServerApi siteServerApi;
  private UpsellServiceImpl upsellService;
  private Event event;

  @Before
  public void setUp() throws IOException {
    ApplicationProperties applicationProperties = new ApplicationProperties();
    applicationProperties.setSiteServerSelectionIdsLimit(2);
    upsellService = new UpsellServiceImpl(applicationProperties, siteServerApi);

    event = new ObjectMapper().readValue(
        IOUtils.toString(getClass().getResourceAsStream("/ss/__files/outcomes.json"), "UTF-8"), Event.class);
  }

  @Test
  public void findUpsellFor() {

    AbstractQuizDto liveQuiz = new QuizDto()
        .setId(UUID.randomUUID().toString())
        .setSourceId("/test-app")
        .setUpsellConfiguration(new UpsellConfigurationDto()
            .setFallbackImagePath("/test-image")
            .setDefaultUpsellOption(1043120068L)
            .setOptions(ImmutableMap.of(
                "a11-a21", 1043120188L,
                "a13-a24", 1043120210L,
                "a14-a22", 1043120229L
            )));

    List<Long> dynamicSelections = new ArrayList<>(liveQuiz.getUpsellConfiguration().getOptions().values());
    Set<String> dynamicSelectionsKeys = liveQuiz.getUpsellConfiguration().getOptions().keySet();

    when(siteServerApi.getEventToOutcomeForOutcome(Arrays.asList("1043120068", "1043120188"), (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build(),
        Collections.emptyList())).thenReturn(Optional.of(Collections.singletonList(event)));

    Optional<UpsellDto> actualUpsell = upsellService.findUpsellFor(liveQuiz);

    assertThat(actualUpsell)
        .isNotEmpty()
        .get()
        .returns(liveQuiz.getUpsellConfiguration().getFallbackImagePath(), from(UpsellDto::getFallbackImagePath))
        .returns(liveQuiz.getUpsellConfiguration().getDefaultUpsellOption(), upsell -> upsell.getDefaultUpsellOption().getSelectionId());
    assertThat(actualUpsell.get().getDynamicUpsellOptions().keySet())
        .containsExactlyInAnyOrderElementsOf(dynamicSelectionsKeys);
    assertThat(actualUpsell.get().getDynamicUpsellOptions().values())
        .extracting(UpsellPriceDto::getSelectionId)
        .containsExactlyInAnyOrderElementsOf(dynamicSelections);
  }

}
