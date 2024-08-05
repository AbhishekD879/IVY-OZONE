package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.CategoryEntity;
import com.egalacoral.spark.siteserver.model.Coupon;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventValidationResultDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeKnockoutEventDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import java.util.List;
import java.util.Optional;
import java.util.Set;

public interface SiteServeService {
  Optional<SiteServeMarketDto> getMarketById(String brand, String marketId);

  Optional<List<Category>> getClassToSubTypeForType(String brand, String typeId);

  SiteServeEventValidationResultDto validateAndGetEventsById(
      String brand, List<String> ids, boolean onlySpecials);

  SiteServeEventValidationResultDto validateEventsByTypeId(
      String brand, List<String> ids, boolean onlySpecials);

  SiteServeEventValidationResultDto validateEventsByOutcomeId(String brand, List<String> ids);

  boolean isTypeIdValid(String brand, String typeId);

  void isTypeIdValid(String brand, Integer typeId);

  Optional<SiteServeKnockoutEventDto> getKnockoutEvent(String brand, String eventId);

  boolean isCategoryNotValidOrHasEvents(String brand, Integer categoryId);

  boolean anyLiveOrUpcomingEventsExists(SportCategory sport);

  Boolean hasSiteServeCategoryEvents(String brand, Integer categoryId);

  boolean hasSiteServeJackpotEvents(String brand);

  Set<Integer> filterByCompetitionEvents(String brand, List<SportCategory> categories);

  Set<Integer> filterByOutrightEvents(String brand, Set<Integer> categoryIds);

  List<Coupon> getCouponsForTodaysAndUpcomingIn24hEvents(String brand);

  List<Event> getSportSpecials(String brand, int categoryId);

  List<CategoryEntity> getCategories(String brand);

  List<Event> getNextEvents(NextEventsParameters nextEventsParameters);

  public List<Event> getCommentsByEventId(String brand, List<String> eventId);

  public Optional<List<Event>> findNextEventsByCategoryId(String brand, Integer categoryId);

  public Optional<List<Event>> findPreviousEventsByCategoryId(String brand, Integer categoryId);

  List<Event> getNextFiveMinsAndLiveEvents(String brand, int categoryId, List<String> eventIds);
}
