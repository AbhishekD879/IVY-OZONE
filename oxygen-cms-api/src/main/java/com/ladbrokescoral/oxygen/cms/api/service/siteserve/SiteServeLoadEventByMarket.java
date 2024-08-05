package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventExtendedDto;
import com.ladbrokescoral.oxygen.cms.api.exception.SiteServeMarketValidationException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class SiteServeLoadEventByMarket extends SiteServeLoadEvent {

  private List<String> categoryCodes;
  private List<String> eventCodes;
  private List<String> eventCodesForDiffCategories;
  private List<String> templates;

  private SiteServeApiProvider siteServerApiProvider;

  public SiteServeLoadEventByMarket(
      @Value("${siteserve.marketValidation.categoryCodes}") String categoryCodes,
      @Value("${siteserve.marketValidation.eventCodes}") String eventCodes,
      @Value("${siteserve.marketValidation.eventCodesForDiffCategories}")
          String eventCodesForDiffCategories,
      @Value("${siteserve.marketValidation.templates}") String templates,
      @Autowired SiteServeApiProvider siteServerApiProvider) {
    this.categoryCodes = Arrays.asList(categoryCodes.split(","));
    this.eventCodes = Arrays.asList(eventCodes.split(","));
    this.eventCodesForDiffCategories = Arrays.asList(eventCodesForDiffCategories.split(","));
    this.templates = Arrays.asList(templates.split(","));
    this.siteServerApiProvider = siteServerApiProvider;
  }

  @Override
  public List<SiteServeEventExtendedDto> loadEvents(
      String brand, String selectionId, Instant dateFrom, Instant dateTo) {
    return siteServerApiProvider.api(brand).getWholeEventToOutcomeForMarket(selectionId, false)
        .orElse(Collections.emptyList()).stream()
        .map(getMapper())
        .map(this::validate)
        .collect(Collectors.toList());
  }

  /*
   * Validation is done in few steps
   * 1. Check if event.categoryCode is one of CATEGORY_CODES - setUp step
   * 2. If 1st is:
   *    - true  - checks if event.sortCode is one of EVENT_SORT_CODES
   *    - false - checks if event.sortCode is one of EVENT_SORT_CODES_FOR_DIFF_CATEGORIES
   * 3. and last we check if margetTemplateName is one of MARKET_TEMPLATES
   *
   * validation is success if 2nd OR 3rd results to true
   */
  protected SiteServeEventExtendedDto validate(
      SiteServeEventExtendedDto siteServeEventExtendedDto) {
    List<String> eventSortCodes;

    if (categoryCodes.contains(siteServeEventExtendedDto.getCategoryCode())) {
      eventSortCodes = new ArrayList<>(eventCodes);
    } else {
      eventSortCodes = new ArrayList<>(eventCodesForDiffCategories);
    }

    if (!(eventSortCodes.contains(siteServeEventExtendedDto.getEventSortCode())
        || templates.contains(siteServeEventExtendedDto.getTemplateMarketName()))) {
      final String validationError =
          "Market with \""
              + siteServeEventExtendedDto.getTemplateMarketName()
              + "\" not supported"
              + "\n\nCategory code: "
              + siteServeEventExtendedDto.getCategoryCode()
              + "; Event sort code: "
              + siteServeEventExtendedDto.getEventSortCode()
              + "; Market template name: "
              + siteServeEventExtendedDto.getTemplateMarketName();
      log.error(validationError);
      throw new SiteServeMarketValidationException(validationError);
    }

    return siteServeEventExtendedDto;
  }
}
