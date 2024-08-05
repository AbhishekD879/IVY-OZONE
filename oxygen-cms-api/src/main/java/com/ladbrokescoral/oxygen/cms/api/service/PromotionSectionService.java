package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.PromotionSection;
import com.ladbrokescoral.oxygen.cms.api.exception.PromotionNotFound;
import com.ladbrokescoral.oxygen.cms.api.repository.PromotionSectionRepository;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;

@Component
@Validated
public class PromotionSectionService extends SortableService<PromotionSection> {

  private final PromotionSectionRepository repo;

  private final PromotionService promotionService;

  @Autowired
  public PromotionSectionService(
      PromotionSectionRepository repo, PromotionService promotionService) {
    super(repo);
    this.repo = repo;
    this.promotionService = promotionService;
  }

  public void deletePromotionIdInSections(String brand, String promotionId) {
    findByBrand(brand)
        .forEach(
            s -> {
              if (s.getPromotionIds() != null) {
                final List<String> promotionIds =
                    new ArrayList<>(Arrays.asList(s.getPromotionIds().split(",")));
                if (!s.getId().equals(s.getBrand()) && promotionIds.contains(promotionId)) {
                  promotionIds.remove(promotionId);
                  s.setPromotionIds(promotionIds.isEmpty() ? null : String.join(",", promotionIds));
                  save(s);
                }
              }
            });
  }

  public void updatePromotionIdInSections(
      String brand, String existedPromotionId, String newPromotionId) {
    findByBrand(brand)
        .forEach(
            s -> {
              if (s.getPromotionIds() != null) {
                final List<String> promotionIds = Arrays.asList(s.getPromotionIds().split(","));
                if (!s.getId().equals(s.getBrand()) && promotionIds.contains(existedPromotionId)) {
                  promotionIds.set(promotionIds.indexOf(existedPromotionId), newPromotionId);
                  s.setPromotionIds(String.join(",", promotionIds));
                  save(s);
                }
              }
            });
  }

  public List<PromotionSection> findByBrandWithDefaultSectionSorted(String brand) {
    final List<PromotionSection> sections =
        repo.findSections(brand, SortableService.SORT_BY_SORT_ORDER_ASC);
    if (sections.stream().noneMatch(x -> x.getId().equals(brand))) {
      sections.add(unassignedSection(brand));
    }
    return sections;
  }

  public List<PromotionSection> findByBrandWithDefaultSection(String brand) {
    final List<PromotionSection> sections = super.findByBrand(brand);
    if (sections.stream().noneMatch(x -> x.getId().equals(brand))) {
      sections.add(unassignedSection(brand));
    }
    return sections;
  }

  public PromotionSection unassignedSection(String brand) {
    final List<PromotionSection> sections = super.findByBrand(brand);
    PromotionSection promotionSection = new PromotionSection();
    promotionSection.setUnassignedPromotionIds(unassignedPromotionIds(sections));
    promotionSection.setName("Unassigned promotions");
    promotionSection.setBrand(brand);
    promotionSection.setId(brand);
    promotionSection.setSortOrder(0.0);
    promotionSection.setDisabled(false);
    return promotionSection;
  }

  private List<String> unassignedPromotionIds(Collection<PromotionSection> byBrand) {
    final Set<String> collect =
        byBrand.stream()
            .flatMap(
                x ->
                    x.getPromotionIds() != null
                        ? Stream.of(x.getPromotionIds().split(","))
                        : Stream.empty())
            .collect(Collectors.toSet());
    return promotionService.findAllExceptPromotionIds(new ArrayList<>(collect)).stream()
        .map(AbstractEntity::getId)
        .collect(Collectors.toList());
  }

  @Override
  public PromotionSection save(PromotionSection section) {
    validateIfPromotionsIdAreExist(section);
    return super.save(section);
  }

  private void validateIfPromotionsIdAreExist(PromotionSection section) {
    if (section.getPromotionIds() != null && !section.getPromotionIds().isEmpty()) {
      final List<String> notFoundIds =
          Stream.of(section.getPromotionIds().split(","))
              .filter(
                  x ->
                      !promotionService
                          .findByBrandAndPromotionId(section.getBrand(), x)
                          .isPresent())
              .collect(Collectors.toList());
      if (!notFoundIds.isEmpty()) {
        throw new PromotionNotFound(String.join(",", notFoundIds));
      }
    }
  }
}
