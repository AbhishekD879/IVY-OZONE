package com.coral.oxygen.middleware.featured.service
import com.coral.oxygen.middleware.JsonFacade
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService
import com.coral.oxygen.middleware.common.utils.QueryFilterBuilder
import com.coral.oxygen.middleware.featured.service.injector.FeaturedSiteServerService
import com.egalacoral.spark.siteserver.api.SimpleFilter
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.Event
import com.egalacoral.spark.siteserver.model.Children
import com.google.gson.Gson
import spock.lang.Specification
import java.time.LocalTime;
import java.time.Duration
class FeatureSiteServerServicespec extends Specification{
  FeaturedSiteServerService featuredSiteServerService;
  SiteServerApi siteServerApi = Mock()
  MarketTemplateNameService marketTemplateNameService = Mock()
  QueryFilterBuilder queryFilterBuilder = Mock();
  SimpleFilter simpleFilter = Mock()
  public static final Gson GSON = JsonFacade.PRETTY_GSON;
  def setup() {
    featuredSiteServerService = new FeaturedSiteServerService(siteServerApi, marketTemplateNameService);
  }
  def "Get NextRaces"(){
    Event[] event = fromFile("FeaturedSiteServerServiceTest/event_with_reference_eachway_terms.json", Event[].class)
    given:
    siteServerApi.getNextNEventsForClass(*_) >>>
        [
          Optional.of(Arrays.asList(event))
        ]
    when:
    String classId = "12";
    String excludeTypeId = "442"
    List<Event> events = featuredSiteServerService.getNextRaces(classId,excludeTypeId)
    then:
    events.size() == 1
  }
  def "Get InternationalToteRacingEventsAndExternalKeys"(){
    Children[] child = fromFile("FeaturedSiteServerServiceTest/event_with_reference_eachway_terms.json", Children[].class)
    given:
    siteServerApi.getEventToOutcomeForClass(*_) >>>
        [
          Optional.of(Arrays.asList(child))
        ]
    when:
    List<String> classIds = new ArrayList<>();
    classIds.add("12")
    Duration d = Duration.between(LocalTime.NOON,LocalTime.MAX);
    List<Children> children = featuredSiteServerService.getInternationalToteRacingEventsAndExternalKeys(classIds,d)
    then:
    children.size() == 1
  }
  def "Get getVirtualRacingEventsAndExternalKeys"(){
    Children[] child = fromFile("FeaturedSiteServerServiceTest/event_with_reference_eachway_terms.json", Children[].class)
    given:
    siteServerApi.getEventToOutcomeForClass(*_) >>>
        [
          Optional.of(Arrays.asList(child))
        ]
    when:
    List<String> classIds = new ArrayList<>();
    classIds.add("12")
    Duration d = Duration.between(LocalTime.NOON,LocalTime.MAX);
    List<Children> children = featuredSiteServerService.getVirtualRacingEventsAndExternalKeys(classIds,"12","13",d)
    then:
    children.size() == 1
  }

  def "Get getVirtualRacingEventsAndExternalKeys"(){
    Children[] child = fromFile("FeaturedSiteServerServiceTest/event_with_reference_eachway_terms.json", Children[].class)
    given:
    siteServerApi.getEventToOutcomeForClass(*_) >>>
        [
          Optional.of(Arrays.asList(child))
        ]
    when:
    List<String> classIds = new ArrayList<>();
    classIds.add("12")
    Duration d = Duration.between(LocalTime.NOON,LocalTime.MAX);
    List<Children> children = featuredSiteServerService.getVirtualRacingEvents(classIds,"12","13",d)
    then:
    children.size() == 1
  }
  public static <T> T fromFile(String name, Class<T> clazz) {
    InputStream stream = FeatureSiteServerServicespec.class.getClassLoader().getResourceAsStream(name);
    return GSON.fromJson(new InputStreamReader(stream), clazz);
  }
}
