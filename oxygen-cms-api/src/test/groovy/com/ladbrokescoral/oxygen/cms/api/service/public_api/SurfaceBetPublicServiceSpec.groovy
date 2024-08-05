package com.ladbrokescoral.oxygen.cms.api.service.public_api

import java.util.concurrent.atomic.AtomicInteger
import java.util.function.Function
import java.util.function.Predicate
import java.util.stream.Collectors

import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.Children
import com.egalacoral.spark.siteserver.model.Event
import com.egalacoral.spark.siteserver.model.Market
import com.egalacoral.spark.siteserver.model.Outcome
import com.egalacoral.spark.siteserver.model.Price
import com.ladbrokescoral.oxygen.cms.api.TestUtil
import com.ladbrokescoral.oxygen.cms.api.dto.SurfaceBetDto
import com.ladbrokescoral.oxygen.cms.api.entity.RelationType
import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants
import com.ladbrokescoral.oxygen.cms.api.exception.SurfaceBetException
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository
import com.ladbrokescoral.oxygen.cms.api.repository.SurfaceBetRepository
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider

import spock.lang.Specification

class SurfaceBetPublicServiceSpec extends Specification {

  SurfaceBetRepository repository = Mock()
  SiteServeApiProvider serveApiProvider = Mock()
  SiteServerApi siteServerApi = Mock()
  SegmentRepository segmentRepository = Mock()

  SurfaceBetPublicService surfaceBetPublicService


  def setup() {
    surfaceBetPublicService = new SurfaceBetPublicService(repository, serveApiProvider,segmentRepository)
  }
  def "test find active SurfaceBet for sport pages"() {
    given:
    repository.findByBrandAndDisplayFromIsBeforeAndDisplayToIsAfterAndDisabledIsFalseOrderBySortOrderAsc(*_) >>
        TestUtil.deserializeListWithJackson("service/public_api/find_surface_bets_response.json", SurfaceBet.class)


    def segments = Segment.builder().segmentName(SegmentConstants.UNIVERSAL).brand("bma").build();

    segmentRepository.findByBrand("bma") >> [segments]

    when:
    def result = surfaceBetPublicService.findActiveByBrandAndRelationType("bma", new AtomicInteger(0),RelationType.sport, RelationType.eventhub)

    then:
    result.size() == 2

    and:
    result.stream().allMatch(isAllSurfaceBetsRelationTypesIn(Arrays.asList(RelationType.sport.name(), RelationType.eventhub.name())))
    result.stream().allMatch(isAllEnabled())
  }

  def "test find active NonUniversalSurfaceBet for sport pages"() {
    given:
    repository.findByBrandAndDisplayFromIsBeforeAndDisplayToIsAfterAndDisabledIsFalseOrderBySortOrderAsc(*_) >>
        TestUtil.deserializeListWithJackson("service/public_api/find_surface_bets_response.json", SurfaceBet.class)


    def segments = Segment.builder().segmentName("segment1").brand("bma").build();

    segmentRepository.findByBrand("bma") >> [segments]

    when:
    def result = surfaceBetPublicService.findActiveByBrandAndRelationType("bma", new AtomicInteger(0),RelationType.sport, RelationType.eventhub)

    then:
    result.size() == 2

    and:
    result.stream().allMatch(isAllSurfaceBetsRelationTypesIn(Arrays.asList(RelationType.sport.name(), RelationType.eventhub.name())))
    result.stream().allMatch(isAllEnabled())
  }

  def "test find active NonUniversalSurfaceBet for default pages"() {
    given:
    List<SurfaceBet> surfaceBets = TestUtil.deserializeListWithJackson("service/public_api/find_surface_bets_response.json", SurfaceBet.class);
    surfaceBets.forEach({ sb -> sb.setReferences(null) })
    repository.findByBrandAndDisplayFromIsBeforeAndDisplayToIsAfterAndDisabledIsFalseOrderBySortOrderAsc(*_) >>
        surfaceBets


    def segments = Segment.builder().segmentName("segment1").brand("bma").build();

    segmentRepository.findByBrand("bma") >> [segments]

    when:
    def result = surfaceBetPublicService.findActiveByBrandAndRelationType("bma", new AtomicInteger(0),RelationType.sport, RelationType.eventhub)

    then:
    result.size() == 4

    and:
    result.stream().allMatch(isAllSurfaceBetsRelationTypesIn(Arrays.asList(RelationType.sport.name(), RelationType.eventhub.name())))
    result.stream().allMatch(isAllEnabled())
  }

