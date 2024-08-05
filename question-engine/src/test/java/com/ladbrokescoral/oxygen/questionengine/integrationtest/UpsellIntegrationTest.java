/*
package com.ladbrokescoral.oxygen.questionengine.integrationtest;

import com.google.common.collect.ImmutableMap;
import com.ladbrokescoral.oxygen.questionengine.configuration.properties.ApplicationProperties;
import com.ladbrokescoral.oxygen.questionengine.dto.AbstractQuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.UpsellDto;
import com.ladbrokescoral.oxygen.questionengine.dto.UpsellPriceDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.UpsellConfigurationDto;
import com.ladbrokescoral.oxygen.questionengine.integrationtest.config.IntegrationTest;
import com.ladbrokescoral.oxygen.questionengine.service.UpsellService;
import org.assertj.core.api.InstanceOfAssertFactories;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.contract.wiremock.AutoConfigureWireMock;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.context.junit4.SpringRunner;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;

import static com.github.tomakehurst.wiremock.client.WireMock.aResponse;
import static com.github.tomakehurst.wiremock.client.WireMock.get;
import static com.github.tomakehurst.wiremock.client.WireMock.stubFor;
import static com.github.tomakehurst.wiremock.client.WireMock.urlEqualTo;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.from;

@IntegrationTest
@RunWith(SpringRunner.class)
@TestPropertySource(
    locations = "classpath:integration-test.properties",
    properties = {
        "wiremock.rest-template-ssl-enabled=false",
        "site-server.baseUrl=http://localhost:${wiremock.server.port}",
        "application.cachingEnabled=false",
        "spring.cache.type=none",
        "application.siteServerSelectionIdsLimit=5"
    })
@AutoConfigureWireMock(port = 0, files = "classpath:/upsell")
public class UpsellIntegrationTest {

  @Autowired
  private UpsellService upsellService;
  @Autowired
  private ApplicationProperties applicationProperties;

  @Test
  public void happyPath() {
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

    String siteServerUrl = String.format("/openbet-ssviewer/Drilldown/2.26/EventToOutcomeForOutcome/%d,%d,%d,%d?includeRestricted=true&translationLang=en&includeUndisplayed=false",
        liveQuiz.getUpsellConfiguration().getDefaultUpsellOption(),
        dynamicSelections.get(0),
        dynamicSelections.get(1),
        dynamicSelections.get(2)
    );

    stubFor(get(urlEqualTo(siteServerUrl)).willReturn(aResponse().withBodyFile("happy-path.json")));

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

  @Test
  public void oneOfConfiguredSelectionIdGivesMoreThanOneOutcome() {
    AbstractQuizDto liveQuiz = new QuizDto()
        .setId(UUID.randomUUID().toString())
        .setSourceId("/test-app")
        .setUpsellConfiguration(new UpsellConfigurationDto()
            .setFallbackImagePath("/test-image")
            .setDefaultUpsellOption(1037508796L)
            .setOptions(ImmutableMap.of(
                "a11-a21", 1037508803L,
                "a14-a22", 1037508810L,
                "a23-a31", 1037508802L
            )));
    List<Long> dynamicSelections = new ArrayList<>(liveQuiz.getUpsellConfiguration().getOptions().values());
    Set<String> dynamicSelectionsKeys = liveQuiz.getUpsellConfiguration().getOptions().keySet();

    String siteServerUrl = String.format("/openbet-ssviewer/Drilldown/2.26/EventToOutcomeForOutcome/%d,%d,%d,%d?includeRestricted=true&translationLang=en&includeUndisplayed=false",
        liveQuiz.getUpsellConfiguration().getDefaultUpsellOption(),
        dynamicSelections.get(0),
        dynamicSelections.get(1),
        dynamicSelections.get(2)
    );

    stubFor(get(urlEqualTo(siteServerUrl)).willReturn(aResponse().withBodyFile("more-than-one-outcome.json")));

    Optional<UpsellDto> actualUpsell = upsellService.findUpsellFor(liveQuiz);

    assertThat(actualUpsell)
        .isNotEmpty()
        .get()
        .returns(liveQuiz.getUpsellConfiguration().getFallbackImagePath(), from(UpsellDto::getFallbackImagePath))
        .returns(liveQuiz.getUpsellConfiguration().getDefaultUpsellOption(), upsell -> upsell.getDefaultUpsellOption().getSelectionId());
    assertThat(actualUpsell)
        .get()
        .extracting(upsell -> upsell.getDynamicUpsellOptions().keySet())
        .asInstanceOf(InstanceOfAssertFactories.iterable(String.class))
        .containsExactlyInAnyOrderElementsOf(dynamicSelectionsKeys);
    assertThat(actualUpsell)
        .get()
        .extracting(upsell -> upsell.getDynamicUpsellOptions().values())
        .asInstanceOf(InstanceOfAssertFactories.iterable(UpsellPriceDto.class))
        .extracting(UpsellPriceDto::getSelectionId)
        .containsExactlyInAnyOrderElementsOf(dynamicSelections);
  }

  @Test
  public void oneOfConfiguredSelectionIdIsIncorrect() {
    long incorrectSelectionId = 1000000000L;
    AbstractQuizDto liveQuiz = new QuizDto()
        .setId(UUID.randomUUID().toString())
        .setSourceId("/test-app")
        .setUpsellConfiguration(new UpsellConfigurationDto()
            .setFallbackImagePath("/test-image")
            .setDefaultUpsellOption(1043120068L)
            .setOptions(ImmutableMap.of(
                "a11-a21", 1043120188L,
                "a13-a24", incorrectSelectionId,
                "a14-a22", 1043120229L
            )));
    List<Long> dynamicSelections = new ArrayList<>(liveQuiz.getUpsellConfiguration().getOptions().values());
    List<String> dynamicSelectionsKeys = new ArrayList<>(liveQuiz.getUpsellConfiguration().getOptions().keySet());

    String siteServerUrl = String.format("/openbet-ssviewer/Drilldown/2.26/EventToOutcomeForOutcome/%d,%d,%d,%d?includeRestricted=true&translationLang=en&includeUndisplayed=false",
        liveQuiz.getUpsellConfiguration().getDefaultUpsellOption(),
        dynamicSelections.get(0),
        dynamicSelections.get(1),
        dynamicSelections.get(2)
    );

    stubFor(get(urlEqualTo(siteServerUrl)).willReturn(aResponse().withBodyFile("wrong-selection-configured.json")));

    Optional<UpsellDto> actualUpsell = upsellService.findUpsellFor(liveQuiz);

    assertThat(actualUpsell)
        .isNotEmpty()
        .get()
        .returns(liveQuiz.getUpsellConfiguration().getFallbackImagePath(), from(UpsellDto::getFallbackImagePath))
        .returns(liveQuiz.getUpsellConfiguration().getDefaultUpsellOption(), upsell -> upsell.getDefaultUpsellOption().getSelectionId());
    assertThat(actualUpsell.get().getDynamicUpsellOptions().keySet())
        .containsExactlyInAnyOrder(dynamicSelectionsKeys.get(0), dynamicSelectionsKeys.get(2));
    assertThat(actualUpsell.get().getDynamicUpsellOptions().values())
        .extracting(UpsellPriceDto::getSelectionId)
        .containsExactlyInAnyOrder(dynamicSelections.get(0), dynamicSelections.get(2));
  }

  @Test
  public void oneOfConfiguredSelectionIdGivesEmptyOutcome() {
    long selectionToReturnEmptyOutcome = 1000000000L;
    AbstractQuizDto liveQuiz = new QuizDto()
        .setId(UUID.randomUUID().toString())
        .setSourceId("/test-app")
        .setUpsellConfiguration(new UpsellConfigurationDto()
            .setFallbackImagePath("/test-image")
            .setDefaultUpsellOption(selectionToReturnEmptyOutcome)
            .setOptions(ImmutableMap.of(
                "a11-a21", 1043120188L,
                "a13-a24", 1043120210L,
                "a14-a22", 1043120229L
            )));
    List<Long> dynamicSelections = new ArrayList<>(liveQuiz.getUpsellConfiguration().getOptions().values());
    List<String> dynamicSelectionsKeys = new ArrayList<>(liveQuiz.getUpsellConfiguration().getOptions().keySet());

    String siteServerUrl = String.format("/openbet-ssviewer/Drilldown/2.26/EventToOutcomeForOutcome/%d,%d,%d,%d?includeRestricted=true&translationLang=en&includeUndisplayed=false",
        liveQuiz.getUpsellConfiguration().getDefaultUpsellOption(),
        dynamicSelections.get(0),
        dynamicSelections.get(1),
        dynamicSelections.get(2)
    );

    stubFor(get(urlEqualTo(siteServerUrl)).willReturn(aResponse().withBodyFile("empty-outcome.json")));

    Optional<UpsellDto> actualUpsell = upsellService.findUpsellFor(liveQuiz);

    assertThat(actualUpsell)
        .isNotEmpty()
        .get()
        .returns(liveQuiz.getUpsellConfiguration().getFallbackImagePath(), from(UpsellDto::getFallbackImagePath))
        .returns(null, UpsellDto::getDefaultUpsellOption);
    assertThat(actualUpsell.get().getDynamicUpsellOptions().keySet())
        .containsExactlyInAnyOrderElementsOf(dynamicSelectionsKeys);
    assertThat(actualUpsell.get().getDynamicUpsellOptions().values())
        .extracting(UpsellPriceDto::getSelectionId)
        .containsExactlyInAnyOrderElementsOf(dynamicSelections);
  }

  @Test
  public void noUpsellConfigured() {
    AbstractQuizDto liveQuiz = new QuizDto()
        .setId(UUID.randomUUID().toString())
        .setSourceId("/test-app");
    assertThat(upsellService.findUpsellFor(liveQuiz)).isEmpty();
  }

  @Test
  public void noDynamicUpsellConfigured() {
    AbstractQuizDto liveQuiz = new QuizDto()
        .setId(UUID.randomUUID().toString())
        .setSourceId("/test-app")
        .setUpsellConfiguration(new UpsellConfigurationDto()
            .setFallbackImagePath("/test-image")
            .setDefaultUpsellOption(1043120068L)
            .setOptions(Collections.emptyMap()));
    String siteServerUrl = String.format("/openbet-ssviewer/Drilldown/2.26/EventToOutcomeForOutcome/%d?includeRestricted=true&translationLang=en&includeUndisplayed=false",
        liveQuiz.getUpsellConfiguration().getDefaultUpsellOption()
    );

    stubFor(get(urlEqualTo(siteServerUrl)).willReturn(aResponse().withBodyFile("no-dynamic-upsell.json")));

    Optional<UpsellDto> actualUpsell = upsellService.findUpsellFor(liveQuiz);

    assertThat(actualUpsell)
        .isNotEmpty()
        .get()
        .returns(liveQuiz.getUpsellConfiguration().getFallbackImagePath(), from(UpsellDto::getFallbackImagePath))
        .returns(liveQuiz.getUpsellConfiguration().getDefaultUpsellOption(), upsell -> upsell.getDefaultUpsellOption().getSelectionId());
    assertThat(actualUpsell.get().getDynamicUpsellOptions()).isEmpty();
  }


  @Test
  public void noDefaultUpsellConfigured() {
    AbstractQuizDto liveQuiz = new QuizDto()
        .setId(UUID.randomUUID().toString())
        .setSourceId("/test-app")
        .setUpsellConfiguration(new UpsellConfigurationDto()
            .setFallbackImagePath("/test-image")
            .setOptions(ImmutableMap.of(
                "a11-a21", 1043120188L,
                "a13-a24", 1043120210L,
                "a14-a22", 1043120229L
            )));
    List<Long> dynamicSelections = new ArrayList<>(liveQuiz.getUpsellConfiguration().getOptions().values());
    Set<String> dynamicSelectionsKeys = liveQuiz.getUpsellConfiguration().getOptions().keySet();

    String siteServerUrl = String.format("/openbet-ssviewer/Drilldown/2.26/EventToOutcomeForOutcome/%d,%d,%d?includeRestricted=true&translationLang=en&includeUndisplayed=false",
        dynamicSelections.get(0),
        dynamicSelections.get(1),
        dynamicSelections.get(2)
    );

    stubFor(get(urlEqualTo(siteServerUrl)).willReturn(aResponse().withBodyFile("no-default-upsell.json")));

    Optional<UpsellDto> actualUpsell = upsellService.findUpsellFor(liveQuiz);

    assertThat(actualUpsell)
        .isNotEmpty()
        .get()
        .returns(liveQuiz.getUpsellConfiguration().getFallbackImagePath(), from(UpsellDto::getFallbackImagePath))
        .returns(null, UpsellDto::getDefaultUpsellOption);
    assertThat(actualUpsell.get().getDynamicUpsellOptions().keySet())
        .containsExactlyInAnyOrderElementsOf(dynamicSelectionsKeys);
    assertThat(actualUpsell.get().getDynamicUpsellOptions().values())
        .extracting(UpsellPriceDto::getSelectionId)
        .containsExactlyInAnyOrderElementsOf(dynamicSelections);
  }
}
*/
