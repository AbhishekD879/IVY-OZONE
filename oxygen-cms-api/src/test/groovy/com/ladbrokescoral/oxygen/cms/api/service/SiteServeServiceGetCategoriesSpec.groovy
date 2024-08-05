package com.ladbrokescoral.oxygen.cms.api.service

import com.egalacoral.spark.siteserver.api.BaseFilter
import com.egalacoral.spark.siteserver.api.BinaryOperation
import com.egalacoral.spark.siteserver.api.ExistsFilter
import com.egalacoral.spark.siteserver.api.LimitToFilter
import com.egalacoral.spark.siteserver.api.SimpleFilter
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.api.UnaryOperation
import com.egalacoral.spark.siteserver.model.CategoryEntity
import com.egalacoral.spark.siteserver.model.Event
import com.egalacoral.spark.siteserver.model.Pool
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeServiceImpl
import org.mockito.Mockito
import spock.lang.Specification
import com.egalacoral.spark.siteserver.model.Category;

class SiteServeServiceGetCategoriesSpec extends Specification {

  SiteServerApi siteServerApiMock
  SiteServeService siteServeService
  SiteServeApiProvider serveApiProviderMock

  def setup() {
    serveApiProviderMock = Mock(SiteServeApiProvider)
    siteServerApiMock = Mock(SiteServerApi)
    siteServeService = new SiteServeServiceImpl(serveApiProviderMock)
    serveApiProviderMock.api("bma") >> siteServerApiMock
  }

  def "with categories" () {
    given:
    CategoryEntity categoryEntity = new CategoryEntity();
    siteServerApiMock.getCategories(Optional.empty(), Optional.empty(), true) >>
        Optional.of(Collections.singletonList(categoryEntity))

    when:
    List<CategoryEntity> categories = siteServeService.getCategories("bma")

    then:
    categories.size() == 1
  }

  def "without categories" () {
    given:

    siteServerApiMock.getCategories(Optional.empty(), Optional.empty(), true) >> Optional.empty()

    when:
    List<CategoryEntity> categories = siteServeService.getCategories("bma")

    then:
    categories.size() == 0
  }

  def "getSportSpecials Active categories" () {
    Category category=new Category();
    category.setId(12233)
    List<Category> categories = new ArrayList<>();
    categories.add(category)

    SimpleFilter activeClassesFilter = (SimpleFilter) new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation("class.categoryId", BinaryOperation.equals, "16")
        .addBinaryOperation("class.siteChannels", BinaryOperation.contains, "M")
        .addField("class.isActive")
        .build()
    given:

    siteServerApiMock.getClasses(activeClassesFilter,new ExistsFilter.ExistsFilterBuilder().build())  >> Optional.ofNullable(categories)
    siteServerApiMock
        .getEventToOutcomeForClass(_ as List,_ as SimpleFilter,_ as LimitToFilter,_ as ExistsFilter,Arrays.asList("event", "market")) >> Optional.ofNullable(Arrays.asList(new Event()))
    when:
    List<Event> events= siteServeService.getSportSpecials("bma",16)

    then:
    events.size() == 1
  }

  def "SiteServe JackpotEvents" () {
    BaseFilter poolSimpleFilter =
        new SimpleFilter.SimpleFilterBuilder()
        .addField("pool.isActive")
        .addBinaryOperation("pool.type", BinaryOperation.equals, "V15")
        .build();
    Pool pool=new Pool()
    pool.setId("12344")
    pool.setMarketIds("1223")

    BaseFilter simpleFilter =
        new SimpleFilter.SimpleFilterBuilder()
        .addUnaryOperation("event.isStarted", UnaryOperation.isFalse)
        .build();

    given:
    siteServerApiMock.getPools(poolSimpleFilter) >> Optional.ofNullable(Arrays.asList(pool))
    siteServerApiMock.getWholeEventToOutcomeForMarket("1223",false,simpleFilter) >> Optional.empty()

    when:
    boolean val=siteServeService.hasSiteServeJackpotEvents("bma")

    then:
    val == false
  }
}