  def "test find active NonUniversalSurfaceBet for edp pages"() {
    given:
    List<SurfaceBet> surfaceBets = TestUtil.deserializeListWithJackson("service/public_api/find_surface_bets_response.json", SurfaceBet.class);
    surfaceBets.get(0).getReferences().forEach({ ref -> ref.setRelatedTo(RelationType.edp) })
    surfaceBets.get(1).getReferences().forEach({ref -> ref.setRefId("1")})
    repository.findByBrandAndDisplayFromIsBeforeAndDisplayToIsAfterAndDisabledIsFalseOrderBySortOrderAsc(*_) >>
        surfaceBets


    def segments = Segment.builder().segmentName("segment1").brand("bma").build();

    segmentRepository.findByBrand("bma") >> [segments]

    when:
    def result = surfaceBetPublicService.findActiveByBrandAndRelationType("bma", new AtomicInteger(0),RelationType.sport, RelationType.eventhub)

    then:
    result.size() == 2

    and:
    result.stream().allMatch(isAllSurfaceBetsRelationTypesIn(Arrays.asList(RelationType.sport.name(), RelationType.eventhub.name())))
    result.stream().allMatch(isAllEnabled())
  }


  def "test find active SurfaceBet for edp"() {
    given:
    def surfaceBets = edpSurfaceBets()
    repository.findUniversalRecordsByBrandAndActiveTrue(*_) >> surfaceBets
    serveApiProvider.api(_) >> siteServerApi
    siteServerApi.getEventToOutcomeForOutcome(*_) >> createEvents(surfaceBets, true)
    def eventId = "123456"
    def segments = Segment.builder().segmentName(SegmentConstants.UNIVERSAL).brand("bma").build();

    segmentRepository.findByBrand("bma") >> [segments]
    when:
    def result = surfaceBetPublicService.findActiveEdpSurfaceBets("bma", eventId)

    then:
    result.size() == 1

    and:
    result.stream().allMatch(isAllSurfaceBetsRelationTypesIn(Arrays.asList(RelationType.edp.name())))
    SurfaceBetDto surfaceBetDto = (SurfaceBetDto) result.get(0)
    surfaceBetDto.getReference().isEnabled()
  }

  def "test find active expiredEvent SurfaceBet for edp"() {
    given:
    def surfaceBets = getSameEventSurfaceBet()
    repository.findUniversalRecordsByBrandAndActiveTrue(*_) >> surfaceBets
    serveApiProvider.api(_) >> siteServerApi
    siteServerApi.getEventToOutcomeForOutcome(*_) >> createEvents(surfaceBets, true)
    def eventId = "11000177"
    def segments = Segment.builder().segmentName(SegmentConstants.UNIVERSAL).brand("bma").build();

    segmentRepository.findByBrand("bma") >> [segments]
    when:
    def result = surfaceBetPublicService.findActiveEdpSurfaceBets("bma", eventId)

    then:
    result.size() == 1

    and:
    result.stream().allMatch(isAllSurfaceBetsRelationTypesIn(Arrays.asList(RelationType.edp.name())))
    SurfaceBetDto surfaceBetDto = (SurfaceBetDto) result.get(0)
    surfaceBetDto.getReference().isEnabled()
  }

  def "test find active SurfaceBet for RefDisabled"() {
    given:
    def surfaceBets = edpSurfaceBets()
    surfaceBets.get(0).getReferences().getAt(0).setEnabled(false);
    surfaceBets.get(0).getReferences().getAt(1).setEnabled(false);
    repository.findUniversalRecordsByBrandAndActiveTrue(*_) >> surfaceBets
    serveApiProvider.api(_) >> siteServerApi
    siteServerApi.getEventToOutcomeForOutcome(*_) >> createEvents(surfaceBets, true)
    def eventId = "123456"
    def segments = Segment.builder().segmentName(SegmentConstants.UNIVERSAL).brand("bma").build();

    segmentRepository.findByBrand("bma") >> [segments]
    when:
    def result = surfaceBetPublicService.findActiveEdpSurfaceBets("bma", eventId)

    then:
    result.size() == 0
  }

  def "test find active NonUniversalSurfaceBet for edp"() {
    given:
    def surfaceBets = edpSurfaceBets()
    surfaceBets.get(0).setDisabled(true);
    repository.findUniversalRecordsByBrandAndActiveTrue(*_) >> surfaceBets
    serveApiProvider.api(_) >> siteServerApi
    siteServerApi.getEventToOutcomeForOutcome(*_) >> createEvents(surfaceBets, true)
    def eventId = "123456"
    def segments = Segment.builder().segmentName("segment1").brand("bma").build();

    segmentRepository.findByBrand("bma") >> [segments]
    when:
    def result = surfaceBetPublicService.findActiveEdpSurfaceBets("bma", eventId)

    then:
    result.size() == 1
  }

