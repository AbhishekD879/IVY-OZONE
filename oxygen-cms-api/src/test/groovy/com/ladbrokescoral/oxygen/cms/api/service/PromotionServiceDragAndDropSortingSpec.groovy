package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto
import com.ladbrokescoral.oxygen.cms.api.entity.Promotion
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException
import com.ladbrokescoral.oxygen.cms.api.repository.PromoLeaderboardRepository
import com.ladbrokescoral.oxygen.cms.api.repository.PromotionRepository
import spock.lang.Specification

class PromotionServiceDragAndDropSortingSpec extends Specification {

  SortableService sortableService;
  PromotionRepository repoMock = Mock()
  private NavigationGroupService navigationGroupService;
  private PromoLeaderboardRepository promoLeaderboardRepository;
  private PromotionRepository repository;
  private ImageService imageService;
  private PromotionLeaderboardMsgPublishService msgPublishService;
  private NavItemService navItemService;

  def setup() {
    sortableService=new PromotionService(repoMock,null,null,null,msgPublishService,navItemService)
  }

  void prepareRepo() {
    repoMock.findById("a") >> Optional.of(buildPromotion("a", 1))
    repoMock.findById("b") >> Optional.of(buildPromotion("b", 2))
    repoMock.findById("c") >> Optional.of(buildPromotion("c", 3))
    repoMock.findById("d") >> Optional.of(buildPromotion("d", 4))
  }

  def "element changed order from first to third"() {
    given: "Sorted elements in asc order"
    prepareRepo()

    and:
    def newOrder = new OrderDto.OrderDtoBuilder()
        .id("a")
        .order(Arrays.asList("b", "c", "a", "d"))
        .build();

    when:
    sortableService.dragAndDropOrder(newOrder)

    then: "Only one element with id 'a' should change it's sortOrder. " +
    "New sortOrder value for element 'a' must be between sortOrder values of 'c' and 'd' elements"
    1 * repoMock.save(buildPromotion("a", 3.5))
  }

  def "element changed order from third to first"() {
    given: "Sorted elements in asc order"
    prepareRepo()

    and:
    def newOrder = new OrderDto.OrderDtoBuilder()
        .id("c")
        .order(Arrays.asList("c", "a", "b", "d"))
        .build();

    when:
    sortableService.dragAndDropOrder(newOrder)

    then: "Only one element with id 'c' should change it's sortOrder. " +
    "New sortOrder value for element 'c' must be lower than sortOrder of 'a' element"
    1 * repoMock.save(buildPromotion("c", 0))
  }

  def "element changed order from third to last"() {
    given: "Sorted elements in asc order"
    prepareRepo()

    and:
    def newOrder = new OrderDto.OrderDtoBuilder()
        .id("c")
        .order(Arrays.asList("a", "b", "d", "c"))
        .build();

    when:
    sortableService.dragAndDropOrder(newOrder)

    then: "Only one element with id 'c' should change it's sortOrder. " +
    "New sortOrder value for element 'c' must be grater than sortOrder of 'd' element"
    1 * repoMock.save(buildPromotion("c", 5.0))
  }

  def "element changed order from first to second"() {
    given: "Sorted elements in asc order"
    prepareRepo()

    and:
    def newOrder = new OrderDto.OrderDtoBuilder()
        .id("a")
        .order(Arrays.asList("b", "a", "c", "d"))
        .build();

    when:
    sortableService.dragAndDropOrder(newOrder)

    then: "Only one element with id 'a' should change it's sortOrder. " +
    "New sortOrder value for element 'a' must be grater than sortOrder of 'b' but lower than 'c' element"
    1 * repoMock.save(buildPromotion("a", 2.5))
  }

  def "changing order for not existed element should throw exception"() {
    given: "Sorted elements in asc order"
    prepareRepo()

    and:
    def newOrder = new OrderDto.OrderDtoBuilder()
        .id("q")
        .order(Arrays.asList("a", "b", "d", "q"))
        .build()

    repoMock.findById("q") >> Optional.empty()

    when:
    sortableService.dragAndDropOrder(newOrder)

    then:
    thrown(NotFoundException.class)
  }

  def "changing order for the only one element in array should not change sortOrder value"() {
    given: "Sorted elements in asc order"
    prepareRepo()

    and:
    def newOrder = new OrderDto.OrderDtoBuilder()
        .id("a")
        .order(Arrays.asList("a"))
        .build()

    when:
    sortableService.dragAndDropOrder(newOrder)

    then: "Only only one element with id 'a' should be saved with the same sortOrder value as it was before sorting"
    1 * repoMock.save(buildPromotion("a", 1.0))
  }

  // Edge case. Multiple elements have the same sort order.

  def "element's new position is between elements with the same sortOrder"() {
    given:

    repoMock.findById("a") >> Optional.of(buildPromotion("a", 1))
    repoMock.findById("b") >> Optional.of(buildPromotion("b", 2))
    repoMock.findById("c") >> Optional.of(buildPromotion("c", 2))
    repoMock.findById("d") >> Optional.of(buildPromotion("d", 2))
    repoMock.findByIdMatches(_ as List<String>) >> Arrays.asList(
        buildPromotion("a", 1),
        buildPromotion("b", 2),
        buildPromotion("c", 2),
        buildPromotion("d", 2))

    def newOrder = new OrderDto.OrderDtoBuilder()
        .id("a")
        .order(Arrays.asList("b", "a", "c", "d"))
        .build();

    when:
    sortableService.dragAndDropOrder(newOrder)

    then: "The whole list is recalculated and saved"
    1 * repoMock.saveAll(Arrays.asList(
        buildPromotion("a", 1.0),
        buildPromotion("b", 0.0),
        buildPromotion("c", 2.0),
        buildPromotion("d", 3.0)))
  }

  private static Promotion buildPromotion(String id, Double sortOrder) {
    Promotion promotion = new Promotion();
    promotion.setId(id)
    promotion.setSortOrder(sortOrder)
    return promotion
  }
}
