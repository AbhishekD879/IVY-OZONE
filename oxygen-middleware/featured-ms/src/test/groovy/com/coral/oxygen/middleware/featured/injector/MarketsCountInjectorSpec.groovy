package com.coral.oxygen.middleware.featured.injector

import com.coral.oxygen.middleware.common.configuration.SiteServerAPIConfiguration
import com.coral.oxygen.middleware.common.service.featured.IdsCollector
import com.coral.oxygen.middleware.featured.service.injector.MarketsCountInjector
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContent
import com.coral.oxygen.middleware.pojos.model.cms.featured.ModularContentItem
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.Aggregation
import org.springframework.boot.test.context.SpringBootTest
import spock.lang.Specification

import java.util.stream.Collectors

import static com.coral.oxygen.middleware.featured.utils.FeaturedDataUtils.*
import static java.lang.String.valueOf
import static java.util.stream.Collectors.toMap
import static java.util.stream.Stream.concat

@SpringBootTest(classes = [SiteServerAPIConfiguration.class])
class MarketsCountInjectorSpec extends Specification {
  MarketsCountInjector marketsCountInjector
  SiteServerApi siteServerApi

  FeaturedModel model
  ModularContentItem featureItem
  List<Aggregation> marketsStartedCount
  List<Aggregation> marketsNotStartedCount
  ModularContent modularContent
  IdsCollector idsCollector

  def setup() {
    siteServerApi = Mock(SiteServerApi)
    marketsCountInjector = new MarketsCountInjector(siteServerApi)

    modularContent = new ModularContent()
    modularContent.addAll(getModularContentItemsFromResource("injector_modular_content.json"))
    featureItem = getModularContentItemFromResource("injector_featured_modular_item.json")
    model = getFeaturedModelFromResource("injector_featured_output_model_result.json")
    marketsStartedCount = getSSMarketsCountForEvent("injector_markets_count_started.json")
    marketsNotStartedCount = getSSMarketsCountForEvent("injector_makrets_count_not_started.json")
    idsCollector = new IdsCollector(modularContent, featureItem)

    siteServerApi.getMarketsCountForEvent(_ as List, _) >> Optional.of(marketsStartedCount) >> Optional.of(marketsNotStartedCount)
  }

  def "Check markets count after injecting"() {
    Map<Long, Integer> marketsMap = concat(marketsNotStartedCount.stream(), marketsStartedCount.stream())
        .collect(toMap({ aggregation -> aggregation.getRefRecordId() },
        { aggregation -> aggregation.getCount() },
        { a, b -> a }))

    List<EventsModuleData> items = model.getModules().stream()
        .map({ outputModule -> outputModule.getData() })
        .flatMap({ collection -> collection.stream() })
        .map({data -> (EventsModuleData) data })
        .collect(Collectors.toList())

    marketsCountInjector.injectData(items, idsCollector)

    model.getModules().stream()
        .map({ outputModule -> outputModule.getData() })
        .flatMap({ collection -> collection.stream() })
        .filter({ event -> event.getId() != null })
        .filter({ event -> marketsMap.containsKey(valueOf(event.getId())) })
        .forEach({ event ->
          assert event.getMarketsCount() == marketsMap.get(valueOf(event.getId()))
        })

    expect:
    true
  }
}
