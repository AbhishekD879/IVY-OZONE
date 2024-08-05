package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import java.util.Collection;
import java.util.List;
import org.springframework.data.mongodb.repository.Query;

public interface SportCategoryRepository extends CustomSegmentRepository<SportCategory> {
  @Query(value = "{ _id : {'$in' : [?0]}}", fields = "{targetUri : 1}")
  List<SportCategory> findAllByMatchingIds(Collection<String> ids);

  List<SportCategory> findAllByBrandOrderBySortOrderAsc(String brand);

  List<SportCategory> findAllByBrandAndDisabledOrderBySortOrderAsc(String brand, Boolean disabled);

  @Query(value = "{ 'targetUri' :{ '$in' : ['default', ?0]}, 'brand' : ?1}", fields = "{_id : 1}")
  List<SportCategory> findAllByMatchingTargetUri(String targetUri, String brand);

  @Query(value = "{ 'categoryId' : {'$in' : ?0}}")
  List<SportCategory> findAllByMatchingCategoryIds(List<Integer> categoryIds);

  @Query(value = "{ 'brand' : ?0, 'categoryId' : {'$in' : ?1}}")
  List<SportCategory> findAllByMatchingCategoryIds(String brand, Collection<Integer> categoryIds);

  List<SportCategory> findAllByDisabledFalse();

  List<SportCategory> findByBrandAndCategoryId(String brand, Integer categoryId);

  List<SportCategory> findByBrandAndImageTitle(String brand, String imageTitle);

  boolean existsByBrandAndCategoryId(String brand, Integer categoryId);

  @Query(
      "{ 'brand' : ?0, 'disabled':false, 'tier':{'$in':['TIER_1','TIER_2']} , 'categoryId':{$exists: true} ,'showInPlay':true}")
  List<SportCategory> findByBrandAndCategoryIdNotNullAndIsActiveAndInTier(String brand);

  @Query(value = "{ _id : {'$nin' : ?0 }, 'brand' : ?1,'disabled':false}")
  List<SportCategory> findByDisableFalseAndIdNotIn(List<String> ids, String brand);
}