  def "test find active NonUniversalSurfaceBet for edpOff"() {
    given:
    def surfaceBets = edpSurfaceBets()
    surfaceBets.get(0).setEdpOn(false);
    repository.findUniversalRecordsByBrandAndActiveTrue(*_) >> surfaceBets
    serveApiProvider.api(_) >> siteServerApi
    siteServerApi.getEventToOutcomeForOutcome(*_) >> createEvents(surfaceBets, true)
    def eventId = "123456"
    def segments = Segment.builder().segmentName("segment1").brand("bma").build();

    segmentRepository.findByBrand("bma") >> [segments]
    when:
    def result = surfaceBetPublicService.findActiveEdpSurfaceBets("bma", eventId)

    then:
    result.size() == 1
  }
  def "test SurfaceBet with SP price is returned for edp"() {
    given:
    def surfaceBets = edpSurfaceBets()
    repository.findUniversalRecordsByBrandAndActiveTrue(*_) >> surfaceBets
    serveApiProvider.api(_) >> siteServerApi
    siteServerApi.getEventToOutcomeForOutcome(*_) >> createEvents(surfaceBets, false)
    def eventId = "123456"
    def segments = Segment.builder().segmentName(SegmentConstants.UNIVERSAL).brand("bma").build();

    segmentRepository.findByBrand("bma") >> [segments]

    when:
    def result = surfaceBetPublicService.findActiveEdpSurfaceBets("bma", eventId)

    then:
    result.size() == 1

    and:
    result.stream().allMatch(isAllSurfaceBetsRelationTypesIn(Arrays.asList(RelationType.edp.name())))
    SurfaceBetDto surfaceBetDto = (SurfaceBetDto) result.get(0)
    surfaceBetDto.getReference().isEnabled()
    Objects.nonNull(surfaceBetDto.getSelectionEvent())
  }

  def "test SurfaceBetException is thrown"() {
    given:
    SurfaceBetRepository repository = Mock()
    SiteServeApiProvider serveApiProvider = Mock()
    SegmentRepository segmentRepository = Mock()

    repository.findByBrand(*_) >> edpSurfaceBets()
    serveApiProvider.api(_) >> { throw new RuntimeException("Sth wrong") }
    SurfaceBetPublicService surfaceBetPublicService = new SurfaceBetPublicService(repository, serveApiProvider,segmentRepository)
    def eventId = "123456"

    when:
    surfaceBetPublicService.findActiveEdpSurfaceBets("bma", eventId)

    then:
    thrown SurfaceBetException
  }

  private static List<SurfaceBet> edpSurfaceBets() {
    TestUtil.deserializeListWithJackson("service/public_api/find_edp_surface_bets_response.json", SurfaceBet.class)
  }

  private static List<SurfaceBet> getSameEventSurfaceBet() {
    TestUtil.deserializeListWithJackson("service/public_api/find_edp_surface_bets_expiredbetid_response.json", SurfaceBet.class)
  }

  Optional<List<Event>> createEvents(List<SurfaceBet> surfaceBets, boolean withPrice) {
    return Optional.of(surfaceBets.stream().map(toEvent(withPrice)).collect(Collectors.toList()))
  }

  Predicate<SurfaceBetDto> isAllEnabled() {
    return new Predicate<SurfaceBetDto>() {
          @Override
          boolean test(SurfaceBetDto sb) {
            return Boolean.FALSE.equals(sb.getDisabled()) && sb.getReference().isEnabled()
          }
        }
  }

  Predicate<SurfaceBetDto> isAllSurfaceBetsRelationTypesIn(List<String> expectedRelationTypes) {
    return new Predicate<SurfaceBetDto>() {
          @Override
          boolean test(SurfaceBetDto sb) {
            return expectedRelationTypes.contains(sb.getReference().getRelationType())
          }
        }
  }

  Function<SurfaceBet, Event> toEvent(boolean withPrice) {
    return new Function<SurfaceBet, Event>() {
          @Override
          Event apply(SurfaceBet surfaceBet) {

            def outcome = new Outcome()
            outcome.id = surfaceBet.getSelectionId().toString()

            def market = new Market()
            market.children = createChildren(outcome)

            if (withPrice) {
              def price = new Price()
              price.isActive = Boolean.TRUE
              price.isToPlace = Boolean.TRUE
              outcome.children = createChildren(price)
            } else {
              market.priceTypeCodes = "SP"
            }

            def event = new Event()
            event.children = createChildren(market)
            return event
          }

          List<Children> createChildren(Market market) {
            def children = new Children()
            children.market = market
            return Collections.singletonList(children)
          }

          List<Children> createChildren(Outcome outcome) {
            def children = new Children()
            children.outcome = outcome
            return Collections.singletonList(children)
          }

          List<Children> createChildren(Price price) {
            def children = new Children()
            children.price = price
            return Collections.singletonList(children)
          }
        }
  }


  def "test find active NonUniversalSurfaceBet for sport pages with page id 10 "() {
    given:
    repository.findByBrandAndDisplayFromIsBeforeAndDisplayToIsAfterAndDisabledIsFalseOrderBySortOrderAsc(*_) >>
        TestUtil.deserializeListWithJackson("service/public_api/find_surface_bets_response_with_page_10.json", SurfaceBet.class)


    def segments = Segment.builder().segmentName("segment1").brand("bma").build();

    segmentRepository.findByBrand("bma") >> [segments]

    when:
    def result = surfaceBetPublicService.findActiveByBrandAndRelationType("bma",new AtomicInteger(0), RelationType.sport, RelationType.eventhub)

    then:
    result.size() == 3
  }
}
