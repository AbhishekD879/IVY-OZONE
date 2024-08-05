package com.ladbrokescoral.oxygen.cms.api.service


import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository
import com.ladbrokescoral.oxygen.cms.util.TierCategoriesHelper
import spock.lang.Specification

class TierCategoriesCacheSpec extends Specification {
  private static final String CORAL_BRAND = "bma"
  private static final String LADBROKES_BRAND = "ladbrokes"

  TierCategoriesCache tierCategoriesCache
  SportCategoryRepository repository
  TierCategoriesHelper helper

  def setup() {
    repository = Mock(SportCategoryRepository)
    tierCategoriesCache = new TierCategoriesCache(repository)
    helper = new TierCategoriesHelper()
  }

  private List<SportCategory> initialCategories() {
    List<SportCategory> allCategories = new ArrayList<>()
    for (SportTier tier : SportTier.values()) {
      allCategories.addAll(helper.getCategories(CORAL_BRAND, tier))
      allCategories.addAll(helper.getCategories(LADBROKES_BRAND, tier))
    }
    return allCategories
  }

  private List<SportCategory> mockDbReturnFutureState() {
    def futureCategories = initialCategories()
    repository.findAll() >> initialCategories() >> futureCategories
    tierCategoriesCache.refreshCategoryIdsCache()
    return futureCategories
  }

  def 'should refresh categories'() {
    given: 'mock DB with initial categories'
    def futureCategories = mockDbReturnFutureState()
    and: 'capture initial tier 2 categories'
    def initialTier2Categories = tierCategoriesCache.getCategoryIds(CORAL_BRAND, SportTier.TIER_2)

    and: 'new sport appeared in repository'
    int newSportId = 12345
    futureCategories.add(TierCategoriesHelper.buildSportCategory(CORAL_BRAND, newSportId, SportTier.TIER_2))

    when: 'refresh cache'
    tierCategoriesCache.refreshCategoryIdsCache()

    then: 'new category exists in cache'
    !initialTier2Categories.contains(newSportId)
    tierCategoriesCache.getCategoryIds(CORAL_BRAND, SportTier.TIER_2).contains(newSportId)
  }

  def 'should retrieve sorted cache view'() {
    given:
    mockDbReturnFutureState()

    when:
    def cacheView = tierCategoriesCache.getCacheView()

    then:
    cacheView.get(0).getBrand() == CORAL_BRAND
    cacheView.get(5).getBrand() == LADBROKES_BRAND
    cacheView.get(0).getTier() == SportTier.TIER_1
    cacheView.get(5).getTier() == SportTier.UNTIED
  }
}
