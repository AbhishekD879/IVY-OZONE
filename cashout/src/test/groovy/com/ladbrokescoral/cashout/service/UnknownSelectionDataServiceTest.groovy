package com.ladbrokescoral.cashout.service

import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.Event
import com.ladbrokescoral.cashout.TestUtil
import com.ladbrokescoral.cashout.model.context.SelectionPrice
import com.ladbrokescoral.cashout.repository.EntityStatus
import com.ladbrokescoral.cashout.repository.ReactiveRepository
import com.ladbrokescoral.cashout.repository.SelectionHierarchyStatusRepository
import reactor.core.publisher.Mono
import reactor.core.scheduler.Schedulers
import reactor.test.StepVerifier
import spock.lang.Specification


class UnknownSelectionDataServiceTest extends Specification {
  private UnknownSelectionDataService service
  private List<SelectionData> data
  private ReactiveRepository priceRepo
  private SelectionHierarchyStatusRepository statusRepo
  private SiteServerApi siteServer
  private UnknownSelectionData unknownData = Mock(UnknownSelectionData)
  private unknownEntities

  void setup() {
    priceRepo = Mock(ReactiveRepository)
    priceRepo.multiGet(_) >> Mono.just(Collections.emptyList()).publishOn(Schedulers.immediate())
    statusRepo = Mock(SelectionHierarchyStatusRepository)
    statusRepo.fetchEventStatuses(_) >> Mono.just(Collections.emptyList())
    statusRepo.fetchMarketStatuses(_) >> Mono.just(Collections.emptyList())
    statusRepo.fetchSelectionStatuses(_) >> Mono.just(Collections.emptyList())
    siteServer = Mock(SiteServerApi)
    siteServer.getWholeEventToOutcomeForMarket(_ as List, _ as Boolean) >> Optional.empty();
    data = []

    unknownEntities = Mock(UnknownSelectionData.UnknownEntities)
    this.unknownEntities.getEventIds() >> []
    this.unknownEntities.getMarketIds() >> []
    this.unknownEntities.getSelectionIds() >> []
    unknownData.getUnknownEntitiesOnly() >> this.unknownEntities
    unknownData.getMarketIdsOfUnknownItems() >> []
    service = createUnknownDataService(unknownData)
  }

  private UnknownSelectionDataService createUnknownDataService(UnknownSelectionData unknownData) {
    new UnknownSelectionDataService(priceRepo, statusRepo, siteServer, unknownData, Schedulers.immediate())
  }

  def "Unknown eventIds are resolved from redis"() {
    when:
    service.resolveUnknowns()
    then:
    unknownEntities.getEventIds() >> [1, 2]

    1 * statusRepo.fetchEventStatuses({it.size() == 2 && it.contains(1) && it.contains(2)}) >> Mono.empty()
    1 * statusRepo.fetchMarketStatuses({it.isEmpty()}) >> Mono.empty()
    1 * statusRepo.fetchSelectionStatuses({it.isEmpty()}) >> Mono.empty()
    1 * priceRepo.multiGet({it.isEmpty()}) >> Mono.empty()
  }

  def "Unknown marketIds are resolved from redis"() {
    when:
    service.resolveUnknowns()
    then:
    unknownEntities.getMarketIds() >> [1, 2]

    1 * statusRepo.fetchEventStatuses({it.isEmpty()}) >> Mono.empty()
    1 * statusRepo.fetchMarketStatuses({it.size() == 2 && it.contains(1) && it.contains(2)}) >> Mono.empty()
    1 * statusRepo.fetchSelectionStatuses({it.isEmpty()}) >> Mono.empty()
    1 * priceRepo.multiGet({it.isEmpty()}) >> Mono.empty()
  }

  def "Unknown selectionsIds are resolved from redis"() {
    when:
    service.resolveUnknowns()
    then:
    unknownEntities.getSelectionIds() >> [
      BigInteger.valueOf(1),
      BigInteger.valueOf(2)
    ]

    1 * statusRepo.fetchEventStatuses({it.isEmpty()}) >> Mono.empty()
    1 * statusRepo.fetchMarketStatuses({it.isEmpty()}) >> Mono.empty()
    1 * statusRepo.fetchSelectionStatuses({it.size() == 2 && it.contains(BigInteger.valueOf(1)) && it.contains(BigInteger.valueOf(2))}) >> Mono.empty()
    1 * priceRepo.multiGet({it.size() == 2 && it.contains("1") && it.contains("2")}) >> Mono.empty()
  }

