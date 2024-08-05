package com.coral.oxygen.middleware.featured.injector

import com.coral.oxygen.middleware.JsonFacade
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService
import com.coral.oxygen.middleware.featured.service.injector.ConsumeBirHREvents
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.Category
import com.egalacoral.spark.siteserver.model.Children
import com.egalacoral.spark.siteserver.model.Event
import com.google.gson.Gson
import org.mockito.Mockito
import spock.lang.Specification



class ConsumeBirHREventsSpec extends Specification{
  public static final Gson GSON = JsonFacade.PRETTY_GSON;
  MarketTemplateNameService marketTemplateNameService
  SiteServerApi siteServerApi
  ConsumeBirHREvents consumeBirHREvents
  def setup(){
    marketTemplateNameService = Mock(MarketTemplateNameService)
    siteServerApi = Mock(SiteServerApi)
    consumeBirHREvents = new ConsumeBirHREvents(siteServerApi,marketTemplateNameService)
  }

  def "Verify Consume Bir HR Events"() {
    List<Category> categories = new ArrayList<>();
    Category category = new Category();
    category.setId(223)
    categories.add(category)
    siteServerApi.getClasses(*_) >>  Optional.of(categories)
    List<Children> child = new ArrayList<>()
    Event event = new Event();
    event.setCategoryId("21")
    Children children = new Children()
    children.setEvent(event)
    siteServerApi.getEventToOutcomeForClass(*_) >>> Optional.of(Arrays.asList(child))
    List<Children> data = consumeBirHREvents.consumeBirEvents()
    expect:
    data.size() >0
  }
}