  def "Event/market/selection statuses and price are updated when fetched from redis"() {
    given:
    def monoEvents = Mono.just([
      new EntityStatus(BigInteger.valueOf(1), true),
      new EntityStatus(BigInteger.valueOf(2), false)
    ])
    def monoMarkets = Mono.just([
      new EntityStatus(BigInteger.valueOf(3), true),
      new EntityStatus(BigInteger.valueOf(4), false)
    ])
    def monoSelections = Mono.just([
      new EntityStatus(BigInteger.valueOf(5), true),
      new EntityStatus(BigInteger.valueOf(6), false)
    ])
    def monoPrices = Mono.just([
      new SelectionPrice("5", "1", "2"),
      new SelectionPrice("6", "3", "4")
    ])
    when:
    service.resolveUnknowns()
    then:
    StepVerifier.create(monoEvents).expectNextCount(1).expectComplete().verify()
    StepVerifier.create(monoMarkets).expectNextCount(1).expectComplete().verify()
    StepVerifier.create(monoSelections).expectNextCount(1).expectComplete().verify()
    StepVerifier.create(monoPrices).expectNextCount(1).expectComplete().verify()
    statusRepo.fetchEventStatuses(_) >> monoEvents
    statusRepo.fetchMarketStatuses(_) >> monoMarkets
    statusRepo.fetchSelectionStatuses(_) >> monoSelections
    priceRepo.multiGet(_) >> monoPrices

    1 * unknownData.updateEventStatus(BigInteger.valueOf(1), true)
    1 * unknownData.updateEventStatus(BigInteger.valueOf(2), false)
    1 * unknownData.updateMarketStatus(BigInteger.valueOf(3), true)
    1 * unknownData.updateMarketStatus(BigInteger.valueOf(4), false)
    1 * unknownData.updateSelectionStatus(BigInteger.valueOf(5), true)
    1 * unknownData.updateSelectionStatus(BigInteger.valueOf(6), false)
    1 * unknownData.updatePrice(BigInteger.valueOf(5), 1, 2)
    1 * unknownData.updatePrice(BigInteger.valueOf(6), 3, 4)
  }

  def "Event/market/selection is resolved from siteserver"() {
    given:
    List<Event> siteServerResponse = loadFromFile("/siteserver/twoMarketResponse.json")
    when:
    service.resolveUnknowns()
    then:
    unknownData.getMarketIdsOfUnknownItems() >> [
      BigInteger.valueOf(156313923),
      BigInteger.valueOf(156518623)
    ]
    siteServerResponse.size() == 2
    1 * siteServer.getWholeEventToOutcomeForMarket(["156313923", "156518623"], true) >> Optional.of(siteServerResponse)
    1 * unknownData.updateEventStatus(BigInteger.valueOf(10420237), true)
    1 * unknownData.updateEventStatus(BigInteger.valueOf(10447521), false)

    1 * statusRepo.updateEventStatus(new EntityStatus(BigInteger.valueOf(10420237), true))
    1 * statusRepo.updateEventStatus(new EntityStatus(BigInteger.valueOf(10447521), false))

    1 * unknownData.updateMarketStatus(BigInteger.valueOf(156313923), true)
    1 * unknownData.updateMarketStatus(BigInteger.valueOf(156518623), false)

    1 * statusRepo.updateMarketStatus(new EntityStatus(BigInteger.valueOf(156313923), true))
    1 * statusRepo.updateMarketStatus(new EntityStatus(BigInteger.valueOf(156518623), false))

    1 * unknownData.updateSelectionStatus(BigInteger.valueOf(581094304), true)
    1 * unknownData.updateSelectionStatus(BigInteger.valueOf(581094302), false)
    1 * unknownData.updateSelectionStatus(BigInteger.valueOf(581094303), true)
    1 * unknownData.updateSelectionStatus(BigInteger.valueOf(581852696), true)
    1 * unknownData.updateSelectionStatus(BigInteger.valueOf(581852697), true)
    1 * unknownData.updateSelectionStatus(BigInteger.valueOf(581852695), true)

    1 * statusRepo.updateSelectionStatus(new EntityStatus(BigInteger.valueOf(581094304), true))
    1 * statusRepo.updateSelectionStatus(new EntityStatus(BigInteger.valueOf(581094302), false))
    1 * statusRepo.updateSelectionStatus(new EntityStatus(BigInteger.valueOf(581094303), true))
    1 * statusRepo.updateSelectionStatus(new EntityStatus(BigInteger.valueOf(581852696), true))
    1 * statusRepo.updateSelectionStatus(new EntityStatus(BigInteger.valueOf(581852697), true))
    1 * statusRepo.updateSelectionStatus(new EntityStatus(BigInteger.valueOf(581852695), true))

    1 * unknownData.updatePrice(BigInteger.valueOf(581094304), 27, 10)
    1 * unknownData.updatePrice(BigInteger.valueOf(581094302), 7, 10)
    1 * unknownData.updatePrice(BigInteger.valueOf(581094303), 10, 3)
    1 * unknownData.updatePrice(BigInteger.valueOf(581852696), 1, 3)
    1 * unknownData.updatePrice(BigInteger.valueOf(581852697), 1, 4)
    1 * unknownData.updatePrice(BigInteger.valueOf(581852695), 1, 2)

    1 * priceRepo.save(new SelectionPrice("581094304", "27", "10")) >> Mono.empty()
    1 * priceRepo.save(new SelectionPrice("581094302", "7", "10")) >> Mono.empty()
    1 * priceRepo.save(new SelectionPrice("581094303", "10", "3")) >> Mono.empty()
    1 * priceRepo.save(new SelectionPrice("581852696", "1", "3")) >> Mono.empty()
    1 * priceRepo.save(new SelectionPrice("581852697", "1", "4")) >> Mono.empty()
    1 * priceRepo.save(new SelectionPrice("581852695", "1", "2")) >> Mono.empty()
  }

  List<Event> loadFromFile(String pathToFile) {
    TestUtil.deserializeListWithJackson(pathToFile, Event.class)
  }
}
